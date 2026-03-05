from sqlalchemy import insert
from src.config.db_config import session
from src.db_models.teacher_review import TeacherReview

def insert_teacher_review(review, tid):
    db_session = session()
    try:
        stmt = insert(TeacherReview).values(**review.model_dump(),tid=tid)
        db_session.execute(stmt)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()