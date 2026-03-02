from src.helpers.subjects_fetcher import fetch_subjects
from fastapi import APIRouter

router = APIRouter()

@router.get("/fetch_subjects/{dept_id}/{batch}/{year}")
def get_subjects(
    dept_id:int,
    batch:str,
    year:int
    ):
    return fetch_subjects(dept_id, batch, year)