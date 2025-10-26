from fastapi import APIRouter, Depends, UploadFile, File
from app.utils.file_handler import save_uploaded_image
from app.services.background_removal_service import remove_background
# ... (similar to colorization)

router = APIRouter()

@router.post("/")
async def remove_bg(file: UploadFile = File(...)):
    input_path = await save_uploaded_image(file)
    output_path = await remove_background(input_path)
    return {"output": output_path}