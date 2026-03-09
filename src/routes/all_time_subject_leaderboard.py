from fastapi import APIRouter
from typing import Optional
from src.services.leaderboards import subject_wise_leaderboard

router = APIRouter()

@router.get("/all_time_subject_leaderboard/{dept_id}/{course_name}")
def subject_leaderboard(
    dept_id:int,
    course_name:str,
    surname: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return subject_wise_leaderboard(dept_id=dept_id, course=course_name, surname=surname, limit=limit, order=order)