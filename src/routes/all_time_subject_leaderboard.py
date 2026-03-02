from fastapi import APIRouter
from typing import Optional
from src.services.leaderboards import subject_wise_leaderboard

router = APIRouter()

@router.get("/all_time_subject_leaderboard")
def subject_leaderboard(
    dept_id:int,
    course:str,
    surname: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return subject_wise_leaderboard(dept_id=dept_id, course=course, surname=surname, limit=limit, order=order)