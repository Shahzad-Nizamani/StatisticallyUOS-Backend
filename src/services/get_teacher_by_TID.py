from sqlalchemy import text
from src.config.db_config import session

def get_single_teacher(tid):

    db_session = session()
    teacher = db_session.execute(text("SELECT * FROM TEACHER WHERE tid = :tid"), {"tid":tid}).fetchone()
    db_session.close()
    return dict(teacher._mapping)