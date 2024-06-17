import os
from celery import Celery
from camera_records import CameraRecords
from telegram_manager import TelegramManager
from dotenv import load_dotenv
import cv2
import numpy as np
import multiprocessing

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')



load_dotenv()

celery_app = Celery(
    'CTR-cameras', 
    broker=os.environ.get("CELERY_BROKER_URL"), 
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)

celery_app.conf.update(
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
    timezone='America/Santiago',
)

CAMERAS = {
    101: {
        "camera_record": CameraRecords(),
        "telegram_manager": TelegramManager(
            message="Alert Camera 101: someone is walking outside of the authorized area!",
            max_frame=20
        )
    }
}

@celery_app.task(name="workers_broker_app.process_frame_task")
def process_frame(data):
    camera_id = data.get("camera_id")
    frame_id = data.get("frame_id")
    frame_content = data.get("frame_content")
    frame = cv2.imdecode(np.frombuffer(frame_content, np.uint8), cv2.IMREAD_COLOR).tolist()
    camera_record = CAMERAS[camera_id]["camera_record"]
    telegram_manager = CAMERAS[camera_id]["telegram_manager"]

    r = camera_record.add_result(frame_id, frame)
    telegram_manager.analyze(r)
    return {
        "alarm": r.alarm,
        "frame_id": frame_id,
        "camera_id": camera_id
    }
