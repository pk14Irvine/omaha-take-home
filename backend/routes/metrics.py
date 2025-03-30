from typing import List
from fastapi import APIRouter
from sqlmodel import Session, select
from dal.engine import engine
from dal.models.metrics import Metrics

router = APIRouter(tags=["metrics"])

@router.get("/api/v1/metrics")
def get_metrics() -> List[Metrics]:
    """
    Retrieve all available climate metrics.
    
    Returns metric data in the format specified in the API docs.
    """
    # TODO: Implement this endpoint
    # 1. Query the metrics table
    # 2. Format response according to API specification

    with Session(engine) as session:
        return session.exec(select(Metrics)).all()

@router.post("/api/v1/create_metric")
def create_metric(metric: Metrics) -> Metrics:
    with Session(engine) as session:
        session.add(metric)
        session.commit()
        session.refresh(metric)
        return metric