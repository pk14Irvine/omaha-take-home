from typing import Optional
from sqlmodel import SQLModel, Field


class Metrics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    display_name: str
    unit: str
    description: str
