from typing import List
from fastapi import APIRouter
from sqlmodel import Session, select
from dal.models.locations import Locations
from dal.engine import engine

router = APIRouter(tags=["locations"])

@router.get("/api/v1/locations")
def get_locations() -> List[Locations]:
    """
    Retrieve all available locations.
    
    Returns location data in the format specified in the API docs.
    """
    # TODO: Implement this endpoint
    # 1. Query the locations table
    # 2. Format response according to API specification

    with Session(engine) as session:
        locations = session.exec(select(Locations)).all()
        return locations

@router.post("/api/v1/create_location")
def create_location(location: Locations) -> Locations:
    with Session(engine) as session:
        session.add(location)
        session.commit()
        session.refresh(location)
        return location