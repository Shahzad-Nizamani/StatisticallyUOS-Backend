from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "teachers"

@router.get("/teacher_image/file/{filename}")
def get_teacher_image(filename: str):
    image_path = BASE_DIR / filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)