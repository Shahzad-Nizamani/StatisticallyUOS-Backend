from src.config.db_config import session
from sqlalchemy import text
from src.services.leaderboards import get_course_code

def subject_stats(dept_id, course):
    db_session = session()
    
    course_codes = get_course_code(db_session, course)
    if not course_codes:
        return {"course": course, "department": dept_id, "result": "NO COURSE FOUND"}
    
    fail_query = text("""
        SELECT COUNT(*) 
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON r.roll_no = s.roll_no
        WHERE c.course_code IN :course_codes 
        AND s.dept_id = :dept_id
        AND r.grade = 'F'
    """)

    fail_count = db_session.execute(fail_query, {"course_codes": course_codes, "dept_id": dept_id}).scalar()

    total_query = text("""
        SELECT COUNT(*) 
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no
        WHERE c.course_code IN :course_codes
        AND s.dept_id = :dept_id
    """)

    total_count = db_session.execute(total_query, {"course_codes": course_codes, "dept_id": dept_id}).scalar()

    avg_marks_query = text("""
        SELECT AVG(marks)
        FROM result r 
        JOIN course c ON r.course_code = c.course_code 
        JOIN student s ON s.roll_no = r.roll_no
        WHERE c.course_code IN :course_codes
        AND s.dept_id = :dept_id
        AND marks != 0
    """)

    avg_marks = round(db_session.execute(avg_marks_query, {"course_codes": course_codes, "dept_id": dept_id}).scalar())
    db_session.close()

    stats = {
        "total_students" : total_count,
        "failed_students" : fail_count,
        "fail_percentage": round((fail_count / total_count) * 100, 1),
        "average_marks" : avg_marks
        }


    return stats