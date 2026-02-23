from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Teacher(Base):
    __tablename__ = "teacher"
    __table_args__ = (
        Index('idx_teacher_dept_id', 'dept_id'),
        Index('idx_teacher_name', 'name'),
        {'extend_existing': True}
    )
    
    tid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String)
    image_path = Column(String)
    original_image_url = Column(String)
    dept_id = Column(Integer, ForeignKey('department.did'), nullable=False)
    
    department = relationship("Department", back_populates="teachers")
    reviews = relationship("Teacher_review", back_populates="teacher")
