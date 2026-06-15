from fastapi import APIRouter, Query, Path
from typing import Optional, Literal
from src.services.leaderboards import subject_wise_leaderboard

router = APIRouter()

@router.get("/all_time_subject_leaderboard/{dept_id}/{course_name}")
def subject_leaderboard(
    course_name: str,
    dept_id: int = Path(ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
    surname: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    order: Literal["asc", "desc"] = "desc"
):
    return subject_wise_leaderboard(dept_id=dept_id, course=course_name, surname=surname, limit=limit, order=order)