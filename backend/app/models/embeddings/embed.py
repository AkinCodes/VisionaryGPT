# Embedding request/response models

from typing import List 
from typing import Optional
from pydantic import BaseModel

class EmbedRequest(BaseModel):
    filepath: str
    description: Optional[str] = None 

class EmbedResponse(BaseModel):
    embedding: List[float]
