from sqlalchemy import Engine
from sqlmodel import create_engine
import os

# Database connection
# DATABASE_URL = f"mysql://{os.environ.get('MYSQL_USER', 'root')}:{os.environ.get('MYSQL_PASSWORD', '')}@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ.get('MYSQL_DB', 'climate_data')}"
# database = databases.Database(DATABASE_URL)

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = 5432
DB = "omaha"

POSTGRES_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine: Engine = create_engine(POSTGRES_URL, echo=True)