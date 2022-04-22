from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(capture):
    while True:
        ref, frame = capture.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cv2.VideoCapture(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

