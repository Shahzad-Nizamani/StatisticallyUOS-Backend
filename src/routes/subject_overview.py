from fastapi import APIRouter, Query, Path
from src.services.subject_stats import subject_stats
from src.services.fetch_subject_reviews import fetch_subject_reviews
from src.pydantic_models.subject_review_model import SubjectReview
from src.services.insert_subject_review import insert_subject_review
from src.services.delete_and_update_subject_reviews import update_review, delete_review

router = APIRouter()

@router.get("/get_subject_stats/{dept_id}/{course_name}")
def get_subject_stats(
    course_name: str,
    dept_id: int = Path(ge=1, le=501, description="Departments only exist between 1 and 501. Please provide a valid department ID."),
    year:int = Query(default=None, ge=2004, le=2025, description="Please provide a valid year between 2004 and 2025.")):

    return subject_stats(dept_id, course_name, year)

@router.get("/get_subject_reviews/{dept_id}/{course_code}")
def subject_reviews(dept_id:int, course_code:str):
    return fetch_subject_reviews(dept_id, course_code)

@router.post("/post_subject_review/{dept_id}/{course_code}")
def post_subject_review(review:SubjectReview, dept_id:int, course_code:str):
    insert_subject_review(review, dept_id, course_code)
    return "Review posted successfully!"

@router.put("/update_subject_review/{review_id}")
def update_subject_review(review_id: int, rating: int, review_msg:str):
    return update_review(review_id, rating, review_msg)

@router.delete("/delete_subject_review/{review_id}")
def delete_subject_review(review_id:int):
    return delete_review(review_id)