# YOLOv8 detection logic

from ultralytics import YOLO
from PIL import Image
import numpy as np


class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):  
        self.model = YOLO(model_path)

    def detect_objects(self, image_path: str):
        results = self.model(image_path)[0] 
        boxes = results.boxes
        labels = results.names
        detections = []

        for box in boxes:
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = results.names[cls_id]

            detections.append(
                {"label": label, "confidence": round(conf, 3), "box": [x1, y1, x2, y2]}
            )

        return detections
