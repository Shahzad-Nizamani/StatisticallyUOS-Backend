from fastapi import APIRouter
from src.services.subject_stats import subject_stats
from src.services.fetch_subject_reviews import fetch_subject_reviews
from src.pydantic_models.subject_review_model import SubjectReview
from src.services.insert_subject_review import insert_subject_review

router = APIRouter()

@router.get("/get_subject_stats/{dept_id}/{course_name}")
def get_subject_stats(dept_id: int, course_name: str):
    return subject_stats(dept_id, course_name)

@router.get("/get_subject_reviews/{dept_id}/{course_code}")
def subject_reviews(dept_id:int, course_code:str):
    return fetch_subject_reviews(dept_id, course_code)

@router.post("/post_subject_review/{dept_id}/{course_code}")
def post_subject_review(review:SubjectReview, dept_id:int, course_code:str):
    insert_subject_review(review, dept_id, course_code)
    return "Review posted successfully!"