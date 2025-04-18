# Poster remix API
from fastapi import APIRouter
from backend.app.models.remix.remix_request import RemixRequest
from backend.app.services.remix.remix_engine import PosterRemixEngine

router = APIRouter()
engine = PosterRemixEngine()

@router.post("/", summary="Poster remix via A + B - C")
def remix(request: RemixRequest):
    result_url = engine.remix(
        anchor_path=request.poster_a_path,
        add_path=request.poster_b_path,
        subtract_path=request.poster_c_path,
        prompt=request.remix_prompt
    )
    return {"image_url": result_url}
