from flask import Flask, render_template, Response
import cv2
import time

app = Flask(__name__)

def gen_frames():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Unable to open camera")
        while True:
            time.sleep(1)
            continue  # Keeps connection open without crashing

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)