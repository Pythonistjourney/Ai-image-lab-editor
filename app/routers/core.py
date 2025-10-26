from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.utils.file_handler import save_uploaded_image, cleanup_temp
from app.utils.validators import validate_image_size
from app.dependencies import get_current_user
from app.models.user import UserInDB
from app.models.schemas import ImageUpload, ImageResponse
from app.utils.logger import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/upload", response_model=ImageUpload)
async def upload_image(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        path = await save_uploaded_image(file)
        if not validate_image_size(path):
            cleanup_temp(path)
            raise HTTPException(status_code=400, detail="Image too large (>10MB)")
        # Log edit to user
        await db.users.update_one(
            {"username": current_user.username},
            {"$push": {"edits": {"func": "upload", "timestamp": datetime.utcnow().isoformat(), "filename": file.filename}}}
        )
        logger.info(f"User {current_user.username} uploaded {file.filename}")
        return ImageUpload(filename=file.filename, path=path)
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

@router.get("/download/{path:path}")
async def download_image(path: str, current_user: UserInDB = Depends(get_current_user)):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return {"download_url": f"/static/{path}"}  # TODO: Serve via static files in prod