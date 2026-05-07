import io
import time
import threading
from pathlib import Path

from flask import Flask, Response, request, jsonify, send_from_directory

# ---------------- Optional hardware imports ----------------
# The server still starts even if the servo/camera libraries are not available.
try:
    from __init__ import kit, lock  # your existing servo setup
except Exception as exc:
    print(f"Servo hardware disabled: {exc}")
    kit = None
    lock = threading.Lock()

try:
    from picamera2 import Picamera2
except Exception as exc:
    print(f"Pi camera disabled: {exc}")
    Picamera2 = None

# ---------------- Flask setup ----------------
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)

# ---------------- Servo setup ----------------
PAN_SERVO = 3
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_CENTER = 90
YAW_LIMIT_DEGREES = 90  # -90 deg left -> 0 servo, +90 deg right -> 180 servo

last_servo_angle = SERVO_CENTER


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def yaw_to_servo_angle(yaw_degrees):
    yaw = clamp(float(yaw_degrees), -YAW_LIMIT_DEGREES, YAW_LIMIT_DEGREES)
    angle = SERVO_CENTER + yaw
    return int(round(clamp(angle, SERVO_MIN, SERVO_MAX)))


def set_pan_servo(angle):
    global last_servo_angle
    angle = int(clamp(angle, SERVO_MIN, SERVO_MAX))
    last_servo_angle = angle

    if kit is None:
        print(f"[SIM] Servo angle: {angle}")
        return

    with lock:
        kit.servo[PAN_SERVO].angle = angle


# Center servo on startup, if hardware is available.
try:
    set_pan_servo(SERVO_CENTER)
except Exception as exc:
    print(f"Could not center servo: {exc}")

# ---------------- Camera setup ----------------
camera = None
if Picamera2 is not None:
    try:
        camera = Picamera2()
        camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
        camera.start()
        time.sleep(1)
        print("Pi camera started")
    except Exception as exc:
        print(f"Could not start Pi camera: {exc}")
        camera = None


def generate_frames():
    """MJPEG stream for the browser. Sends a tiny empty frame if camera is unavailable."""
    while True:
        stream = io.BytesIO()

        if camera is not None:
            try:
                camera.capture_file(stream, format="jpeg")
            except Exception as exc:
                print(f"Camera frame error: {exc}")
        else:
            # No camera: do not crash the stream. The page will still test WebXR/servo control.
            stream.write(b"")

        stream.seek(0)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n"
        )
        time.sleep(1 / 30)


# ---------------- Routes ----------------
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "quest_webxr.html")


@app.route("/video")
def video():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/headtracking", methods=["POST"])
def headtracking():
    try:
        data = request.get_json(force=True) or {}
        yaw = float(data.get("yaw", 0))
        angle = yaw_to_servo_angle(yaw)
        set_pan_servo(angle)

        return jsonify({
            "ok": True,
            "yaw": yaw,
            "servo_angle": angle,
            "hardware_servo": kit is not None,
        })
    except Exception as exc:
        print(f"Tracking error: {exc}")
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/status")
def status():
    return jsonify({
        "ok": True,
        "servo_angle": last_servo_angle,
        "hardware_servo": kit is not None,
        "camera": camera is not None,
    })


def start_server():
    print("FPV WebXR server running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    start_server()
