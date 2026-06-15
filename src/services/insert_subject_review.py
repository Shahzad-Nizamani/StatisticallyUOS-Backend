from sqlalchemy import insert, text
from src.config.db_config import session
from src.db_models.subject_review import SubjectReview
from fastapi import HTTPException

def insert_subject_review(review, dept_id, course_code):
    db_session = session()

    course_exists = db_session.execute(
        text("SELECT 1 FROM COURSE WHERE course_code = :course_code"), {"course_code": course_code}
    ).fetchone()

    if not course_exists:
        raise HTTPException(status_code=400, detail="Invalid course code provided.")
    
    try:
        stmt = insert(SubjectReview).values(
            **review.model_dump(),
            dept_id=dept_id,
            course_code=course_code
        )
        db_session.execute(stmt)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()