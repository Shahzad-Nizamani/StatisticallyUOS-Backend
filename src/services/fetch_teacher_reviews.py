from src.config.db_config import session
from sqlalchemy import text

def fetch_teacher_reviews(tid):
    db_session = session()
    
    try:        
        query = text('''
            SELECT 
                name, 
                rating, 
                review_msg, 
                created_at,
                AVG(rating) OVER () as avg_rating,
                COUNT(*) FILTER (WHERE rating = 1) OVER () as zero_rating_count,
                COUNT(*) FILTER (WHERE rating = 5) OVER () as five_rating_count
            FROM teacher_review 
            WHERE tid = :tid
        ''')
        reviews = db_session.execute(query, {"tid": tid})
        rows = reviews.fetchall()

        return {
            "avg_rating": round(float(rows[0][4]), 1) if rows else 0,
            "zero_rating_count": rows[0][5] if rows else 0,
            "five_rating_count": rows[0][6] if rows else 0,
            "reviews": [
                {
                    "name": row[0],
                    "rating": row[1],
                    "review_msg": row[2],
                    "created_at": row[3].strftime("%Y-%m-%d") if row[3] else None
                }
                for row in rows
            ]
        }
    finally:
        db_session.close()