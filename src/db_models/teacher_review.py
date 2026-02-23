from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from src.config.db_config import Base

class Teacher_review(Base):
    __tablename__ = "teacher_review"
    __table_args__ = (
        Index('idx_teacherReview_id', 'tid'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False, default='Anonymous')
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 10"), nullable=False)
    review_msg = Column(String(500))
    tid = Column(Integer, ForeignKey("teacher.tid", ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="reviews")