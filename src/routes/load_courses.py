from src.helpers.subjects_fetcher import fetch_subjects
from fastapi import APIRouter

router = APIRouter()

@router.get("/fetch_subjects/{dept_id}/{batch}/{part}")
def get_subjects(
    dept_id:int,
    batch:str,
    part:int
    ):
    return fetch_subjects(dept_id, batch, part)