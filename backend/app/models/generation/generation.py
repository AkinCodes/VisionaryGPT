# GeneratedPoster SQLModel

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

class GenerationRequest(BaseModel):
    prompt: str  
    filepath: str 

class GenerationResponse(BaseModel):
    output: str 

# class GeneratedPoster(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     prompt: str
#     image_url: str
