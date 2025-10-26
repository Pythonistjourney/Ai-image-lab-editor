from fastapi import APIRouter, Depends, UploadFile, File

router = APIRouter()

@router.post("/")
async def transfer_style(file: UploadFile = File(...), style: str = "van_gogh"):
    # TODO: Call service
    return {"message": f"Style transfer with {style} - Placeholder"}