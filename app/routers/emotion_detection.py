from fastapi import APIRouter, Depends, UploadFile, File
from app.utils.file_handler import save_uploaded_image
from app.services.emotion_detection_service import detect_emotion
from app.dependencies import get_current_user
from app.models.user import UserInDB
from app.utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/")
async def detect(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    input_path = await save_uploaded_image(file)
    try:
        result = await detect_emotion(input_path)
        await db.users.update_one(
            {"username": current_user.username},
            {"$push": {"edits": {"func": "emotion_detect", "emotion": result["emotion"], "timestamp": datetime.utcnow().isoformat()}}}
        )
        logger.info(f"Emotion detected for {current_user.username}: {result['emotion']}")
        return result
    except Exception as e:
        logger.error(f"Emotion detection endpoint error: {e}")
        return {"error": str(e)}