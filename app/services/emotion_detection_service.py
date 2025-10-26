from deepface import DeepFace
from app.services.image_processor import load_image
from app.utils.logger import logger

async def detect_emotion(image_path: str) -> dict:
    try:
        img = load_image(image_path)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        logger.info(f"Detected emotion: {dominant_emotion} in {image_path}")
        return {"emotion": dominant_emotion, "confidence": result[0]['emotion'][dominant_emotion], "all_emotions": result[0]['emotion']}
    except Exception as e:
        logger.error(f"Emotion detection error: {e}")
        raise