from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from src.config.db_config import Base


class Subject_review(Base):
    __tablename__ = "subject_review"
    __table_args__ = (
        Index('idx_subjetcReview_courseCode', 'course_code'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False, default='Anonymous')
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 10"), nullable=False)
    review_msg = Column(String(500))
    course_code = Column(String(15), ForeignKey("course.course_code", ondelete="CASCADE"))
    dept_id = Column(Integer, ForeignKey("department.did", ondelete="CASCADE"))

    course = relationship("Course", back_populates="reviews")