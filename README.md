# Drowsiness-Detection-System
This type of system mainly implemented for drivers to reduce or avoid road accidents.

# Major frameworks and library used:
Drowsiness detection with Python3.6, OpenCV and Dlib library.

# Run:
If you want to run this project:

You required a shape predictor file 'shape_predictor_68_face_landmarks.dat'. You can google it and download this file. 

Then open the terminal and run below command.

    python detect_drowsiness_V3.py --shape-predictor shape_predictor_68_face_landmarks.dat
    
    or,
    
    python detect_drowsiness_V3.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav
    
![Output-1](assets/1.png?raw=true "Real Time Video Streaming")
Real Time Video Streaming

![Output-2](assets/2.png?raw=true "Real Time Video Streaming with Alert Message")
Real Time Video Streaming with Alert Message

    python detect_drowsiness_V3.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav --sms +91********** --mail example@abc.com

![Output-3](assets/3.jpg?raw=true "Message")

Message recieved from server

![Output-4](assets/4.jpg?raw=true "E-mail")
E-mail recieved from server
