from fastapi import APIRouter
from src.services.fetch_teachers import get_teachers_by_deptID, get_teacher_by_tid
from src.pydantic_models.teacher_review_model import TeacherReview
from src.services.insert_teacher_review import insert_teacher_review
from src.services.fetch_teacher_reviews import fetch_teacher_reviews

router = APIRouter()

@router.get("/teachers/{dept_id}")
def get_teachers_by_dept(dept_id: int):
    return get_teachers_by_deptID(dept_id)


@router.get("/rate_teacher/{tid}")
def rate_teacher(tid: int):
    return get_teacher_by_tid(tid)


@router.post("/teacher_review/{tid}")
def teacher_review(review:TeacherReview, tid:int):
    insert_teacher_review(review, tid)
    return "Review posted successfully!"

@router.get("/teacher_reviews/{tid}")
def get_teacher_reviews(tid:int):
    return fetch_teacher_reviews(tid)