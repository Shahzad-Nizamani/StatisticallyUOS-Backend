from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.requests import Request

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "teachers"

@router.get("/teacher_images/all")
def get_all_teacher_images(request: Request):
    all_files = list(BASE_DIR.glob("*.jpg"))

    if not all_files:
        raise HTTPException(status_code=404, detail="No teacher images found")

    return {
        "total": len(all_files),
        "teachers": [
            {"filename": f.name, "url": str(request.url_for("get_teacher_image", filename=f.name))}
            for f in all_files
        ]
    }

@router.get("/teacher_image/file/{filename}")
def get_teacher_image(filename: str):
    image_path = BASE_DIR / filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)