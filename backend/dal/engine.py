from sqlalchemy import Engine
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")

POSTGRES_URL = f"postgresql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine: Engine = create_engine(POSTGRES_URL, echo=True)