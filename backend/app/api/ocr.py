# app/api/ocr.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.app.models.ocr import OCRResponse
from backend.app.services.ocr.ocr_reader import OCRReader
import easyocr  

router = APIRouter()
ocr = OCRReader()

@router.post("/", summary="Extract text from an image", response_model=OCRResponse)
async def extract_text(file: UploadFile = File(...), language: str = 'en'):
    try:
        print(f"Received headers: {file.headers}")

        image_data = await file.read()
        print(f"Received image with size: {len(image_data)} bytes")

        results = ocr.extract_text(image_data, language)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text: {str(e)}")

@router.get("/languages", summary="List supported OCR languages", response_model=List[str])
async def get_supported_languages():
    try:
        return easyocr.Reader.lang_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch languages: {str(e)}")
