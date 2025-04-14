import json
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session, select
from ..dal.engine import engine
from ..dal.models.climate_data import ClimateSummary, Distributions
from ..dal.models.pagination import PaginationWrapper, PaginationMeta
from ..dal.models.locations import Locations
from ..dal.models.metrics import Metrics
from .climate import QUALITY_CODES

router = APIRouter(tags=["summary"])

QUALITY_WEIGHTS = {
    'excellent': 1.0,
    'good': 0.8,
    'questionable': 0.5,
    'poor': 0.3
}

@router.get("/api/v1/summary")
def get_summary(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None,
    page: Optional[int] = 0,
    limit: Optional[int] = 10
) -> PaginationWrapper[ClimateSummary]:
    """
    Retrieve quality-weighted summary statistics for climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns weighted min, max, and avg values for each metric in the format specified in the API docs.
    """
    # Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. Get list of metrics to summarize
    # 4. For each metric:
    #    - Calculate quality-weighted statistics using QUALITY_WEIGHTS
    #    - Calculate quality distribution
    #    - Apply proper filtering
    # 5. Format response according to API specification
    if quality_threshold: quality_threshold = QUALITY_WEIGHTS[quality_threshold]
    skip = page * limit
    query = """
    select
            (select count(*) from climatedata),
            m.name, m.unit, min(c.value),
            max(c.value), avg(c.value),
            avg(c.value * c.quality_weight) as weighted_avg,
            sum(case when c.quality = 'poor' then 1 else 0 end) as poor,
            sum(case when c.quality = 'questionable' then 1 else 0 end) as questionable,
            sum(case when c.quality = 'good' then 1 else 0 end) as good,
            sum(case when c.quality = 'excellent' then 1 else 0 end) as excellent,
            count(m.id) as total
        from climatedata c
        join locations l on c.location_id = l.id
        join metrics m on c.metric_id = m.id
        where
            ( :location_id is Null or :location_id = c.location_id) and
            ( :start_date is NULL or :start_date < c.date) and 
            ( :end_date is NULL or c.date < :end_date) and
            ( :metric is Null or :metric = m.name) and
            ( :quality_threshold is Null or c.quality_weight >= :quality_threshold)
        group by
            m.id
        limit :limit
        offset :skip;
    """
    with Session(engine) as session:
        # Execute the query with parameters
        result = session.execute(
            text(query),
            {
                "location_id": location_id,
                "start_date": start_date,
                "end_date": end_date,
                "metric": metric,
                "quality_threshold": quality_threshold,
                "limit": limit,
                "skip": skip
            }
        )

        # Fetch and process results
        response = result.fetchall()
        data = []
        for row in response:
            dist = Distributions(
                poor = row.poor / row.total,
                questionable = row.questionable / row.total,
                good = row.good / row.total,
                excellent = row.excellent / row.total
            )
            data.append(
                ClimateSummary(
                    name = row.name,
                    min = row.min,
                    max = row.max,
                    avg = row.avg,
                    weighted_avg = row.weighted_avg,
                    unit = row.unit,
                    quality_distributions = dist
                )
            )
        meta = PaginationMeta (
            count = response[0][0],
            page = page,
            per_page = limit
        )
        return PaginationWrapper(
            data = data,
            meta = meta
        )