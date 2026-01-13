from sqlalchemy import Column, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from config.db_config import Base

class Student(Base):

    __tablename__ = "student"
    __table_args__ = {'extend_existing': True}

    roll_no = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    surname = Column(String)
    gender = Column(String, CheckConstraint("gender IN('m', 'f')"))
    cgpa = Column(Float)
    percentage = Column(Float)
    dept_name = Column(String, ForeignKey("department.dname"), nullable=False)

    results = relationship("Result", back_populates="student") 
    department = relationship("Department", back_populates="students")