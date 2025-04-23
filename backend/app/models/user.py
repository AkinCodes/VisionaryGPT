# backend/app/models/user.py
from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Union[str, None] = None 
    disabled: bool = False
