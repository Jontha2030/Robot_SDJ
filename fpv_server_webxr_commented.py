"""
fpv_server_webxr_commented.py

Raspberry Pi Flask server for a Quest/WebXR head-tracking servo project.

What this server does:
1. Hosts the HTML/JavaScript page that the Quest Browser opens.
2. Provides a /video MJPEG stream from the Pi camera.
3. Receives yaw values from the headset at /headtracking.
4. Converts yaw into a servo angle and moves the servo.
5. Provides /status so the webpage can check whether the Pi/server is alive.

Run this on the Raspberry Pi, not on your laptop:
    python3 fpv_server_webxr_commented.py

Then, in another Pi terminal:
    ngrok http 5000

Open the HTTPS ngrok URL in Quest Browser.
"""

import io
import time
import threading
from pathlib import Path

from flask import Flask, Response, request, jsonify, send_from_directory


# -----------------------------------------------------------------------------
# Optional hardware imports
# -----------------------------------------------------------------------------
# These imports depend on Raspberry Pi hardware/libraries.
# During development, it is useful if the Flask website can still run even when
# the servo or camera is disconnected. That is why these imports are wrapped in
# try/except blocks instead of being allowed to crash the whole program.

try:
    # This imports your existing servo controller object and thread lock.
    # "kit" is probably an Adafruit ServoKit instance from your __init__.py.
    # "lock" prevents two threads from trying to move the servo at the same time.
    from __init__ import kit, lock
except Exception as exc:
    # If the servo setup fails, run in simulation mode.
    # The server will print servo angles instead of moving real hardware.
    print(f"Servo hardware disabled: {exc}")
    kit = None
    lock = threading.Lock()

try:
    # Picamera2 is the Raspberry Pi camera library.
    from picamera2 import Picamera2
except Exception as exc:
    # If the camera library is missing or unavailable, the server still runs.
    print(f"Pi camera disabled: {exc}")
    Picamera2 = None


# -----------------------------------------------------------------------------
# Flask setup
# -----------------------------------------------------------------------------

# BASE_DIR is the folder containing this Python file.
# It lets Flask find quest_webxr.html even if you start Python from another place.
BASE_DIR = Path(__file__).resolve().parent

# Create the Flask application object.
# This object owns the routes such as /, /video, /headtracking, and /status.
app = Flask(__name__)


# -----------------------------------------------------------------------------
# Servo setup and mapping constants
# -----------------------------------------------------------------------------

# Servo channel on the ServoKit board.
# In your original code, the pan servo was connected to channel 3.
PAN_SERVO = 3

# Normal hobby servos usually accept angles from 0 to 180 degrees.
SERVO_MIN = 0
SERVO_MAX = 180

# Center position for the pan servo.
SERVO_CENTER = 90

# The headset yaw value is limited to -90 to +90 degrees.
# -90 means looking far left, +90 means looking far right.
YAW_LIMIT_DEGREES = 90

# Store the most recent angle so /status can report it.
last_servo_angle = SERVO_CENTER


def clamp(value, min_val, max_val):
    """Keep value inside the range [min_val, max_val]."""
    return max(min_val, min(max_val, value))


def yaw_to_servo_angle(yaw_degrees):
    """
    Convert Quest headset yaw into a servo angle.

    The JavaScript sends yaw relative to the starting head direction:
        -90 degrees = look left
          0 degrees = look forward
        +90 degrees = look right

    This function maps that to:
          0 degrees = servo left
         90 degrees = servo center
        180 degrees = servo right

    Because SERVO_CENTER is 90, the formula is simple:
        servo_angle = 90 + yaw

    Then the result is clamped to protect the servo from invalid angles.
    """
    yaw = clamp(float(yaw_degrees), -YAW_LIMIT_DEGREES, YAW_LIMIT_DEGREES)
    angle = SERVO_CENTER + yaw
    return int(round(clamp(angle, SERVO_MIN, SERVO_MAX)))


def set_pan_servo(angle):
    """
    Move the pan servo, or simulate movement if no servo hardware is available.

    This is the only function that actually talks to the servo hardware.
    Keeping all servo movement here makes the code easier to debug.
    """
    global last_servo_angle

    # Make sure the requested angle is safe.
    angle = int(clamp(angle, SERVO_MIN, SERVO_MAX))

    # Save this even in simulation mode so /status still reports useful data.
    last_servo_angle = angle

    # If kit is None, the hardware import failed.
    # In that case, print the intended angle instead of crashing.
    if kit is None:
        print(f"[SIM] Servo angle: {angle}")
        return

    # Use a lock because Flask is running with threaded=True.
    # Multiple requests could arrive close together, and the hardware library
    # should not be accessed by two threads at exactly the same time.
    with lock:
        kit.servo[PAN_SERVO].angle = angle


# Center the servo when the server starts.
# This is wrapped in try/except because hardware can fail independently of Flask.
try:
    set_pan_servo(SERVO_CENTER)
except Exception as exc:
    print(f"Could not center servo: {exc}")


# -----------------------------------------------------------------------------
# Camera setup
# -----------------------------------------------------------------------------

camera = None

# Only try to create the camera object if Picamera2 imported successfully.
if Picamera2 is not None:
    try:
        camera = Picamera2()

        # Configure the stream resolution.
        # Lower resolution reduces bandwidth and latency.
        camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))

        # Start the camera.
        camera.start()

        # Give the camera a moment to warm up before grabbing frames.
        time.sleep(1)

        print("Pi camera started")
    except Exception as exc:
        print(f"Could not start Pi camera: {exc}")
        camera = None


def generate_frames():
    """
    Generate an MJPEG video stream for the browser.

    MJPEG is basically a never-ending sequence of JPEG images.
    The browser receives these images through the /video route and displays them
    in the <img src="/video"> element in the HTML page.

    If the camera is unavailable, this function sends an empty frame instead of
    crashing. That lets you test WebXR and servo control without a camera.
    """
    while True:
        # BytesIO is an in-memory file-like object.
        # Picamera2 can write a JPEG into it.
        stream = io.BytesIO()

        if camera is not None:
            try:
                # Capture one JPEG frame into memory.
                camera.capture_file(stream, format="jpeg")
            except Exception as exc:
                print(f"Camera frame error: {exc}")
        else:
            # No camera: keep the HTTP stream alive with empty data.
            stream.write(b"")

        # Go back to the beginning of the memory buffer so stream.read() works.
        stream.seek(0)

        # Yield one MJPEG frame.
        # The boundary and Content-Type format are what tell the browser this is
        # a sequence of JPEG images rather than one normal file.
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n"
        )

        # Aim for about 30 frames per second.
        time.sleep(1 / 30)


# -----------------------------------------------------------------------------
# Flask routes
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """
    Serve the main webpage.

    When the Quest Browser opens the ngrok URL, it requests /.
    Flask responds by sending quest_webxr.html.
    """
    return send_from_directory(BASE_DIR, "quest_webxr.html")


@app.route("/video")
def video():
    """
    Serve the live camera stream.

    The HTML page contains:
        <img id="stream" src="/video">

    That causes the browser to request this route.
    """
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/headtracking", methods=["POST"])
def headtracking():
    """
    Receive head-tracking data from the Quest webpage.

    The JavaScript sends JSON like:
        { "yaw": 23.5 }

    This function:
    1. Reads the yaw value.
    2. Converts it into a servo angle.
    3. Moves the servo.
    4. Sends JSON back so the webpage can show the servo angle.
    """
    try:
        # force=True tells Flask to parse JSON even if the browser's content type
        # is unusual. The "or {}" protects against an empty body.
        data = request.get_json(force=True) or {}

        # Get the yaw value sent by JavaScript.
        # If missing, default to 0 degrees.
        yaw = float(data.get("yaw", 0))

        # Convert headset yaw to servo angle.
        angle = yaw_to_servo_angle(yaw)

        # Move the servo or print a simulated angle.
        set_pan_servo(angle)

        # Reply to the browser with useful debugging information.
        return jsonify({
            "ok": True,
            "yaw": yaw,
            "servo_angle": angle,
            "hardware_servo": kit is not None,
        })
    except Exception as exc:
        # If anything goes wrong, print it in the Pi terminal and return an error
        # to the browser.
        print(f"Tracking error: {exc}")
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/status")
def status():
    """
    Small debugging endpoint used by the webpage when it first loads.

    It confirms that:
    - the Pi server is reachable
    - the servo hardware import worked
    - the camera started
    - the current servo angle is known
    """
    return jsonify({
        "ok": True,
        "servo_angle": last_servo_angle,
        "hardware_servo": kit is not None,
        "camera": camera is not None,
    })


# -----------------------------------------------------------------------------
# Server startup
# -----------------------------------------------------------------------------

def start_server():
    """Start Flask so other devices on the network/ngrok can access it."""
    print("FPV WebXR server running on http://0.0.0.0:5000")

    # host="0.0.0.0" means listen on all network interfaces, not just localhost.
    # This is why your Quest/ngrok can reach it.
    #
    # threaded=True allows Flask to handle the video stream and /headtracking
    # requests at the same time.
    app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    start_server()
