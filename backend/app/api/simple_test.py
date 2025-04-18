from fastapi import APIRouter
from pydantic import BaseModel

# Test: Define a simple model with just one field.
class SimpleRequest(BaseModel):
    name: str

router = APIRouter()

# Simple route for testing the model
@router.post("/", response_model=SimpleRequest)
def simple_endpoint(request: SimpleRequest):
    return request
