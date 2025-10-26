from fastapi import FastAPI
from app.routers import (
    auth, core, colorization, style_transfer, emotion_detection, background_removal,
    skin_tone_adjust, ai_presets, super_resolution, object_removal,
    cartoon_stylization, auto_enhancement
)

app = FastAPI(title="AI Image Lab Editor", version="1.0.0", description="Professional AI image editing backend")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(core.router, prefix="/core", tags=["core"])
app.include_router(colorization.router, prefix="/colorize", tags=["colorization"])
app.include_router(style_transfer.router, prefix="/style-transfer", tags=["style-transfer"])
app.include_router(emotion_detection.router, prefix="/emotion-detection", tags=["emotion-detection"])
app.include_router(background_removal.router, prefix="/background-removal", tags=["background-removal"])
app.include_router(skin_tone_adjust.router, prefix="/skin-tone", tags=["skin-tone"])
app.include_router(ai_presets.router, prefix="/ai-presets", tags=["ai-presets"])
app.include_router(super_resolution.router, prefix="/super-resolution", tags=["super-resolution"])
app.include_router(object_removal.router, prefix="/object-removal", tags=["object-removal"])
app.include_router(cartoon_stylization.router, prefix="/cartoon-stylization", tags=["cartoon-stylization"])
app.include_router(auto_enhancement.router, prefix="/auto-enhancement", tags=["auto-enhancement"])

@app.get("/")
async def root():
    return {"message": "AI Image Lab Editor - Ready for pro edits!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)