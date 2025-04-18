# Face detection

from fastapi import APIRouter
from backend.app.models.embeddings import EmbedRequest
from backend.app.services.faces.face_analyzer import FaceAnalyzer

router = APIRouter()
analyzer = FaceAnalyzer()  # Provide path to known faces directory

@router.post("/", summary="Detect and recognize faces in an image")
def detect_faces(request: EmbedRequest):
    try:
        results = analyzer.detect_faces(request.filepath)
        if not results:
            return {"error": "No faces detected"}
        return {"faces": results}
    except FileNotFoundError:
        return {"error": f"File not found at {request.filepath}"}
    except ValueError:
        return {"error": f"Invalid image format or corrupted image at {request.filepath}"}
    except Exception as e:
        return {"error": str(e)}

