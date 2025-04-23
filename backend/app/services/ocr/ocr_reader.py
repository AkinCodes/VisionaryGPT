from fastapi import HTTPException
from backend.app.models.ocr import OCRResponse
from io import BytesIO
from PIL import Image
import easyocr

class OCRReader:
    def __init__(self):
        self.reader_cache = {}

    def get_reader(self, language: str):
        if language in ['ch_sim', 'ch_tra']:
            lang_combo = [language, 'en']
        else:
            lang_combo = [language]

        key = tuple(lang_combo)
        if key not in self.reader_cache:
            self.reader_cache[key] = easyocr.Reader(lang_combo, gpu=False)  # CPU-only
        return self.reader_cache[key]

    def extract_text(self, image_data: bytes, language: str = 'en'):
        try:
            # Perform OCR on the image with the specified language
            reader = self.get_reader(language)

            # Use in-memory bytes instead of file path
            image = Image.open(BytesIO(image_data))

            # Process the image using EasyOCR
            results = reader.readtext(image)

            # Extract each text line from the results
            text_lines = [item[1] for item in results]  

            # Return the response model with the list of detected text lines
            return OCRResponse(text=text_lines)  # Return text as a list of strings
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error performing OCR: {str(e)}")
