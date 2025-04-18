# app/models/ocr.py
from pydantic import BaseModel
from fastapi import UploadFile
from typing import List


class OCRRequest(BaseModel):
    file: UploadFile 
    language: str 

class OCRResponse(BaseModel):
    text: List[str] 
