from fastapi import APIRouter
from src.services.fetch_teachers import fetch_teachers, get_teacher_by_tid
from src.pydantic_models.teacher_review_model import TeacherReview
from src.services.insert_teacher_review import insert_teacher_review
from src.services.fetch_teacher_reviews import fetch_teacher_reviews
from fastapi.requests import Request

router = APIRouter()

@router.get("/teachers")
def get_all_teachers(request: Request):
    return fetch_teachers(request)


@router.get("/single_teacher/{tid}")
def rate_teacher(tid: int, request: Request):
    return get_teacher_by_tid(tid, request)


@router.post("/post_teacher_review/{tid}")
def teacher_review(review:TeacherReview, tid:int):
    insert_teacher_review(review, tid)
    return "Review posted successfully!"

@router.get("/get_teacher_reviews/{tid}")
def get_teacher_reviews(tid:int):
    return fetch_teacher_reviews(tid)