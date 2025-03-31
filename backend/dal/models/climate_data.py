from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import VARCHAR, DATE, DOUBLE_PRECISION

"""
Climate data class that correlates to CLIMATEDATA table.

RAW SQL:
CREATE TABLE IF NOT EXISTS CLIMATEDATA (
	ID SERIAL PRIMARY KEY,
	LOCATION_ID INTEGER NOT NULL REFERENCES LOCATIONS (ID),
	METRIC_ID INTEGER NOT NULL REFERENCES METRICS (ID),
	DATE DATE NOT NULL,
	VALUE DOUBLE PRECISION,
	QUALITY VARCHAR(50)
);
"""
class ClimateData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="locations.id", nullable=False)
    metric_id: int = Field(foreign_key="metrics.id", nullable=False)
    date: str = Field(sa_column=DATE)
    value: float
    quality: str
