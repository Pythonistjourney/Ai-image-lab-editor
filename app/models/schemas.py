from pydantic import BaseModel
from typing import Optional
from app.models.user import UserInDB

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ImageUpload(BaseModel):
    filename: str
    path: str

class ImageResponse(BaseModel):
    output_path: str
    download_url: str
    metadata: dict = {}