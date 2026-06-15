from fastapi import HTTPException

from src.config.db_config import session
from sqlalchemy import text

def fetch_teacher_reviews(tid):
    db_session = session()

    teacher_exists = db_session.execute(
        text("SELECT 1 FROM teacher WHERE tid = :tid"), {"tid": tid}
    ).fetchone()

    if not teacher_exists:
        raise HTTPException(404, detail="Teacher not found")

    try:        
        query = text('''
    SELECT
        id,
        name, 
        rating, 
        review_msg, 
        created_at,
        AVG(rating) OVER () as avg_rating,
        COUNT(*) FILTER (WHERE rating = 1) OVER () as one_rating_count,
        COUNT(*) FILTER (WHERE rating = 5) OVER () as five_rating_count
    FROM teacher_review 
    WHERE tid = :tid AND is_deleted = FALSE
''')
        reviews = db_session.execute(query, {"tid": tid})
        rows = reviews.fetchall()

        return {
            "avg_rating": round(float(rows[0][5]), 1) if rows else 0,
            "one_rating_count": rows[0][6] if rows else 0,
            "five_rating_count": rows[0][7] if rows else 0,
            "reviews": [
                {
                    "id": row[0],
                    "name": row[1],
                    "rating": row[2],
                    "review_msg": row[3],
                    "created_at": row[4].strftime("%Y-%m-%d") if row[4] else None
                }
                for row in rows
            ]
        }
    finally:
        db_session.close()