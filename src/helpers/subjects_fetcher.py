from sqlalchemy import text
from src.config.db_config import session

def fetch_subjects(dept_id, batch, year):
    db_session = session()

    query = text("""
        SELECT DISTINCT c.* FROM course c 
        JOIN result r ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no 
        WHERE s.roll_no LIKE :batch AND s.dept_id = :dept_id AND r.year = :year AND c.course_name NOT ILIKE '%ELECTIVE%'
    """)
    params = {"batch": f"{batch}%", "dept_id": dept_id, "year": year}

    subjects = db_session.execute(query, params).fetchall()
    db_session.close()

    return {"subjects": [{"course_code": row[0],"course_name": row[1]} for row in subjects]}