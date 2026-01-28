from config.db_config import session
from sqlalchemy.dialects.postgresql import insert
from src.db_models.course import Course
from src.db_models.student import Student
from src.db_models.result import Result

def insert_all_to_db(students, courses, results):
    db_session = session()

    try:
        bulk_insert_students = insert(Student).values(students).on_conflict_do_nothing(index_elements=["roll_no"])
        db_session.execute(bulk_insert_students)

        if courses and any(c.get('course_code') for c in courses):
            bulk_insert_courses = insert(Course).values(courses)
            bulk_insert_courses = bulk_insert_courses.on_conflict_do_nothing(
        index_elements=['course_code']
    )
            db_session.execute(bulk_insert_courses) 

        bulk_insert_results = insert(Result).values(results).on_conflict_do_nothing(index_elements=["roll_no", "course_code"])
        db_session.execute(bulk_insert_results) 

        db_session.commit()
        print(f"Successfully processed {len(students)} students, {len(courses)} courses, {len(results)} results")

    except Exception as e:
        print(f"Error while inserting all: {e}")
        db_session.rollback()
        raise

    finally:
        db_session.close()