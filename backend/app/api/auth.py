# Register/Login endpoints

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from backend.app.models.user import User
from backend.app.core.database import get_session
from backend.app.core.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register_user(
    username: str, password: str, session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(username=username, hashed_password=hash_password(password))
    session.add(new_user)
    session.commit()
    return {"message": "User created"}


@router.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
