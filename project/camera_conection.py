import cv2
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("URL_RTSP"))

cap = cv2.VideoCapture(
    os.environ.get("URL_RTSP")
)

id_frame = 0
while cap.isOpened():
    success, frame = cap.read()
    if success:
        # here process the frame and send it to the workers_api
        # in production you have to chance the localhost to the container name
        response = requests.post(
            f"http://0.0.0.0:8000/camera/101/frame/{id_frame}", 
            json={
                "frame": frame.tolist()
            })
        print('success')
        id_frame += 1
    else:
        break
