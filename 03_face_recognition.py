import cv2
import numpy as np
import sqlite3
from datetime import datetime


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


conn = sqlite3.connect('attendance.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS attendance')
c.execute('''CREATE TABLE attendance (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                id INTEGER,
                name TEXT,
                roll_no TEXT,
                date TEXT,
                time TEXT,
                status TEXT
            )''')
conn.commit()


names = {1: "Tushar", 2: "Akash", 3: "Janish", 4: "Biswayan", 5: "kshitij"}  

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        if confidence < 60:
            name = names.get(id, "Unknown")
            cv2.putText(img, name, (x+5, y-5), font, 1, (0, 255, 0), 2)

            
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            c.execute("SELECT * FROM attendance WHERE id=? AND date=? AND status='Present'", (id, date))
            attendance_record = c.fetchone()
            if attendance_record is None:
                roll_no = "N/A"
                status = "Present"
                c.execute("INSERT INTO attendance (id, name, roll_no, date, time, status) VALUES (?, ?, ?, ?, ?, ?)", (id, name, roll_no, date, time, status))
                conn.commit()
                print(f"Attendance recorded for {name} on {date} at {time}")
        else:
            name = "Unknown"
            cv2.putText(img, name, (x+5, y-5), font, 1, (0, 0, 255), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Smart Attendance System', img)
    if cv2.waitKey(1) == 13:  
        break

cam.release()
cv2.destroyAllWindows()
conn.close()
