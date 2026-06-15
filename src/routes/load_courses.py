from src.helpers.subjects_fetcher import fetch_subjects
from fastapi import APIRouter, Path

router = APIRouter()

@router.get("/fetch_subjects/{dept_id}/{batch}/{part}")
def get_subjects(
    batch:str,
    part:int = Path(ge=1, le=4),
    dept_id: int = Path(ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
    ):
    return fetch_subjects(dept_id, batch, part)