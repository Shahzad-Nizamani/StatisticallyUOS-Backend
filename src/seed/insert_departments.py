from sqlalchemy.dialects.postgresql import insert
from src.config.db_config import session
from src.db_models.department import Department
from sqlalchemy import delete

def save_dept_toDB(departments):
    additional_depts = [
        {"did": 500, "dname" : "COMPUTER SCIENCE MEDICAL"},
        {"did" : 501, "dname" : "COMPUTER SCIENCE ENGINEERING"}
    ]

    departments.extend(additional_depts)
    db_session = session()
    try:
        
        bulk_insert = (insert(Department).values(departments).on_conflict_do_nothing(index_elements=["did"]))
        db_session.execute(bulk_insert)

        db_session.commit()

    except Exception as e:
        print(f"An error occured while inserting departments; {e}")
        db_session.rollback()
    
    try:
        delete_government_and_cs = (delete(Department).where(Department.dname.ilike("%GOVERNMENT%")))
        db_session.execute(delete_government_and_cs)
        delete_cs = (delete(Department).where(Department.did == 10))
        db_session.execute(delete_cs)
        db_session.commit()
        
    except Exception as e:
        print(f"An error occured while deleting government departments; {e}")

    finally:
        db_session.close()