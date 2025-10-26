import torch
from deoldify import device
from deoldify.device_id import DeviceId
from diffusers import StableDiffusionInpaintPipeline  # For inpainting
from transformers import pipeline  # For CLIP in presets

device.set(device=DeviceId.GPU0 if torch.cuda.is_available() else DeviceId.CPU0)

# Lazy loaders
_colorizer = None
_inpaint_pipe = None
_clip = None

def get_colorizer():
    global _colorizer
    if _colorizer is None:
        from deoldify.visualize import get_image_colorizer
        _colorizer = get_image_colorizer(artistic=True)
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