from sqlalchemy import text
from src.config.db_config import session
from src.helpers.course_codes_fetcher import get_course_code

def cgpa_leaderboard(dept_id, surname, limit, order):
    db_session = session()
    
    
    sort = "ASC" if order == "asc" else "DESC"

    if surname and dept_id:
        surname = surname.upper()

        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT WHERE DEPT_ID = :dept_id AND SURNAME = :surname ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "surname": surname, "limit": limit}
        ).fetchall()
    elif dept_id:
        leaderboard = db_session.execute(
            text(f"SELECT * FROM STUDENT WHERE DEPT_ID = :dept_id ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "limit": limit}
        ).fetchall()
    elif surname:
        surname = surname.upper()
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


def subject_wise_leaderboard(course, dept_id, surname, limit, order):
    db_session = session()
    course_codes = get_course_code(db_session,course)
      
    sort = "ASC" if order == "asc" else "DESC"

    base = "SELECT s.roll_no, s.name, s.fname, s.surname, r.marks, r.grade FROM STUDENT s JOIN RESULT r ON s.roll_no = r.roll_no WHERE s.dept_id = :dept_id AND r.course_code in :course_codes"

    if surname:
        surname = surname.upper()

        leaderboard = db_session.execute(
            text(f"{base} AND s.SURNAME = :surname ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "course_codes": course_codes, "surname":surname, "limit": limit}
        ).fetchall()
    else:
        leaderboard = db_session.execute(
            text(f"{base} ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id":dept_id, "course_codes": course_codes, "limit": limit}
        ).fetchall()

    db_session.close()
    return [dict(row._mapping) for row in leaderboard]

def batch_wise_subject_leaderboard(dept_id, batch, course, order, limit):
    db_session = session()
    sort = "ASC" if order == "asc" else "DESC"

    query = text(f"""
        SELECT s.roll_no, s.name, s.fname, s.surname, r.marks, r.grade 
        FROM student s 
        JOIN result r ON s.roll_no = r.roll_no 
        WHERE s.dept_id = :dept_id 
        AND s.roll_no LIKE :batch 
        AND r.course_code = :course_code
        ORDER BY r.marks {sort} NULLS LAST LIMIT :limit
    """)
    
    leaderboard = db_session.execute(
        query, 
        {
            "dept_id": dept_id, 
            "batch": f"{batch}%",
            "course_code": course,
            "limit":limit
        }
    ).fetchall()

    db_session.close()

    return [dict(row._mapping) for row in leaderboard]