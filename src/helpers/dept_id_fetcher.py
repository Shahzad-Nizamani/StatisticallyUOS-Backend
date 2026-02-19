from sqlalchemy import text

def get_dept_id(db_session, department):
    result = db_session.execute(text("SELECT did FROM DEPARTMENT WHERE DNAME = :department"), {"department": department}).fetchone()
    return result[0] if result else None