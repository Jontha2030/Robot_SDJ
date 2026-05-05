import io
import json
import threading
import time
from flask import Flask, Response
from flask_sock import Sock
from picamera2 import Picamera2
from adafruit_servokit import ServoKit

app = Flask(__name__)
sock = Sock(app)
kit = ServoKit(channels=8)

# Servo channels
PAN_SERVO  = 1  # left/right (yaw)

# Initialize servos to center
kit.servo[PAN_SERVO].angle  = 90
# Setup camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(
    main={"size": (640, 480)}
))
camera.start()
time.sleep(1)

# ---- Camera Stream ----
def generate_frames():
    while True:
        stream = io.BytesIO()
        camera.capture_file(stream, format='jpeg')
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + stream.read() + b'\r\n')
        time.sleep(0.033)  # ~30fps

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# ---- Head Tracking ----
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def map_to_servo(value, in_min, in_max):
    # Maps head rotation to 0-180 servo range
    return int((value - in_min) / (in_max - in_min) * 180)

@sock.route('/headtracking')
def headtracking(ws):
    print("Quest connected")
    while True:
        try:
            data = json.loads(ws.receive())
            yaw   = data.get('yaw', 0)    # left/right (-180 to 180)
            # Map to servo angles
            pan_angle  = map_to_servo(clamp(yaw,   -90,  90), -90,  90)
            print("Looking,",pan_angle)

            kit.servo[PAN_SERVO].angle  = pan_angle

        except Exception as e:
            print(f"Tracking error: {e}")
            break
    print("Quest disconnected")

# ---- Serve the HTML page ----
@app.route('/')
def index():
    return open('quest.html').read()

if __name__ == '__main__':
    print("Server running...")
    app.run(host='0.0.0.0', port=5000, threaded=True, ssl_context='adhoc')  # generates self-signed cert automatically