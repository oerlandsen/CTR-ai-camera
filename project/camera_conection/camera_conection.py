import cv2
import requests
import os
from dotenv import load_dotenv
import time
import io
import subprocess

load_dotenv()

# Check if the VPN container is running and wait for the VPN connection
vpn_container = os.getenv('VPN_CONTAINER', '0') == '1'
if vpn_container:
    while True:
        try:
            subprocess.check_call(['ping', '-c', '1', '10.240.206.185'])
            break
        except subprocess.CalledProcessError:
            print("Waiting for VPN connection...")
            time.sleep(5)

print(os.environ.get("URL_RTSP"))

cap = cv2.VideoCapture(os.environ.get("URL_RTSP"))

id_frame = 0
time.sleep(5)
while cap.isOpened():
    success, frame = cap.read()
    if success:
        # Process the frame and send it to the workers_api
        _, buffer = cv2.imencode('.jpg', frame)  # Convert the frame to JPEG format
        frame_file = io.BytesIO(buffer)
        print('before post to workers api')
        # Send the frame as multipart/form-data
        response = requests.post(
            f"http://producer:8000/camera", 
            files={"frame": frame_file},
            data={"camera_id": 101, "frame_id": id_frame}
        )
        print('success')
        id_frame += 1
        time.sleep(0.5)
    else:
        break
