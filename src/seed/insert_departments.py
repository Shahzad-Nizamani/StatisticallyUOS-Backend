from sqlalchemy.dialects.postgresql import insert
from src.config.db_config import session
from src.db_models.department import department

def save_dept_toDB(departments):
    db_session = session()
    try:
        
        bulk_insert = (insert(department).values(departments).on_conflict_do_nothing(index_elements=["id"]))
        db_session.execute(bulk_insert)
        db_session.commit()

    except Exception as e:
        print(e)
        db_session.rollback()
    finally:
        db_session.close()