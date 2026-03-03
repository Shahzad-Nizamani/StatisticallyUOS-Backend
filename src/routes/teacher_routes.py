from fastapi import APIRouter
from src.services.fetch_teachers import get_teachers_by_deptID, get_teacher_by_tid

router = APIRouter()

@router.get("/rate_teacher/{tid}")
def rate_teacher(tid: int):
    return get_teacher_by_tid(tid)

@router.get("/teachers/{dept_id}")
def get_teachers_by_deptID(dept_id: int):
    return get_teachers_by_deptID(dept_id)