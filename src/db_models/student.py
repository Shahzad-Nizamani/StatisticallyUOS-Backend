from sqlalchemy import Column, String, Float, CheckConstraint
from sqlalchemy.orm import relationship
from department import Base

class Student(Base):

    __tablename__ = "student"

    roll_no = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    surname = Column(String)
    gender = Column(String, CheckConstraint("gender IN('m', 'f')"), nullable=True)
    cgpa = Column(Float)
    percentage = Column(Float)

    results = relationship("Result", back_populates="student") 