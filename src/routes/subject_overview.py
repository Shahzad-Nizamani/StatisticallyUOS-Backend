from fastapi import APIRouter
from src.services.fail_pctg import calc_fail_pctg
from src.services.subject_reviews import fetch_subject_reviews
from src.pydantic_models.subject_review_model import SubjectReview
from src.services.insert_subject_review import insert_subject_review

router = APIRouter()

@router.get("/subject_failpctg/{dept_id}/{course_code}")
def fail_pctg(dept_id: int, course_code: str):
    return calc_fail_pctg(dept_id, course_code)

@router.get("/subject_reviews/{dept_id}/{course_code}")
def subject_reviews(dept_id:int, course_code:str):
    return fetch_subject_reviews(dept_id, course_code)

@router.post("/subject_review/{dept_id}/{course_code}")
def post_subject_review(review:SubjectReview, dept_id:int, course_code:str):
    insert_subject_review(review, dept_id, course_code)
    return "Review posted successfully!"