from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.models.user import UserCreate, UserInDB
from app.models.schemas import Token, TokenData
from app.config import settings
from app.utils.logger import logger

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(db: AsyncIOMotorDatabase, username: str):
    user_doc = await db.users.find_one({"username": username})
    if user_doc:
        return UserInDB(id=str(user_doc["_id"]), **user_doc)

async def authenticate_user(db: AsyncIOMotorDatabase, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/register", response_model=Token)
async def register(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    db_user = await get_user(db, form_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(form_data.password)
    user_dict = UserCreate(username=form_data.username, email=form_data.username + "@example.com", password=hashed_password).dict()
    user_dict.pop("password")
    user_dict["hashed_password"] = hashed_password
    user_dict["edits"] = []
    await db.users.insert_one(user_dict)
    logger.info(f"User {form_data.username} registered")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    logger.info(f"User {user.username} logged in")
    return {"access_token": access_token, "token_type": "bearer"}