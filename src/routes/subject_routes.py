from fastapi import APIRouter
from src.services.fail_pctg import calc_fail_pctg
from src.services.subject_reviews import fetch_subject_reviews

router = APIRouter()

@router.get("/subject_overview/{dept}/{course}")
def rate_subject_and_fail_pctg(dept: int, course: str):
    reviews = fetch_subject_reviews(dept, course)

    return calc_fail_pctg(dept, course), reviews