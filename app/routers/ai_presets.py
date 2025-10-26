from fastapi import APIRouter, Depends, UploadFile, File
from app.services.ai_presets_service import generate_ai_presets
# ... 

@router.post("/")
async def generate_presets(file: UploadFile = File(...), num: int = 3):
    input_path = await save_uploaded_image(file)
    presets = await generate_ai_presets(input_path, num)
    return {"presets": presets}