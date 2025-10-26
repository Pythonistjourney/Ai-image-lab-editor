import cv2
import numpy as np
from PIL import Image
from app.services.image_processor import load_image, cv2_to_pil, save_image
from app.utils.logger import logger
from typing import Literal

PRESETS = {
    "warm": {"r": 1.1, "g": 1.0, "b": 0.9},
    "cool": {"r": 0.9, "g": 1.0, "b": 1.1},
    "fair": {"brightness": 1.1, "contrast": 1.0},
    "deep": {"brightness": 0.9, "contrast": 1.1}
}

async def adjust_skin_tone(image_path: str, preset: Literal["warm", "cool", "fair", "deep"]) -> str:
    try:
        img = load_image(image_path)
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Simple skin tone adjustment (TODO: Use ML for better detection)
        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        # Apply preset (basic curve adjustment)
        factors = PRESETS.get(preset, PRESETS["warm"])
        adjusted = cv_img.copy()
        adjusted[:, :, 0] *= factors["b"]  # Blue
        adjusted[:, :, 1] *= factors["g"]  # Green
        adjusted[:, :, 2] *= factors["r"]  # Red
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        
        output_img = cv2_to_pil(adjusted)
        output_path = image_path.replace(".jpg", f"_{preset}.jpg").replace(".png", f"_{preset}.png")
        save_image(output_img, output_path)
        logger.info(f"Adjusted skin tone ({preset}): {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Skin tone adjustment error: {e}")
        raise