from sqlalchemy import insert
from src.config.db_config import session
from src.db_models.subject_review import SubjectReview

def insert_subject_review(review, dept_id, course_code):
    db_session = session()
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