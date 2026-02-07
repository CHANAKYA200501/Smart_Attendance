import cv2
import numpy as np
from PIL import Image
import os


recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        
        if imagePath.startswith('.') or not imagePath.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            PIL_img = Image.open(imagePath).convert('L')  
        except Exception as e:
            print(f"Skipping file {imagePath}: {e}")
            continue

        img_numpy = np.array(PIL_img, 'uint8')

        
        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except:
            print(f"Skipping file {imagePath}: invalid filename format")
            continue

        
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. Please wait...")

faces, ids = getImagesAndLabels('dataset')
recognizer.train(faces, np.array(ids))


if not os.path.exists('trainer'):
    os.makedirs('trainer')
recognizer.write('trainer/trainer.yml')

print(f"{len(np.unique(ids))} faces trained successfully.")
