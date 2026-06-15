from sqlalchemy import insert, text
from src.config.db_config import session
from src.db_models.teacher_review import TeacherReview
from fastapi import HTTPException

def insert_teacher_review(review, tid):
    db_session = session()

    teachers = db_session.execute(text(
        "SELECT tid FROM teacher")).scalars().all()
    
    if tid not in teachers:
        db_session.close()
        raise HTTPException(status_code=400, detail="Invalid teacher ID provided.")
    try:
        stmt = insert(TeacherReview).values(**review.model_dump(),tid=tid)
        db_session.execute(stmt)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()