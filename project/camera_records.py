import logging
from shapely.geometry import Point, Polygon
from ultralytics import YOLO
import torch
import numpy as np
import json
import cv2
from PIL import Image





logging.basicConfig(level=logging.DEBUG)


class AiResult:

    def __init__(self, alarm: bool):
        self.alarm = alarm


class CameraRecords:

    def __init__(
        self,
        max_time_out_of_zone=1, 
        min_conf=.2,
        annotation_path="./model_files/annotations.json",
        flush_every=100,
    ):
        """
        Initialize the camera records

        Args:
            max_time_out_of_zone (int, optional): Maximum time in seconds out of the zone before
                triggering an alarm. Defaults to 1.
            min_conf (float, optional): Minimum confidence for detection. Defaults to .2.
            annotation_path (str, optional): Path to authorized zones. Defaults to "./model/annotations.json".
        """
        # Previous results
        self.previous_results = {}

        # Model
        self.model = YOLO('model_files/yolov8l.pt')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(device)

        # Parameters
        self.fps = 20 # frames per second
        self.resolution = (1920, 1088) # resolution of the camera
        self.max_time_out_of_zone = max_time_out_of_zone * self.fps # max time out of zone in frames        
        self.min_conf = min_conf # minimum confidence for the detection
        self.authorized_zones = self.get_authorized_zones(annotation_path) # authorized zones

        # Flush system to avoid memory leak
        self.flush_every = flush_every
        self.last_update = 0

    def add_result(self, id_frame, frame) -> AiResult:

        # prediction
        frame = Image.fromarray(np.array(frame))
        print(f'frame: {frame}')
        result = self.model.track(frame, persist=True, classes=[0], verbose=False)[0]
        print(f'result: {result}')
        boxes = result.boxes
        data = boxes.data.cpu().numpy()
        data = data[(data[:,5] > self.min_conf)]
        
        # iterate on every person in the frame and add it in the previous results
        alarm = False
        for d in data:

            self.last_update = id_frame

            coordinates = Point(
                (d[0] + d[2]) / 2,
                d[3]
            )
            indice = d[4]
            if indice not in self.previous_results:
                self.previous_results[indice] = []
            self.previous_results[indice].append(
                    {
                        "coordinates": coordinates,
                        "id_frame": id_frame,
                        "is_outside": all(not p.contains(coordinates) for p in self.authorized_zones)
                    }
                )

            # get alerts for every person given the max_time_out_of_zone
            nb_points = len(self.previous_results[indice])
            if self.previous_results[indice][-1]["is_outside"]:
                out = True
                i = 1
                current_frame = id_frame
                while out and i <= nb_points:
                    current_point = self.previous_results[indice][-i]
                    if current_point["is_outside"]:
                        current_frame = current_point["id_frame"]
                        i += 1
                    else:
                        out = False

                time_out_of_zone = id_frame - current_frame
                if time_out_of_zone > self.max_time_out_of_zone:
                    alarm = True

        if id_frame - self.last_update > self.flush_every:
            self.flush_memory()
            self.last_update = id_frame

        return AiResult(alarm)
    
    def flush_memory(self):
        self.previous_results = {}

    def get_authorized_zones(self, annotation_path):

        with open(annotation_path, 'r') as f:
            anns = json.load(f)[0]["annotations"]
            
        list_polygons = []
        
        for ann in anns:

            pts= ann["result"][0]["value"]["points"]

            for i in range(len(pts)):
                pts[i] = [
                    int(pts[i][0] * self.resolution[0] / 100),
                    int(pts[i][1] * self.resolution[1] / 100)
                ]

            pts = np.array(pts).reshape((-1, 2))
            
            list_polygons.append(Polygon(pts))
        
        return list_polygons