from flask import Flask, Blueprint, render_template, Response, request, redirect,url_for
import cv2
import face_recognition
import numpy as np
import os
import time
import imutils 
from imutils.video import VideoStream
from werkzeug.utils import redirect
from flask_login import login_required, current_user
from __init__ import create_app, db
from werkzeug.utils import secure_filename
main = Blueprint('main', __name__)
# app=Flask(__name__)
app = create_app()

@app.route("/")
def home():
    return render_template('index2.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route("/home")
def mainpage():
    return render_template('home.html')

# @app.route("/")
# def home():
#     return render_template('home.html')


@app.route('/upload')  
def upload():  
    return render_template("file_upload_form.html")

@app.route('/success', methods = ['POST'])  
def success(): 
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, 'filename') 
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)

        return render_template("success.html", name = f.filename)  

@app.route('/video')
def calc():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    #print(Path('C:\\flask\\face_finish\\face_rec.py'))
    
    Dain_image = face_recognition.load_image_file("Dain/Dain.jpg")
    # Dain_image = face_recognition.load_image_file("Dain/Dain2.jpg")
    Dain_face_encoding = face_recognition.face_encodings(Dain_image)[0]

    Jungmin_image = face_recognition.load_image_file("Jungmin/Jungmin.jpg") 
    # Jungmin_image = face_recognition.load_image_file("Jungmin/Jungmin2.jpg")
    Jungmin_face_encoding = face_recognition.face_encodings(Jungmin_image)[0]

    Minah_image = face_recognition.load_image_file("Minah/Minah.jpg") 
    Minah_face_encoding = face_recognition.face_encodings(Minah_image)[0]

    Geunoh_image = face_recognition.load_image_file("Geunoh/Geunoh.jpg") 
    Geunoh_face_encoding = face_recognition.face_encodings(Geunoh_image)[0]

# Create arrays of known face encodings and their names
    known_face_encodings = [
        Dain_face_encoding,
        Jungmin_face_encoding, 
        Minah_face_encoding,
        Geunoh_face_encoding
    ]
    known_face_names = [
        "Dain",
        "Jungmin",
        "Minah",
        "Geunoh"
    ]
# Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    def gen_frames(): 
        camera = cv2.VideoCapture(0)
        while True: 
            success, frame = camera.read()  # read the camera frame
            frame = cv2.flip(frame,1)
            if not success:
                break
            else:
                #Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                #Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                #Only process every other frame of video to save time
                
                #Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    #See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    #Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                

                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 4)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom + 1), (right, bottom), (0, 255, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, top - 10), font, 1.0, (0, 255, 255), 2)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(debug=True)
