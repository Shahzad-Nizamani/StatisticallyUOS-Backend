from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Course(Base):

    __tablename__ = "course"
    __table_args__ = {'extend_existing': True}

    course_code = Column(String, primary_key=True)
    course_name = Column(String)

    results = relationship("Result", back_populates="course")