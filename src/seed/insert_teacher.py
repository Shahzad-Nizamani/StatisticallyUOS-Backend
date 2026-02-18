from src.config.db_config import session
from sqlalchemy.dialects.postgresql import insert
from src.db_models.teacher import Teacher

def insert_teacher_to_db(teachers_list):

    db_session = session()

    try:
        bulk_insert_teachers = insert(Teacher).values(teachers_list).on_conflict_do_nothing()
        db_session.execute(bulk_insert_teachers)

        db_session.commit()

    except Exception as e:
        print(f"Error while inserting teachers into db {e}!!!")
        db_session.rollback()
        raise
    
    finally:
        db_session.close()