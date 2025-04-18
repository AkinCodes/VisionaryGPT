from pydantic import BaseModel

class MetadataRequest(BaseModel):
    filepath: str

class MetadataResponse(BaseModel):
    gpt_output: str
