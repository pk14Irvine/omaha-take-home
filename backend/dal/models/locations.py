from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import VARCHAR, DOUBLE_PRECISION

"""
Locations data class that correlates to the LOCATIONS table.

RAW SQL:
CREATE TABLE IF NOT EXISTS LOCATIONS (
	ID SERIAL PRIMARY KEY,
	NAME VARCHAR(255),
	COUNTRY VARCHAR(255),
	LATITUDE DOUBLE PRECISION,
	LONGITUDE DOUBLE PRECISION,
	REGION VARCHAR(255)
);
"""
class Locations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str
    latitude: float
    longitude: float
    region: str
