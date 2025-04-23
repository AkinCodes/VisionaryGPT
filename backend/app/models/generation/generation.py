# GeneratedPoster SQLModel

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

class GenerationRequest(BaseModel):
    prompt: str  
    filepath: str 

class GenerationResponse(BaseModel):
    output: str 