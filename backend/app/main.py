from fastapi import FastAPI
from backend.app.api.embedding import router as embedding_router
from backend.app.api.remix import router as remix_router
from backend.app.api.classify import router as classify_router
from backend.app.api.ocr import router as ocr_router
from backend.app.api.metadata import router as metadata_router
from backend.app.api.generation import router as generation_router
from backend.app.api.feedback import router as feedback_router
from backend.app.api.faces import router as faces_router
from backend.app.api.detect import router as detect_router
from backend.app.api.auth import router as auth_router
from backend.app.api.active_learning import router as active_learning_router
from backend.app.api.simple_test import router as simple_test_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(embedding_router, prefix="/embed", tags=["Embeddings"])
app.include_router(remix_router, prefix="/remix", tags=["Remix"])
app.include_router(classify_router, prefix="/classify", tags=["Classify"])
app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(metadata_router, prefix="/metadata", tags=["Metadata"])
app.include_router(generation_router, prefix="/generation", tags=["Generation"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])
app.include_router(faces_router, prefix="/faces", tags=["Faces"])
app.include_router(detect_router, prefix="/detect", tags=["Detection"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(
    active_learning_router, prefix="/active_learning", tags=["Active Learning"]
)
app.include_router(simple_test_router, prefix="/simple-test", tags=["Simple Test"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")




# Testing by adding a basic route to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to VisionaryGPT!"}
