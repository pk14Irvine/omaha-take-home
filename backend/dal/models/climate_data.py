from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import VARCHAR, DATE, DOUBLE_PRECISION

class ClimateData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="locations.id", nullable=False)
    metric_id: int = Field(foreign_key="metrics.id", nullable=False)
    date: str = Field(sa_column=DATE)
    value: float
    quality: str
