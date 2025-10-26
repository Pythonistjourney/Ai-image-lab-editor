from fastapi import APIRouter, Depends, UploadFile, File
from app.utils.file_handler import save_uploaded_image
from app.services.colorization_service import colorize_image
from app.dependencies import get_current_user
from app.models.user import UserInDB
from app.models.schemas import ImageResponse
from app.utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ImageResponse)
async def colorize(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    input_path = await save_uploaded_image(file)
    try:
        output_path = await colorize_image(input_path)
        # Log edit
        await db.users.update_one(
            {"username": current_user.username},
            {"$push": {"edits": {"func": "colorize", "timestamp": datetime.utcnow().isoformat(), "input": file.filename}}}
        )
        logger.info(f"Colorized for {current_user.username}")
        return ImageResponse(output_path=output_path, download_url=f"/core/download/{output_path}", metadata={"func": "colorize"})
    except Exception as e:
        logger.error(f"Colorize endpoint error: {e}")
        return {"error": str(e)}