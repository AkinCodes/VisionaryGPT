# RemixRequest model

from pydantic import BaseModel

class RemixRequest(BaseModel):
    poster_a_path: str  # e.g. "static/uploads/posterA.jpg"
    poster_b_path: str  # e.g. "static/uploads/posterB.jpg"
    poster_c_path: str  # e.g. "static/uploads/posterC.jpg"
    remix_prompt: str   # Optional creative description (optional override)



