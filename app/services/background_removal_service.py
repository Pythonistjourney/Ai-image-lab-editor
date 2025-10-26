from rembg import remove
from PIL import Image
from app.services.image_processor import load_image, save_image
from app.utils.logger import logger

async def remove_background(image_path: str) -> str:
    try:
        img = load_image(image_path)
        output_img = remove(img)
        output_path = image_path.replace(".jpg", "_no_bg.png")
        save_image(output_img, output_path)
        logger.info(f"Removed background: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Background removal error: {e}")
        raise