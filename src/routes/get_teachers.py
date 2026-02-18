from fastapi import FastAPI
from typing import Optional
from src.services.get_teachers_by_deptID import get_teachers
from src.services.get_teacher_by_TID import get_single_teacher
from src.services.leaderboards import cgpa_leaderboard as service_cgpa_leaderboard
from src.services.leaderboards import subject_wise_leaderboard

app = FastAPI()

@app.get("/cgpa_leaderboard")
def cgpa_leaderboard(
    surname: Optional[str] = None,
    department: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return service_cgpa_leaderboard(surname, department, limit, order)

@app.get("/subject_leaderboard")
def subject_leaderboard(
    department:str,
    course:str,
    surname: Optional[str] = None,
    limit: Optional[int] = 10,
    order: Optional[str] = "desc"
):
    return subject_wise_leaderboard(department=department, course=course, surname=surname, limit=limit, order=order)

@app.get("/teachers/{dept_id}")
def get_teachers_by_deptID(dept_id: int):
    return get_teachers(dept_id)

@app.get("/rate_teacher/{tid}")
def rate_teacher(tid: int):
    return get_single_teacher(tid)