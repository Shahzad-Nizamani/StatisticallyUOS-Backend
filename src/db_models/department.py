from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

base = declarative_base()

class department(base):

    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    Did = Column(Integer, nullable=False)
    name = Column(String, nullable=False)