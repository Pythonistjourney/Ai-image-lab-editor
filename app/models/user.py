from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str  # MongoDB ObjectId as str
    hashed_password: str

    class Config:
        from_attributes = True  # For dict-to-model
