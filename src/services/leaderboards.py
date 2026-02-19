from sqlalchemy import text
from src.config.db_config import session
from src.helpers.dept_id_fetcher import get_dept_id
from src.helpers.course_codes_fetcher import get_course_code

def cgpa_leaderboard(surname, department, limit, order):
    db_session = session()
    dept_id = get_dept_id(db_session,department)
    sort = "ASC" if order == "asc" else "DESC"

    if surname and department:
        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT WHERE DEPT_ID = :dept_id AND SURNAME = :surname ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "surname": surname, "limit": limit}
        ).fetchall()
    elif department:
        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT WHERE DEPT_ID = :dept_id ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "limit": limit}
        ).fetchall()
    elif surname:
        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT WHERE SURNAME = :surname ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"surname": surname, "limit": limit}
        ).fetchall()
    else:
        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"limit": limit}
        ).fetchall()

    db_session.close()
    return [dict(row._mapping) for row in leaderboard]


def subject_wise_leaderboard(course, surname, department, limit, order):
    db_session = session()
    dept_id = get_dept_id(db_session,department)
    course_code = get_course_code(db_session,course)

    sort = "ASC" if order == "asc" else "DESC"

    base = "SELECT s.roll_no, s.name, s.surname, r.marks, r.grade FROM STUDENT s JOIN RESULT r ON s.roll_no = r.roll_no WHERE s.dept_id = :dept_id AND r.course_code in :course_code"

    if surname:
        leaderboard = db_session.execute(
            text(f"{base} AND s.SURNAME = :surname ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id":dept_id, "course_code": course_code, "surname": surname, "limit": limit}
        ).fetchall()
    else:
        leaderboard = db_session.execute(
            text(f"{base} ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id":dept_id, "course_code": course_code, "limit": limit}
        ).fetchall()

    db_session.close()
    return [dict(row._mapping) for row in leaderboard]