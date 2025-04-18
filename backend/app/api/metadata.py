from fastapi import APIRouter, HTTPException
from backend.app.models.metadata.metadata import MetadataRequest, MetadataResponse
from backend.app.services.metadata.clip_gpt_generator import PosterMetadataGenerator  # Import from the correct file
from dotenv import load_dotenv
import os  

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("API key is missing. Please set the OPENAI_API_KEY environment variable.")

router = APIRouter()

@router.post("/", response_model=MetadataResponse)
def generate_metadata(request: MetadataRequest):
    # Initialize PosterMetadataGenerator
    metadata_generator = PosterMetadataGenerator()
    
    try:
        metadata = metadata_generator.generate_metadata(request.filepath)
        return MetadataResponse(gpt_output=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating metadata: {str(e)}")
