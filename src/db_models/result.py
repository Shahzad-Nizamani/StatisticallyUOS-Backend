from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, CheckConstraint
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Result(Base):
    __tablename__ = "result"
    __table_args__ = {'extend_existing': True}

    roll_no = Column(String, ForeignKey("student.roll_no", ondelete="CASCADE"), primary_key=True, index=True)
    course_code = Column(String, ForeignKey("course.course_code", ondelete="CASCADE"), primary_key=True, index=True)
    marks = Column(Integer, default=0)
    grade = Column(CHAR(2), CheckConstraint("grade IN ('A+', 'A', 'B', 'B+', 'C', 'C+', 'D', 'D+', 'F')"))
    year = Column(Integer, nullable=False)
    
    student = relationship("Student", back_populates="results")
    course = relationship("Course", back_populates="results")