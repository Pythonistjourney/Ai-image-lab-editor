from fastapi import FastAPI
from app.routers import auth, core, colorization  # Add others as implemented

app = FastAPI(title="AI Image Lab Editor", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(core.router, prefix="/core", tags=["core"])
app.include_router(colorization.router, prefix="/colorize", tags=["colorization"])

# Placeholder for others
# app.include_router(style_transfer.router, prefix="/style", tags=["style-transfer"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
