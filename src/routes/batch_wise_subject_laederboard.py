from fastapi import APIRouter
from typing import Optional
from src.services.leaderboards import batch_wise_subject_leaderboard

router = APIRouter()

@router.get("/batch_wise_subject_leaderboard/{dept_id}/{batch}/{course}")
def batch_subject_leaderboard(dept_id:int, batch:str, course:str, order:Optional[str]="desc", limit:Optional[int]=10):
    return batch_wise_subject_leaderboard(dept_id, batch, course, order, limit)