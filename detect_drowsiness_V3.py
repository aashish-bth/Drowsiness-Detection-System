# python detect_drowsiness_V3.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav
# python detect_drowsiness_V3.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav --sms +918092727929 --mail aashish.bth@gmail.com

from scipy.spatial import distance as dist
from imutils import face_utils
from threading import Thread
import playsound
import argparse
import dlib
import cv2

def sound_alarm(path):
	playsound.playsound(path)

def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])

	ear = (A + B) / (2.0 * C)
	return ear

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="", help="path alarm .WAV file")
ap.add_argument("-s", "--sms", type=str, default="", help="enter number with country code like +91 for India")
ap.add_argument("-m", "--mail", type=str, default="", help="enter email address like example@mail.com")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 28
MSG_COUNT_THRESH = 1

COUNTER = 0
ALARM_ON = False
MSG_COUNTER = 0

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("\n[ INFO:0] Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("[ INFO:1] Starting video streaming...")
cap = cv2.VideoCapture(0)

while True:
	frame = cap.read()[1]
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		cv2.putText(frame,'FACE',(x+w//2-9,y+h+9), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (11,255,255), 2, cv2.LINE_AA)

	rects = detector(gray, 0)
	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		ear = (leftEAR + rightEAR) / 2.0

		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		if ear < EYE_AR_THRESH:
			COUNTER += 1

			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				if not ALARM_ON:
					ALARM_ON = True
					MSG_COUNTER += 1

					if args["alarm"] != "":
						t = Thread(target=sound_alarm, args=(args["alarm"],))
						t.deamon = True
						t.start()

				cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		else:
			COUNTER = 0
			ALARM_ON = False

		cv2.putText(frame, "E.A.R. - {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
		if MSG_COUNTER > MSG_COUNT_THRESH:
			import location
			if args["sms"] != "":
				import sms
				sms.send_sms(args["sms"], location.website, location.co_ordinates)
			else:
				print("\nUnable to send SMS, plz provide a registered mobile number.")
			if args["mail"] !="":
				import mail
				mail.send_mail(args["mail"], location.website, location.co_ordinates, location.msg_distance)
			else:
				print("\nUnable to send Email, plz provide an email id.")
			MSG_COUNTER = 0
 
	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
	   break

cap.release()
cv2.destroyAllWindows()
