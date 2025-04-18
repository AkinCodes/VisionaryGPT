# Feedback SQLModel
from sqlmodel import SQLModel, Field
from typing import Optional

class FeedbackItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    poster_path: str
    liked: bool
