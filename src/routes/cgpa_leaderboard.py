from fastapi import APIRouter
from typing import Optional
from src.services.leaderboards import cgpa_leaderboard as service_cgpa_leaderboard

router = APIRouter()

@router.get("/cgpa_leaderboard")
def cgpa_leaderboard(
    surname: Optional[str] = None,
    department: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return service_cgpa_leaderboard(surname, department, limit, order)