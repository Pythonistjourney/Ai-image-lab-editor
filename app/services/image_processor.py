from PIL import Image
import cv2
import numpy as np
from typing import Tuple, Optional

def load_image(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")

def save_image(img: Image.Image, path: str):
    img.save(path)

def resize_image(img: Image.Image, max_size: int = 1024) -> Image.Image:
    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        return img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return img

def cv2_to_pil(cv_img: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))