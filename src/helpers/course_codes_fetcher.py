from sqlalchemy import text

def get_course_code(db_session, course):
    codes = db_session.execute(text("SELECT course_code FROM COURSE WHERE COURSE_NAME = :course"), {"course": course}).fetchall()
    return tuple([row[0] for row in codes])