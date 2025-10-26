import cv2
import numpy as np
from app.services.image_processor import load_image, cv2_to_pil, save_image
from app.utils.logger import logger

async def cartoonize_image(image_path: str) -> str:
    try:
        img = load_image(image_path)
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(cv_img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        output_img = cv2_to_pil(cartoon)
        output_path = image_path.replace(".jpg", "_cartoon.jpg")
        save_image(output_img, output_path)
        logger.info(f"Cartoonized image: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Cartoon stylization error: {e}")
        raise