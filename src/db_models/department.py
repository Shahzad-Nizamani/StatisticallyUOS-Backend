from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from config.db_config import Base

class Department(Base):

    __tablename__ = "department"

    did = Column(Integer, primary_key=True)
    dname = Column(String, nullable=False, unique=True)

    courses = relationship("Course", back_populates="department")
    students = relationship("Student", back_populates="department")