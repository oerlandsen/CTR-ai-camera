import os
from celery import Celery
from camera_records import CameraRecords
from telegram_manager import TelegramManager
from dotenv import load_dotenv

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

# example of a task
@celery_app.task
def process_frame(frame_id, frame, camera_id):
    print(f"Processing frame {type(frame)}")
    camera_record = CAMERAS[camera_id]["camera_record"]
    telegram_manager = CAMERAS[camera_id]["telegram_manager"]

    r = camera_record.add_result(frame_id, frame)
    telegram_manager.analyze(r)
    return {
        "alarm": r.alarm,
        "frame_id": frame_id,
        "camera_id": camera_id
    }
