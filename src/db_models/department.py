from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

Base = declarative_base()

class Department(Base):

    __tablename__ = "department"

    did = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    courses = relationship("Course", back_populates="department")
    students = relationship("Student", back_populates="department")