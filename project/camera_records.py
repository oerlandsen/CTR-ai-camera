
import logging

logging.basicConfig(level=logging.DEBUG)

class CameraRecords:

    def __init__(self):
        self.value = 0
        self.initialized = True
        logging.debug("Initializing CameraRecords with value = 0")

    def store_result(self, result):
        logging.debug(f"Storing result: {result} (current current value: {self.value})")
        self.value = result
        logging.debug(f"New value: {self.value}")

    def get_value(self):
        logging.debug(f"Getting current value: {self.value}")
        return self.value

camera_record = CameraRecords()
