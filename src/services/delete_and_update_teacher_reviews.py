from src.config.db_config import session
from sqlalchemy import text
from fastapi import HTTPException

def update_review(review_id, rating, review_msg):

    db_session = session()
    review = db_session.execute(text("select * from teacher_review where id = :review_id"), {"review_id" :review_id}).fetchone()
    
    if not review:
        db_session.close()
        raise HTTPException(404, detail="Review does not exist")
    else:
        update_query = "UPDATE teacher_review SET rating = :rating, review_msg = :review_msg WHERE id = :review_id"
        db_session.execute(text(update_query), {"rating":rating, "review_msg":review_msg, "review_id" :review_id})

        db_session.commit()
        db_session.close()
        return "Review updated successfully!"
    

def delete_review(review_id):

    db_session = session()
    review = db_session.execute(text("select * from teacher_review where id = :review_id"), {"review_id" :review_id}).fetchone()

    if review:
        delete_query = "DELETE FROM teacher_review WHERE id =:review_id"
        db_session.execute(text(delete_query), {"review_id":review_id})

        db_session.commit()
        db_session.close()

        return "Review deleted successfully!"
    else:
        db_session.close()
        raise HTTPException(404, detail="Review does not exist")