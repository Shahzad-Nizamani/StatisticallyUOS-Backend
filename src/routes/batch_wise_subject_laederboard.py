from fastapi import APIRouter, Query, Path
from typing import Literal
from src.services.leaderboards import batch_wise_subject_leaderboard

router = APIRouter()

@router.get("/batch_wise_subject_leaderboard/{dept_id}/{batch}/{course_code}")
def batch_subject_leaderboard(
      batch:str,
        course_code:str,
         dept_id: int = Path(ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
          order: Literal["asc", "desc"] = "desc",
            limit: int = Query(default=10, ge=1, le=100)):
    
    return batch_wise_subject_leaderboard(dept_id, batch, course_code, order, limit)