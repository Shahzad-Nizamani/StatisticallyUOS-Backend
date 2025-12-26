from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from department import Base

class Course(Base):

    __tablename__ = "course"

    course_code = Column(String, primary_key=True)
    course_name = Column(String, nullable=False)
    did = Column(Integer, ForeignKey("department.did"), nullable=False, index=True)

    results = relationship("Result", back_populates="course")
    department = relationship("Department", back_populates="courses")