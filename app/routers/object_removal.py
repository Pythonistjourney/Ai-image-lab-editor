from fastapi import APIRouter, Depends, UploadFile, File
from app.services.object_removal_service import remove_object
# ...

@router.post("/")
async def remove_obj(file: UploadFile = File(...)):
    input_path = await save_uploaded_image(file)
    output_path = await remove_object(input_path)
    return {"output": output_path}