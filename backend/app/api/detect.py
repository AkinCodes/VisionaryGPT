# Object detection with YOLO

from fastapi import APIRouter, HTTPException
from backend.app.models.embeddings import EmbedRequest
from ultralytics import YOLO
from PIL import Image
from pydantic import BaseModel
from typing import List

class DetectionResponse(BaseModel):
    labels: List[str]
    coordinates: List[List[float]]

router = APIRouter()

# Load YOLO model (only once when the server starts)
model = YOLO("yolov8n.pt")

@router.post("/", response_model=DetectionResponse)
def detect_objects(request: EmbedRequest):
    try:
        image = Image.open(request.filepath)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading image: {str(e)}")

    results = model(image)

    boxes = results[0].boxes
    if boxes is None or boxes.cls is None:
        return DetectionResponse(labels=[], coordinates=[])

    labels = [model.names[int(cls)] for cls in boxes.cls.tolist()]
    coordinates = boxes.xyxy.tolist()

    return DetectionResponse(labels=labels, coordinates=coordinates)
