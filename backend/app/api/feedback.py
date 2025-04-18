from fastapi import APIRouter
from backend.app.models.feedback.feedback import FeedbackItem
import json
from pathlib import Path

router = APIRouter()
FEEDBACK_FILE = Path("app/data/user_feedback.json")


@router.post("/")
def store_feedback(item: FeedbackItem):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    feedback = []

    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE) as f:
            feedback = json.load(f)

    feedback.append(item.dict())

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f, indent=2)

    return {"message": "Feedback saved"}
