from src.config.db_config import session
from sqlalchemy import text

def fetch_teacher_reviews(tid):
    db_session = session()
    
    try:        
        query = text('SELECT name, rating, review_msg, created_at FROM teacher_review WHERE tid = :tid')
        reviews = db_session.execute(query, {"tid":tid})
        
        return [
            {
                "name": row[0],
                "rating": row[1],
                "review_msg": row[2],
                "created_at": row[3].strftime("%Y-%m-%d") if row[3] else None
            }
            for row in reviews.fetchall()
        ]
    finally:
        db_session.close()