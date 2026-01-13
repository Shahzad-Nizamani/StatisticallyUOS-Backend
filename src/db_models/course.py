from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db_config import Base

class Course(Base):

    __tablename__ = "course"
    __table_args__ = {'extend_existing': True}

    course_code = Column(String, primary_key=True)
    course_name = Column(String, nullable=False)
    dept_name = Column(String, ForeignKey("department.dname"), nullable=False, index=True)

    results = relationship("Result", back_populates="course")
    department = relationship("Department", back_populates="courses")