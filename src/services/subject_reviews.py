from src.config.db_config import session
from sqlalchemy import text
from src.helpers.dept_id_fetcher import get_dept_id

def fetch_subject_reviews(dept_id, course):
    db_session = session()
    
    try:        
        query = text('SELECT name, rating, review_msg FROM subject_review WHERE course_code = :course AND dept_id = :dept_id')
        reviews = db_session.execute(query, {"course": course, "dept_id": dept_id})
        
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