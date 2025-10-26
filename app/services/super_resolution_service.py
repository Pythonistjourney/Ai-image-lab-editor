from diffusers import StableDiffusionUpscalePipeline
from PIL import Image
from app.services.image_processor import load_image, save_image, resize_image
from app.utils.logger import logger

# Lazy load
_upscaler = None

def get_upscaler():
    global _upscaler
    if _upscaler is None:
        _upscaler = StableDiffusionUpscalePipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler").to("cpu")
    return _upscaler

async def upscale_image(image_path: str, scale: int = 2) -> str:
    try:
        img = load_image(image_path)
        img = resize_image(img, 512)  # Prep
        upscaler = get_upscaler()
        upscaled = upscaler(prompt="high res", image=img).images[0]
        output_path = image_path.replace(".jpg", f"_upscaled_x{scale}.jpg")
        save_image(upscaled, output_path)
        logger.info(f"Upscaled image: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Super resolution error: {e}")
        raise