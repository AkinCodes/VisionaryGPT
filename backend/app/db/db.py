# backend/app/db/db.py
from sqlmodel import Session, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.app.models.models import User, GeneratedPoster

# Setup SQLAlchemy session
engine = create_engine("sqlite:///database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def validate_user_exists(session: Session, user_id: int) -> bool:
    """Check if the user exists in the database."""
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user is not None

def create_generated_poster(session: Session, user_id: int, prompt: str, image_url: str):
    """Create a new generated poster, ensuring the user exists."""
    if not validate_user_exists(session, user_id):
        raise ValueError(f"User with ID {user_id} does not exist.")
    
    generated_poster = GeneratedPoster(user_id=user_id, prompt=prompt, image_url=image_url)
    
    session.add(generated_poster)
    session.commit()
    session.refresh(generated_poster)
    return generated_poster
