from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, CheckConstraint
from sqlalchemy.orm import relationship
from config.db_config import Base

class Result(Base):

    __tablename__ = "result"
    __table_args__ = {'extend_existing': True}
    
    roll_no = Column(
        String, 
        ForeignKey("student.roll_no"), 
        primary_key=True,
        index=True
    )
    course_code = Column(
        String, 
        ForeignKey("course.course_code"), 
        primary_key=True,
        index=True
    )
    marks = Column(Integer, default=0)
    grade = Column(
        CHAR(2),
        CheckConstraint("grade IN ('A+', 'A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F')"),
        nullable=False
    )
    dept_name  = Column(String, ForeignKey("department.dname"), nullable=False)
    year = Column(Integer, nullable=False)
    
    student = relationship("Student", back_populates="results")
    course = relationship("Course", back_populates="results")
    department = relationship("Department", back_populates="results")