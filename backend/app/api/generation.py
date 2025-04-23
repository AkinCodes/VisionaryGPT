import os
import tempfile
import uuid
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from backend.app.models.generation.generation import GenerationResponse
from backend.app.services.generation.stable_diffusion import StableDiffusionGenerator

router = APIRouter()
generator = StableDiffusionGenerator()

UPLOAD_FOLDER = tempfile.mkdtemp() 

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/", response_model=GenerationResponse)
async def generate_poster(
    prompt: str = Form(...), 
    file: UploadFile = File(...),
    user_id: int = Form(...)  
):
    try:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        image_url = generator.generate(prompt, file_path)

        with Session(engine) as session:
            new_poster = create_generated_poster(session, user_id, prompt, image_url)

        os.remove(file_path)

        return GenerationResponse(output=image_url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating poster: {str(e)}")
