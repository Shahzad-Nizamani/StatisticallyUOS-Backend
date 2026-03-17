from sqlalchemy import text

def get_course_code(db_session, course):
    codes = db_session.execute(
        text("SELECT course_code FROM course WHERE canonical_name = (SELECT canonical_name FROM course WHERE course_name = :course LIMIT 1)"),
        {"course": course}
    ).fetchall()
    return tuple(row[0] for row in codes)