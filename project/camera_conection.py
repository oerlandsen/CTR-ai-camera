import cv2
import requests
import os
from dotenv import load_dotenv
import time
import io

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
        _, buffer = cv2.imencode('.jpg', frame)  # Convert the frame to JPEG format
        frame_file = io.BytesIO(buffer)
        print('before post to workers api')
        # Send the frame as multipart/form-data
        response = requests.post(
            f"http://workers-api:8000/camera/101/frame/{id_frame}", 
            files={"frame": frame_file}
        )
        print('success')
        id_frame += 1
        time.sleep(1)
    else:
        break
