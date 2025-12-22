from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float

base = declarative_base()

class Student(base):

    __tablename__ = "student"

    id = Column(Integer)
    rollno = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    cgpa = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)