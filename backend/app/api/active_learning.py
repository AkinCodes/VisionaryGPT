# Save uncertain predictions with correction

from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend.app.models.active_learning.correction import Correction
from backend.app.core.database import get_session

router = APIRouter()


@router.post("/corrections")
def save_correction(item: Correction, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    return {"message": "Correction saved"}
