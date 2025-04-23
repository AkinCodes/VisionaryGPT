# Poster genre classification

from fastapi import APIRouter, HTTPException
from backend.app.models.common.filepath_request import FilepathRequest
from backend.app.services.classification.genre_classifier import GenreClassifier

router = APIRouter()
classifier = GenreClassifier()

# @router.post("/", summary="Classify genre from poster")
# def classify_poster(request: FilepathRequest):
#     result = classifier.predict(request.filepath)

#     # Check if the prediction returned an error (low confidence)
#     if "error" in result:
#         raise HTTPException(status_code=400, detail=result["error"])

#     # If confidence is too low, return an error response
#     if result["confidence"] < 0.4:
#         print(f"Low confidence detected: {result['confidence']}")  # Debugging output
#         return {"error": "Classification confidence too low"}

#     return result

@router.post("/", summary="Classify genre from poster")
def classify_poster(request: FilepathRequest):
    result = classifier.predict(request.filepath)

    # Add a low_confidence flag if the top prediction is below 0.4
    result["low_confidence"] = result["confidence"] < 0.4

    if result["low_confidence"]:
        print(f"Low confidence detected: {result['confidence']}")  # Optional debug info

    return result

