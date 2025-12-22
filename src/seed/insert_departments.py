from src.config.db_config import session, engine
from src.db_models.department import department, base

base.metadata.create_all(bind=engine)

def save_dept_toDB(departments):
    db_session = session()

    try:
        for d in departments:
            exists = db_session.query(department).filter_by(Did=d.Did).first()

            if not exists:
                db_session.add(department(**d.model_dump()))

        db_session.commit()

    except Exception as e:
        print(e)
        db_session.rollback()
    finally:
        db_session.close()