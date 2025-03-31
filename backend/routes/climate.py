from typing import List, Optional
from fastapi import APIRouter
from sqlmodel import Session, select
from ..dal.engine import engine
from ..dal.models.climate_data import ClimateData
from ..dal.models.metrics import Metrics
from ..dal.models.locations import Locations
from pydantic import BaseModel

router = APIRouter(tags=["climate"])

"""
Pagination Meta Data Response

TODO: PULL OUT INTO MODELS
"""
class ClimateResponseData(BaseModel):
    id: int
    location_id: int
    location_name: str
    latitude: float
    longitude: float
    date: str
    metric: str
    value: float
    unit: str
    quality: str

"""
Pagination Meta Data Response

TODO: PULL OUT INTO MODELS
"""
class PaginationMetaResponse(BaseModel):
    total_count: int
    page: int
    per_page: int

"""
Paginated Data Response - Meant to be a generic wrapper for reusability

TODO: PULL OUT INTO MODELS
"""
class PaginatedDataResponse(BaseModel):
    data: List[ClimateResponseData]
    meta: PaginationMetaResponse

QUALITY_CODES = ["poor", "questionable", "good", "excellent"]

@router.get("/api/v1/climate")
def get_climate_data(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None
    ) -> PaginatedDataResponse:
    """
    Retrieve climate data with optional filtering.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns climate data in the format specified in the API docs.
    """
    # Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. Build and execute SQL query with proper JOINs and filtering
    # 4. Apply quality threshold filtering
    # 5. Format response according to API specification

    query = select(
        ClimateData.id,
        Locations.id,
        Locations.name,
        Locations.latitude,
        Locations.longitude,
        ClimateData.date,
        Metrics.name.label("metric_name"),
        ClimateData.value,
        Metrics.unit,
        ClimateData.quality
    ) \
        .join(Locations, ClimateData.location_id == Locations.id) \
        .join(Metrics, ClimateData.metric_id == Metrics.id)
    

    if location_id:
        query = query.where(ClimateData.location_id == location_id)

    if start_date:
        query = query.where(ClimateData.date >= start_date) 
    
    if end_date:
        query = query.where(ClimateData.date <= end_date)

    if metric:
        metric = metric.lower() # Convert to lower 
        query = query.where(Metrics.name == metric)

    if quality_threshold:
        quality_threshold = quality_threshold.lower() # Convert to lower 
        qualityIndex = QUALITY_CODES.index(quality_threshold)
        query = query.where(ClimateData.quality.in_(QUALITY_CODES[qualityIndex:]))

    with Session(engine) as session:
        rows = session.exec(query).all()
        data = []
        for row in rows:
            data.append(ClimateResponseData(
                id=row.id,
                location_id=row.id,
                location_name=row.name,
                latitude=row.latitude,
                longitude=row.longitude,
                date=row.date,
                metric=row.metric_name,
                value=row.value,
                unit=row.unit,
                quality=row.quality
            ))

        return PaginatedDataResponse(
            data=data,
            meta=PaginationMetaResponse(
                total_count=len(data),
                page=1,
                per_page=50
            )
        )

@router.post("/api/v1/create_climate")
def create_climate_data(climate: ClimateData) -> ClimateData:
    """
    Create Climate Data entry. Also used in seeding flow.

    Returns created climate data entry. 
    """
    with Session(engine) as session:
        session.add(climate)        
        session.commit()
        session.refresh(climate)
        return climate
