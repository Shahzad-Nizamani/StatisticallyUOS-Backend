from fastapi import APIRouter, Path
from src.services.fetch_teachers import fetch_teachers_by_dept, get_teacher_by_tid
from src.pydantic_models.teacher_review_model import TeacherReview
from src.services.insert_teacher_review import insert_teacher_review
from src.services.fetch_teacher_reviews import fetch_teacher_reviews
from fastapi.requests import Request
from src.services.delete_and_update_teacher_reviews import update_review, delete_review

router = APIRouter()

@router.get("/teachers/{dept_id}")
def get_teachers_by_dept_id(
    request: Request,
    dept_id: int = Path(ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
    
    ):
    return fetch_teachers_by_dept(dept_id, request)


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

@router.put("/update_teacher_review/{review_id}")
def update_teacher_review(review_id: int, rating: int, review_msg:str):
    return update_review(review_id, rating, review_msg)

@router.delete("/delete_teacher_review/{review_id}")
def delete_teacher_review(review_id:int):
    return delete_review(review_id)