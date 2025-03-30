from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import VARCHAR, DOUBLE_PRECISION

class Locations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str
    latitude: float
    longitude: float
    region: str
