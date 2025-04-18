from fastapi import APIRouter, HTTPException
from backend.app.models.common.filepath_request import FilepathRequest
from backend.app.services.classification.genre_classifier import GenreClassifier
from backend.app.models.embeddings.embed import EmbedRequest, EmbedResponse
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from pathlib import Path
import torch

# Initialize the CLIP processor and model
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
router = APIRouter()

@router.post("/", response_model=EmbedResponse)
def embed_image(request: EmbedRequest):
    image_path = Path(request.filepath).resolve()
    print(f"Received filepath: {request.filepath}")  
    print(f"Resolved image path: {image_path}")  

    if not image_path.exists():
        raise HTTPException(status_code=400, detail="File not found")
    if not image_path.is_file():
        raise HTTPException(status_code=400, detail="Provided path is not a valid file")

    try:
        image = Image.open(image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error opening image: {str(e)}")

    inputs = processor(images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)

    embedding = embeddings.squeeze().tolist()
    return EmbedResponse(embedding=embedding)
