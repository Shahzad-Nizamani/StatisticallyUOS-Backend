from src.config.db_config import session
from sqlalchemy import text
from src.services.leaderboards import get_course_code
from fastapi import HTTPException

def subject_stats(dept_id, course, year=None):
    db_session = session()
    
    course_codes = get_course_code(db_session, course)
    if not course_codes:
        raise HTTPException(404, detail="Course not found")

    year_filter = "AND r.year = :year" if year else ""
    params_base = {"course_codes": course_codes, "dept_id": dept_id}
    if year:
        params_base["year"] = year

    fail_count = db_session.execute(text(f"""
        SELECT COUNT(*) 
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON r.roll_no = s.roll_no
        WHERE c.course_code IN :course_codes 
        AND s.dept_id = :dept_id
        AND r.grade = 'F'
        {year_filter}
    """), params_base).scalar()

    total_count = db_session.execute(text(f"""
        SELECT COUNT(*) 
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no
        WHERE c.course_code IN :course_codes
        AND s.dept_id = :dept_id
        {year_filter}
    """), params_base).scalar()

    avg_marks = round(db_session.execute(text(f"""
        SELECT AVG(marks)
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no
        WHERE c.course_code IN :course_codes
        AND s.dept_id = :dept_id
        AND marks != 0
        {year_filter}
    """), params_base).scalar())

    grade_row = db_session.execute(text(f"""
        SELECT
            COUNT(*) FILTER (WHERE r.grade LIKE 'A%') as a_count,
            COUNT(*) FILTER (WHERE r.grade LIKE 'B%') as b_count,
            COUNT(*) FILTER (WHERE r.grade LIKE 'C%') as c_count,
            COUNT(*) FILTER (WHERE r.grade LIKE 'D%') as d_count
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no
        WHERE c.course_code IN :course_codes
        AND s.dept_id = :dept_id
        {year_filter}
    """), params_base).fetchone()

    db_session.close()

    a_count, b_count, c_count, d_count = grade_row

    return {
        "total_students": total_count,
        "failed_students": fail_count,
        "fail_percentage": round((fail_count / total_count) * 100, 1),
        "average_marks": avg_marks,
        "grade_percentage": {
            "A": round((a_count / total_count) * 100, 1),
            "B": round((b_count / total_count) * 100, 1),
            "C": round((c_count / total_count) * 100, 1),
            "D": round((d_count / total_count) * 100, 1),
        }
    }