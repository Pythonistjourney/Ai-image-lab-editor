from fastapi import APIRouter, Depends, UploadFile, File
from app.services.cartoon_stylization_service import cartoonize_image
# ...

@router.post("/")
async def cartoonize(file: UploadFile = File(...)):
    input_path = await save_uploaded_image(file)
    output_path = await cartoonize_image(input_path)
    return {"output": output_path}