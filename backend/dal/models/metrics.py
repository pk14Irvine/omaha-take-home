from typing import Optional
from sqlmodel import SQLModel, Field

"""
Metrics data class that correlates to the Metrics Table.

RAW SQL:
CREATE TABLE IF NOT EXISTS METRICS (
	ID SERIAL PRIMARY KEY,
	NAME VARCHAR(255) NOT NULL,
	DISPLAY_NAME VARCHAR(255),
	UNIT VARCHAR(50),
	DESCRIPTION TEXT
);
"""
class Metrics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    display_name: str = Field(index = True)
    unit: str
    description: str
