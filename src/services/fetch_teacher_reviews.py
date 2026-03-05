from src.config.db_config import session
from sqlalchemy import text

def fetch_teacher_reviews(tid):
    db_session = session()
    
    try:        
        query = text('SELECT name, rating, review_msg FROM teacher_review WHERE tid = :tid')
        reviews = db_session.execute(query, {"tid":tid})
        
        return [
            {
                "name": row[0],
                "rating": row[1],
                "review_msg": row[2]
            }
            for row in reviews.fetchall()
        ]
    finally:
        db_session.close()