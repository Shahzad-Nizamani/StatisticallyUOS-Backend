from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from config.db_config import Base

class Department(Base):

    __tablename__ = "department"
    __table_args__ = {'extend_existing': True}

    dname = Column(String, primary_key=True)
    did = Column(Integer)
    
    courses = relationship("Course", back_populates="department")
    students = relationship("Student", back_populates="department")
    results = relationship("Result", back_populates="department")