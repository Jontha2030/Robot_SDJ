"""
fpv_server_webxr.py

Lýsing
What this server does:
1. Hosts the HTML/JavaScript page that the Quest Browser opens.
2. Provides a /video MJPEG stream from the Pi camera.
3. Receives yaw values from the headset at /headtracking.
4. Converts yaw into a servo angle and moves the servo.
5. Provides /status so the webpage can check whether the Pi/server is alive.

1. RPi'inn hýsir vefsíðu í gegnum ngrok sem hægt er að opna með tölvu sem er með browser (og þá aðallega Quest VR gleraugum)
2. RPi'inn sendir straum af myndum úr Picamera myndavél á vefsíðu sem skilar sér því í myndbands streymi
3. Vefsíðan les hreyfi upplýsingar úr VR gleraugum og sendir á bakenda vefsíðu
4. RPi'inn les þær upplýsingar af bakendanum og hreyfir servo mótóra sem nemur hreyfingu notanda, en á þessum servo mótór situr myndavélin


Keyrt í gegnum main.py

Í annari tölvu, með ngrok sett upp, þarf að keyra:
    ngrok http 5000
sem hýsir https vefsíðu í gegnum ngrok (nauðsynlegt til að fá heimild til að lesa upplýsingar af VR gleraugum)

"""

import io
import time
from pathlib import Path

from flask import Flask, Response, request, jsonify, send_from_directory

from __init__ import kit, lock

from picamera2 import Picamera2


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

# Hér er skilgreint hvar servo er tengdur á PCB borðinu, en það eru 8 tengi, frá 0-7
PAN_SERVO = 3

# Set snúnings mörk til þess að fá ekki "angle out of range" villu
SERVO_MIN = 0
SERVO_MAX = 180

# Miðjustaða
SERVO_CENTER = 90

# Þar sem að við látum servoinn alltaf byrja í 90° (miðjan), á hann bara að geta hreyfst í +-90°
YAW_LIMIT_DEGREES = 90

# Breyta sem mun vera sent á vefsíðu
last_servo_angle = SERVO_CENTER


def clamp(value, min_val, max_val):
    """Sér til þess að gildin sem send eru á servo'ana séu á bilinu 0-180°"""
    return max(min_val, min(max_val, value))


def yaw_to_servo_angle(yaw_degrees):
    """
    Frá bakendanum, sem unnin er af Javascript, er staða snúnings miðuð við að 
        -90° = alveg til vinstri
          0° = beint áfram
        +90° = alveg til hægri
        
    en, þar sem að servo'inn táknar 90° sem miðjuna, hliðrum við því sem kemur frá Javascript um akkúrat 90° (0 + 90 = 90)
    """
    yaw = clamp(float(yaw_degrees), -YAW_LIMIT_DEGREES, YAW_LIMIT_DEGREES)
    angle = SERVO_CENTER + yaw
    return int(round(clamp(angle, SERVO_MIN, SERVO_MAX)))


def set_pan_servo(angle):
    """
    Þetta fall talar við servo mótórinn og hreyfir hann í samræmi við VR gleraugun.
    "angle" sem er sett inn í þetta fall er búið að fara í gegnum yaw_to_servo_angle() fallið
    """
    global last_servo_angle

    # Make sure the requested angle is safe.
    angle = int(clamp(angle, SERVO_MIN, SERVO_MAX))

    # Þetta var hugsað fyrir það að birta stöðu servo's á vefsíðu
    last_servo_angle = angle

    # Nota lock til þess að breyta stöðu servo'a, en þetta er gerir okkur kleyft að skilgreina servo controller tenginguna
    # í einu falli, __init__ sem öll önnur föll í öllum forritum róbótans erfa
    with lock:
        kit.servo[PAN_SERVO].angle = angle


# Hér er sett servo'inn í miðjuna þegar forrit er ræst (höfum í try-except ef ehv. skyldi fara úrskeiðis)
try:
    set_pan_servo(SERVO_CENTER)
except Exception as exc:
    print(f"Could not center servo: {exc}")


# -----------------------------------------------------------------------------
# Camera setup
# -----------------------------------------------------------------------------

camera = None # Ef myndavélin er ekki skynjuð á forritið samt ennþá að ganga, það verður bara engin mynd á vefsíðunni

try:
    camera = Picamera2()

    # Hér er skilgreint stærð myndar
    camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))

    camera.start()

    # Ekki vitlaust að bíða í smá á meðan myndavél ræsist
    time.sleep(1)

    print("Pi camera started")
except Exception as exc:
    print(f"Could not start Pi camera: {exc}")
    camera = None


def generate_frames():
    """
    Hér er sótt myndir af myndavélinni og send sem straumur af myndum á vefsíðu sem myndar því myndband
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
            # Ef engin myndavél fynnst er sent tómt boð, en þá keyrir forritið a.mk..
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

        # Hér er hraði straums sem við stillum á 30fps
        time.sleep(1 / 30)


# -----------------------------------------------------------------------------
# Flask routes (þetta er bara klassísk vefforritun sem gervigreindin cookaði)
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
