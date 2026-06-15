from fastapi import APIRouter, Query
from typing import Optional, Literal
from src.services.leaderboards import cgpa_leaderboard as service_cgpa_leaderboard

router = APIRouter()

@router.get("/cgpa_leaderboard")
def cgpa_leaderboard(
    dept_id: int = Query(default=None, ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
    batch: Optional[str] = None,
    surname: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    order: Literal["asc", "desc"] = "desc"
): 
    return service_cgpa_leaderboard(dept_id, batch, surname, limit, order)