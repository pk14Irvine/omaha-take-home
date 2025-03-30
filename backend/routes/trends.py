from typing import Optional
from fastapi import APIRouter
from sqlalchemy import text
from sqlmodel import Session
import pandas as pd
import numpy as np
from scipy import stats
from dal.engine import engine

router = APIRouter(tags=["trends"])

@router.get("/api/v1/trends")
def get_trends(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None
):
    """
    Analyze trends and patterns in climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns trend analysis including direction, rate of change, anomalies, and seasonality.
    """
    # TODO: Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. For each metric:
    #    - Calculate trend direction and rate of change
    #    - Identify anomalies (values > 2 standard deviations)
    #    - Detect seasonal patterns if sufficient data
    #    - Calculate confidence scores
    # 4. Format response according to API specification

    # Query the climate data from the database
    query = """
    SELECT c.date, c.value, m.name AS metric_name, c.quality
    FROM climatedata c
    JOIN metrics m ON c.metric_id = m.id
    WHERE (:location_id IS NULL OR c.location_id = :location_id)
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
    """

    with Session(engine) as session:
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

        data = result.fetchall()

        # Process the data into a DataFrame for easier analysis
        df = pd.DataFrame(data, columns=['date', 'value', 'metric_name', 'quality'])
        df['date'] = pd.to_datetime(df['date'])

        # Analyze trends and calculate rate of change using linear regression
        trend_results = {}
        for metric_name, group in df.groupby('metric_name'):
            # Perform linear regression (slope gives the rate of change)
            x = np.array([i for i in range(len(group))])
            y = group['value'].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            trend_results[metric_name] = {
                'trend_direction': 'increasing' if slope > 0 else 'decreasing',
                'rate_of_change': slope,
                'r_squared': r_value**2
            }

            # Detect anomalies (values > 2 standard deviations from the mean)
            mean = np.mean(group['value'])
            std_dev = np.std(group['value'])
            anomalies = group[group['value'] > (mean + 2 * std_dev)]

            trend_results[metric_name]['anomalies'] = anomalies[['date', 'value']].to_dict(orient='records')

            # Optionally, we can also detect seasonality by checking for periodic trends
            # For simplicity, we assume monthly seasonality and group by month
            group['month'] = group['date'].dt.month
            seasonality = group.groupby('month')['value'].mean()

            trend_results[metric_name]['seasonality'] = seasonality.to_dict()

        return trend_results