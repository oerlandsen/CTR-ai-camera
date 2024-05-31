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

# import logging

# logging.basicConfig(level=logging.DEBUG)

# class CameraRecords:
#     _instance = None

#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(CameraRecords, cls).__new__(cls, *args, **kwargs)
#             logging.debug("Creating a new instance of CameraRecords")
#         return cls._instance

#     def __init__(self):
#         if not hasattr(self, 'initialized'):
#             self.value = 0
#             self.initialized = True
#             logging.debug("Initializing CameraRecords with value = 0")

#     def store_result(self, result):
#         logging.debug(f"Storing result: {result} (current value: {self.value})")
#         self.value += result
#         logging.debug(f"New value: {self.value}")

#     def get_value(self):
#         logging.debug(f"Getting current value: {self.value}")
#         return self.value

# camera_record = CameraRecords()


# example of a task
@celery_app.task
def add(x, y):
    current_value = camera_record.get_value()
    result = current_value + x + y
    camera_record.store_result(result)
    return result
