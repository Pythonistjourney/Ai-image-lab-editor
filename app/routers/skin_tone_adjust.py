from fastapi import APIRouter, Depends, UploadFile, File, Query
from typing import Literal
from app.utils.file_handler import save_uploaded_image
from app.services.skin_tone_adjust_service import adjust_skin_tone
from app.dependencies import get_current_user
from app.models.user import UserInDB
from app.models.schemas import ImageResponse
from app.utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ImageResponse)
async def adjust_tone(
    file: UploadFile = File(...),
    preset: Literal["warm", "cool", "fair", "deep"] = Query("warm"),
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    input_path = await save_uploaded_image(file)
    try:
        output_path = await adjust_skin_tone(input_path, preset)
        await db.users.update_one(
            {"username": current_user.username},
            {"$push": {"edits": {"func": "skin_tone", "preset": preset, "timestamp": datetime.utcnow().isoformat()}}}
        )
        logger.info(f"Skin tone adjusted ({preset}) for {current_user.username}")
        return ImageResponse(output_path=output_path, download_url=f"/core/download/{output_path}", metadata={"preset": preset})
    except Exception as e:
        logger.error(f"Skin tone endpoint error: {e}")
        return {"error": str(e)}