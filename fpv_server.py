import io
import json
import time
from flask import Flask, Response, request, jsonify
from picamera2 import Picamera2
from __init__ import kit, lock

# ------------ LÝSING ------------
# Þetta forrit hýsir vefsíðu á RPi'inu sem hægt er að tengjast í gegnum IOT-research netið
# Á þessa vefsíður sendir Pi'inn stanslaust myndir frá Pi myndavélinni
# Þessari vefsíðu er síðan hægt að tengjast í hvaða tölvu sem er en það er mjög skemmtilegt að 
# gera það í gegnum VR gleraugu

app = Flask(__name__) # Nota Flask til þess að búa til vefsíðu

# Hugmyndin er að geta hreyft servo'a með VR gleraugunum (ekki virkandi)
PAN_SERVO = 3
kit.servo[PAN_SERVO].angle = 90

#camera = Picamera2()
#camera.configure(camera.create_video_configuration(
#    main={"size": (640, 480)}
#))
#camera.start()
time.sleep(1)

# ------
# Þetta eru föll tengt því að hreyfa servo'a með VR gleraugum (virkar ekki ennþá)
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def map_to_servo(value, in_min, in_max):
    return int((value - in_min) / (in_max - in_min) * 180)
# ------

# Hér er tekið mynd af Pi myndavélinni
def generate_frames():
    while True:
        stream = io.BytesIO()
        #camera.capture_file(stream, format='jpeg')
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + stream.read() + b'\r\n')
        time.sleep(0.033) # Alltaf biðið í þennan "x" tíma en hann stýrir þar með FPS á myndbandinu sem myndirnar mynda

# Hér er myndavélagluggi vefsíðunar sem sýnir myndirnar frá Pi myndavélinni
@app.route('/video')
def video():
    return Response(
        #generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# --------
# Hér er gluggi sem á að halda utan um VR hluta vefsíðu (virkar ekki eins og er)
@app.route('/headtracking', methods=['POST'])
def headtracking():
    try:
        data = request.get_json()
        yaw = data.get('yaw', 0)
        pan_angle = map_to_servo(clamp(yaw, -90, 90), -90, 90)
        print("Looking:", pan_angle)
        with lock:
            kit.servo[PAN_SERVO].angle = pan_angle
        return jsonify({'ok': True})
    except Exception as e:
        print(f"Tracking error: {e}")
        return jsonify({'error': str(e)}), 500
# -----

# Þetta er grunn vefsíðan
@app.route('/')
def index():
    return open('quest.html').read()

# Þetta er fall sem ræsir vefsíðuna en það er sér fall til þess að geta kallað á það sem þráð í main
def start_server():
    print("FPV server running...")
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == '__main__':
    start_server()