from app.services.ml_models import get_inpainter
from PIL import Image
from app.services.image_processor import load_image, save_image
from app.utils.logger import logger

async def remove_object(image_path: str, mask_path: Optional[str] = None) -> str:
    try:
        img = load_image(image_path)
        inpainter = get_inpainter()
        # TODO: Use mask for inpainting
        inpainted = inpainter(prompt="clean background", image=img, mask_image=Image.new("RGB", img.size, (255, 255, 255))).images[0]
        output_path = image_path.replace(".jpg", "_inpainted.jpg")
        save_image(inpainted, output_path)
        logger.info(f"Removed object: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Object removal error: {e}")
        raise