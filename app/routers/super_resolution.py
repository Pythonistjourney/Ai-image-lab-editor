from fastapi import APIRouter, Depends, UploadFile, File
from app.services.super_resolution_service import upscale_image
# ...

@router.post("/")
async def upscale(file: UploadFile = File(...), scale: int = 2):
    input_path = await save_uploaded_image(file)
    output_path = await upscale_image(input_path, scale)
    return {"output": output_path}