import os
import shutil
from fastapi import UploadFile, File
from PIL import Image
from typing import Callable

UPLOAD_DIR = "/tmp/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_image(file: UploadFile = File(...)) -> str:
    if not file.content_type.startswith("image/"):
        raise ValueError("File must be an image")
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Basic validation
    try:
        img = Image.open(path)
        img.verify()
        img.close()
    except Exception:
        os.remove(path)
        raise ValueError("Invalid image file")
    return path

def cleanup_temp(path: str):
    if os.path.exists(path):
        os.remove(path)