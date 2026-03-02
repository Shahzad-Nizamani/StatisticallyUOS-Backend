from sqlalchemy import text
from src.config.db_config import session

def get_teacher_by_tid(tid):

    db_session = session()
    teacher = db_session.execute(text("SELECT * FROM TEACHER WHERE tid = :tid"), {"tid":tid}).fetchone()
    db_session.close()
    return dict(teacher._mapping)

def get_teachers_by_deptID(dept_id):
    db_session = session()
    result = db_session.execute(text("SELECT * FROM teacher WHERE dept_id = :dept_id"), {"dept_id": dept_id})
    teachers = result.fetchall()
    return {"teachers": [dict(row._mapping) for row in teachers]}