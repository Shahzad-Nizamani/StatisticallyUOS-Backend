import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()  # load variables from .env

DATABASE_URL = os.getenv("database_url")

engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(engine, autoflush=False)

Base = declarative_base()