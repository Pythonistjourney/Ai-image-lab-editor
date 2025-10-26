from PIL import Image
from typing import Optional

def validate_image_size(image_path: str, max_size_mb: int = 10) -> bool:
    size_mb = os.path.getsize(image_path) / (1024 * 1024)
    return size_mb <= max_size_mb

def get_image_dimensions(image_path: str) -> tuple[int, int]:
    with Image.open(image_path) as img:
        return img.size