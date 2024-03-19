from flask import Flask, render_template, Response
import cv2
import numpy as np  # For generating sound (optional)

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def play_alert_sound():
    # Example using NumPy for sound generation (replace with your preferred method)
    duration = 1  # Duration in seconds
    frequency = 440  # Frequency in Hz
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    y = np.sin(2 * np.pi * frequency * t)



def gen_frames():
    face_count = 0
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            faces = detector.detectMultiScale(gray, 1.1, 7)

            # Draw rectangle around each face and update count
            face_count = len(faces)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Overlay face count text and alert message
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"Faces Detected: {face_count}", (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            if face_count >= 5:
                cv2.putText(frame, "ALERT: 5 Faces Detected!classroom limit exceeded", (10, 60), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                play_alert_sound()  # Play sound alert

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Assuming you have an index.html template

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
