from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Department(Base):

    __tablename__ = "department"
    __table_args__ = {'extend_existing': True}

    did = Column(Integer, primary_key=True)
    dname = Column(String)
    
    students = relationship("Student", back_populates="department")