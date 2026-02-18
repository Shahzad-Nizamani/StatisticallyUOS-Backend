from sqlalchemy import text
from src.config.db_config import session

def get_teachers(dept_id):
    db_session = session()
    result = db_session.execute(text("SELECT * FROM teacher WHERE dept_id = :dept_id"), {"dept_id": dept_id})
    teachers = result.fetchall()
    return {"teachers": [dict(row._mapping) for row in teachers]}