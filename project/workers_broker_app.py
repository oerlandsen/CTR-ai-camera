from celery import Celery
from camera_records import camera_record

CELERY_BROKER_URL='redis://redis-broker:6379/0'
CELERY_RESULT_BACKEND='redis://redis-broker:6379/0'

celery_app = Celery('CTR-cameras', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.conf.update(
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
    timezone='America/Santiago',
)

# example of a task
@celery_app.task
def add(x, y):
    current_value = camera_record.get_value()
    result = current_value + x + y
    camera_record.store_result(result)
    return result
