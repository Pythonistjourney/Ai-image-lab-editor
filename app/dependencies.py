from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.database import get_db
from app.models.user import UserInDB
from app.models.schemas import TokenData
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.users.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return UserInDB(id=str(user["_id"]), **user)