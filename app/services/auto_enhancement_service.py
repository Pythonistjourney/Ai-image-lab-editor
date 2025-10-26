from PIL import ImageEnhance
from app.services.image_processor import load_image, save_image
from app.utils.logger import logger

async def auto_enhance_image(image_path: str) -> str:
    try:
        img = load_image(image_path)
        # Simple auto-enhance chain
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.05)
        output_path = image_path.replace(".jpg", "_enhanced.jpg")
        save_image(img, output_path)
        logger.info(f"Auto-enhanced image: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Auto-enhancement error: {e}")
        raise