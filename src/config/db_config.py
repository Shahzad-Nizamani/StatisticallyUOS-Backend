import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


load_dotenv()  # load variables from .env

DATABASE_URL = os.getenv("database_url")

engine = create_engine(DATABASE_URL)
session = sessionmaker(engine, autoflush=False)