from fastapi import APIRouter
from typing import Optional
from src.services.leaderboards import cgpa_leaderboard as service_cgpa_leaderboard

router = APIRouter()

@router.get("/cgpa_leaderboard")
def cgpa_leaderboard(
    dept_id: Optional[int] = None,
    surname: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return service_cgpa_leaderboard(dept_id, surname, limit, order)