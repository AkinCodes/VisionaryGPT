# Correction SQLModel

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Correction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    poster_path: str
    original_prediction: str
    corrected_value: str
    correction_type: str  
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None