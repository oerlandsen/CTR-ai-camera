import cv2
import requests

URL_RTSP = 'rtsp://admin:ctr_isp2021@10.240.206.185:554/Streaming/channels/101'
cap = cv2.VideoCapture(URL_RTSP)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # here process the frame and send it to the workers_api
        # in production you have to chance the localhost to the container name
        # response = requests.post("http://localhost:8000/add/1/2")
        print('succes')
    else:
        break
