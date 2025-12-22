from scraper.scrap_dept import get_departments
from config.db_config import session, engine
from db_models import department

department.base.metadata.create_all(bind=engine)

def add_all_departments():
    db_session = session()

    try:
        departments = get_departments()

        for d in departments:
            db_session.add(d)

        db_session.commit()

    except Exception as e:
        print(e)
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    add_all_departments()