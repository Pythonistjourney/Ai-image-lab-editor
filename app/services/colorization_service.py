from PIL import Image
import torch
from transformers import pipeline
from app.services.image_processor import load_image, save_image, resize_image
from app.utils.logger import logger

# Lazy load HF colorization pipeline
_colorizer = None

def get_colorizer():
    global _colorizer
    if _colorizer is None:
        device = 0 if torch.cuda.is_available() else -1  # GPU if avail, else CPU
        _colorizer = pipeline(
            "image-to-image",
            model="RichardZhang/colorization-v2",  # Proven GAN for B&W → RGB
            device=device,
            torch_dtype=torch.float16 if device != -1 else torch.float32
        )
    return _colorizer

async def colorize_image(image_path: str) -> str:
    try:
        img = load_image(image_path)
        if img.mode != 'L':  # Ensure grayscale input
            img = img.convert('L').convert('RGB')  # Quick prep
        img = resize_image(img, 224)  # Model optimal size
        colorizer = get_colorizer()
        colored = colorizer(img, num_inference_steps=20)["generated_image"][0]  # Generate & extract
        output_path = image_path.replace(".jpg", "_colored.jpg").replace(".png", "_colored.png")
        save_image(colored, output_path)
        logger.info(f"HF Colorized {image_path} → {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Colorization error: {e}")
        raise