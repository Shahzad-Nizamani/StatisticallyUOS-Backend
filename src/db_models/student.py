from sqlalchemy import Column, String, Float, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Student(Base):

    __tablename__ = "student"
    __table_args__ = {'extend_existing': True}

    roll_no = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    surname = Column(String)
    cgpa = Column(Float)
    percentage = Column(Float)
    dept_id = Column(Integer, ForeignKey("department.did", ondelete="CASCADE"), nullable=False)

    results = relationship("Result", back_populates="student") 
    department = relationship("Department", back_populates="students")