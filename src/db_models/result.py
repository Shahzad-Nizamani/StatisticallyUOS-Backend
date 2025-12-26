from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, CheckConstraint
from sqlalchemy.orm import relationship
from department import Base

class Result(Base):

    __tablename__ = "result"
    
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
    grade = Column(
        CHAR(2),
        CheckConstraint("grade IN ('A+', 'A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F')"),
        nullable=False
    )
    marks = Column(Integer, default=0)
    semester = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    student = relationship("Student", back_populates="results")
    course = relationship("Course", back_populates="results")