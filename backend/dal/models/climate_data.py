from typing import Optional
from pydantic import BaseModel
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
    location_id: int = Field(foreign_key="locations.id", nullable=False, index = True)
    metric_id: int = Field(foreign_key="metrics.id", nullable=False, index = True)
    date: str = Field(index = True)
    value: float
    quality: str
    quality_weight: float = Field(index = True)


class ClimateResponseData(BaseModel):
    id: int
    location_id: int
    location_name: str
    latitude: float
    date: str
    metric: str
    value: float
    unit: str
    quality: str

class Distributions(BaseModel):
    poor: float
    questionable: float
    good: float
    excellent: float

class ClimateSummary(BaseModel):
    name: str
    min: float
    max: float
    avg: float
    weighted_avg: float
    unit: str
    quality_distributions: Distributions