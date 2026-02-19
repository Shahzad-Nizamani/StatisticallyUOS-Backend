from sqlalchemy import text
from src.helpers.dept_id_fetcher import get_dept_id
from src.config.db_config import session

def fetch_subjects(department, batch, year):
    db_session = session()
    dept_id = get_dept_id(db_session, department)

    if year:
        query = text("""
            SELECT DISTINCT c.course_name FROM course c 
            JOIN result r ON r.course_code = c.course_code 
            JOIN student s ON s.roll_no = r.roll_no 
            WHERE s.roll_no LIKE :batch AND s.dept_id = :dept_id AND r.year = :year
        """)
        params = {"batch": f"{batch}%", "dept_id": dept_id, "year": year}
    else:
        query = text("""
            SELECT DISTINCT c.course_name FROM course c 
            JOIN result r ON r.course_code = c.course_code 
            JOIN student s ON s.roll_no = r.roll_no 
            WHERE s.roll_no LIKE :batch AND s.dept_id = :dept_id
        """)
        params = {"batch": f"{batch}%", "dept_id": dept_id}

    subjects = db_session.execute(query, params).fetchall()
    db_session.close()

    return {"department": department, "batch": batch, "total": len(subjects), "subjects": [row[0] for row in subjects]}