import torch
from diffusers import StableDiffusionInpaintPipeline  # For object removal inpainting
from transformers import pipeline  # For CLIP in AI presets

# Lazy loaders
_colorizer = None
_inpaint_pipe = None
_clip = None

def get_colorizer():
    global _colorizer
    if _colorizer is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _colorizer = pipeline(
            "image-to-image",
            model="RichardZhang/colorization-v2",  # HF GAN for B&W → RGB (replaces DeOldify)
            device=device,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
    return _colorizer

def get_inpainter():
    global _inpaint_pipe
    if _inpaint_pipe is None:
        _inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting").to("cpu")
    return _inpaint_pipe

def get_clip():
    global _clip
    if _clip is None:
        _clip = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
    return _clip