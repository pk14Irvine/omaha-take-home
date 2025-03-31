import json
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session, select
from ..dal.engine import engine
from ..dal.models.climate_data import ClimateData
from ..dal.models.locations import Locations
from ..dal.models.metrics import Metrics
from .climate import QUALITY_CODES

router = APIRouter(tags=["summary"])

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
    data: List[ClimateResponseData] #eventually make this a union 
    meta: PaginationMetaResponse

@router.get("/api/v1/summary")
def get_summary(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None
):
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

    query = """
    WITH FilteredData AS (
        SELECT
            c.location_id,
            c.metric_id,
            c.value,
            c.quality,
            m.name AS metric_name,
            m.unit AS metric_unit,
            CASE
                WHEN c.quality = 'excellent' THEN 1.0
                WHEN c.quality = 'good' THEN 0.75
                WHEN c.quality = 'questionable' THEN 0.5
                WHEN c.quality = 'poor' THEN 0.25
                ELSE 0
            END AS quality_weight
        FROM climatedata c
        JOIN metrics m ON c.metric_id = m.id
        WHERE
            (:location_id IS NULL OR c.location_id = :location_id)
            AND (:start_date IS NULL OR c.date >= :start_date)
            AND (:end_date IS NULL OR c.date <= :end_date)
            AND (:metric_name IS NULL OR m.name = :metric_name)
            AND (:quality_threshold IS NULL OR 
                (CASE 
                    WHEN c.quality = 'excellent' THEN 1.0
                    WHEN c.quality = 'good' THEN 0.75
                    WHEN c.quality = 'questionable' THEN 0.5
                    WHEN c.quality = 'poor' THEN 0.25
                    ELSE 0
                END) >=
                CASE 
                    WHEN :quality_threshold = 'excellent' THEN 1.0
                    WHEN :quality_threshold = 'good' THEN 0.75
                    WHEN :quality_threshold = 'questionable' THEN 0.5
                    WHEN :quality_threshold = 'poor' THEN 0.25
                    ELSE 0
                END)
    ),
    MetricStats AS (
        SELECT
            metric_id,
            metric_name,
            metric_unit,
            MIN(value) AS min_value,
            MAX(value) AS max_value,
            AVG(value) AS avg_value,
            SUM(value * quality_weight) / SUM(quality_weight) AS weighted_avg_value,
            SUM(CASE WHEN quality = 'excellent' THEN 1 ELSE 0 END) AS excellent_count,
            SUM(CASE WHEN quality = 'good' THEN 1 ELSE 0 END) AS good_count,
            SUM(CASE WHEN quality = 'questionable' THEN 1 ELSE 0 END) AS questionable_count,
            SUM(CASE WHEN quality = 'poor' THEN 1 ELSE 0 END) AS poor_count
        FROM FilteredData
        GROUP BY metric_id, metric_name, metric_unit
    )
    SELECT
        metric_name,
        min_value,
        max_value,
        avg_value,
        weighted_avg_value,
        metric_unit,
        jsonb_build_object(
            'excellent', excellent_count::float / NULLIF(excellent_count + good_count + questionable_count + poor_count, 0),
            'good', good_count::float / NULLIF(excellent_count + good_count + questionable_count + poor_count, 0),
            'questionable', questionable_count::float / NULLIF(excellent_count + good_count + questionable_count + poor_count, 0),
            'poor', poor_count::float / NULLIF(excellent_count + good_count + questionable_count + poor_count, 0)
        ) AS quality_distribution
    FROM MetricStats;
    """
    with Session(engine) as session:
        # Execute the query with parameters
        result = session.execute(
            text(query),
            {
                "location_id": location_id,
                "start_date": start_date,
                "end_date": end_date,
                "metric_name": metric,
                "quality_threshold": quality_threshold
            }
        )

        # Fetch and process results
        summary = result.fetchall()
        print("summary: ", summary)
        data = {}
        for row in summary:
            metric_name = row.metric_name
            data[metric_name] = {
                "min": row.min_value,
                "max": row.max_value,
                "avg": row.avg_value,
                "weighted_avg": row.weighted_avg_value,
                "unit": row.metric_unit,
                "quality_distribution": row.quality_distribution
            }

        return data