import cv2
import os

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('Enter User ID (number): ')
name = input('Enter Name: ')

if not os.path.exists('dataset'):
    os.makedirs('dataset')

cam = cv2.VideoCapture(0)
print("Capturing face samples. Look at the camera...")

count = 0
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        
        cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('Face Capture', frame)

    if cv2.waitKey(1) == 13 or count >= 50:  
        break

cam.release()
cv2.destroyAllWindows()
print("Dataset collection complete!")


