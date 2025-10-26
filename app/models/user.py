from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str  # MongoDB ObjectId as str
    hashed_password: str
    edits: list = []  # Track user edits, e.g., [{"func": "colorize", "timestamp": "2025-10-26"}]

    class Config:
        from_attributes = True