import sys
sys.path.append('src')

from src.db_models.department import Department
from src.db_models.student import Student
from src.db_models.course import Course
from src.db_models.result import Result
from src.db_models.teacher import Teacher
from src.config.db_config import Base, engine

def create_tables():
    print("===creating tables===")

    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created!")
    except Exception as e:
        print(f"Error while creating tables {e}.")