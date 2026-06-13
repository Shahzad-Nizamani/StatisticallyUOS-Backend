from sqlalchemy import text
from src.config.db_config import session
from src.helpers.course_codes_fetcher import get_course_code

def cgpa_leaderboard(dept_id, batch, surname, limit, order):
    db_session = session()
    
    sort = "ASC" if order == "asc" else "DESC"

    conditions = []
    params = {"limit": limit}

    if dept_id:
        conditions.append("DEPT_ID = :dept_id")
        params["dept_id"] = dept_id

    if batch:
        conditions.append("roll_no LIKE :batch")
        params["batch"] = f"{batch}%"

    if surname:
        conditions.append("SURNAME = :surname")
        params["surname"] = surname.upper()

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    leaderboard = db_session.execute(
        text(f"SELECT * FROM STUDENT {where_clause} ORDER BY CGPA {sort} NULLS LAST LIMIT :limit"),
        params
    ).fetchall()

    db_session.close()
    return [dict(row._mapping) for row in leaderboard]

def subject_wise_leaderboard(course, dept_id, surname, limit, order):
    db_session = session()
    course_codes = get_course_code(db_session, course)
    print(f"Course codes for '{course}': {course_codes}")

    if not course_codes:
        db_session.close()
        return []

    sort = "ASC" if order == "asc" else "DESC"
    placeholders = ", ".join(f"'{code}'" for code in course_codes)
    base = f"SELECT s.roll_no, s.name, s.fname, s.surname, r.marks, r.grade FROM STUDENT s JOIN RESULT r ON s.roll_no = r.roll_no WHERE s.dept_id = :dept_id AND r.course_code IN ({placeholders})"

    if surname:
        surname = surname.upper()
        leaderboard = db_session.execute(
            text(f"{base} AND s.SURNAME = :surname ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "surname": surname, "limit": limit}
        ).fetchall()
    else:
        leaderboard = db_session.execute(
            text(f"{base} ORDER BY r.MARKS {sort} NULLS LAST LIMIT :limit"),
            {"dept_id": dept_id, "limit": limit}
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