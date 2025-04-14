from typing import List, Optional
from fastapi import APIRouter
from sqlalchemy import text
from sqlmodel import Session, select
from ..dal.engine import engine
from ..dal.models.climate_data import ClimateData, ClimateResponseData
from ..dal.models.metrics import Metrics
from ..dal.models.locations import Locations
from pydantic import BaseModel
from ..dal.models.pagination import PaginationWrapper, PaginationMeta

router = APIRouter(tags=["climate"])

QUALITY_WEIGHTS = {
    'excellent': 1.0,
    'good': 0.8,
    'questionable': 0.5,
    'poor': 0.3
}

QUALITY_CODES = ["poor", "questionable", "good", "excellent"]

@router.get("/api/v1/climate")
def get_climate_data(
     location_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        metric: Optional[str] = None,
        quality_threshold: Optional[str] = None,
        page: Optional[int] = 0,
        limit: Optional[int] = 10
    ) -> PaginationWrapper[ClimateResponseData]:
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
    if quality_threshold: quality_threshold = QUALITY_WEIGHTS[quality_threshold]
    skip = page * limit
    with Session(engine) as session:
        query = '''
        select (select count(*) from climatedata), c.id as id, c.location_id as location_id, l.name as location_name, l.latitude as latitude, c.date as date,  m.display_name as metric, c.value as value, m.unit as unit, c.quality as quality
        from climatedata c
        join locations l on c.location_id = l.id
        join metrics m on c.metric_id = m.id
        where
            ( :location_id is Null or :location_id = c.location_id) and
            ( :start_date is NULL or :start_date < c.date) and 
            ( :end_date is NULL or c.date < :end_date) and
            ( :metric is Null or :metric = m.name) and
            ( :quality_threshold is Null or c.quality_weight >= :quality_threshold)
        limit :limit
        offset :skip;
        '''
        resp = session.execute(text(query),{
            'location_id': location_id,
            'start_date': start_date,
            'end_date': end_date,
            'metric': metric,
            'quality_threshold': quality_threshold,
            'limit': limit,
            'skip': skip
        }).fetchall()
        data = [
            ClimateResponseData(
                id=row.id,
                location_id=row.id,
                location_name=row.location_name,
                latitude=row.latitude,
                date=row.date,
                metric=row.metric,
                value=row.value,
                unit=row.unit,
                quality=row.quality
            ) for row in resp
        ]
        meta = PaginationMeta (
            count = resp[0][0],
            page = page,
            per_page = limit
        )
        return PaginationWrapper(
            data = data,
            meta = meta
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
