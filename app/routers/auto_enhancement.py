from fastapi import APIRouter, Depends, UploadFile, File
from app.services.auto_enhancement_service import auto_enhance_image
# ...

@router.post("/")
async def enhance(file: UploadFile = File(...)):
    input_path = await save_uploaded_image(file)
    output_path = await auto_enhance_image(input_path)
    return {"output": output_path}