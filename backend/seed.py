from typing import List

from sqlalchemy import text
from sqlmodel import Session
from dal.models.locations import Locations
from dal.models.metrics import Metrics
from dal.models.climate_data import ClimateData
from routes.locations import create_location
from routes.metrics import create_metric
from routes.climate import create_climate_data
from dal.engine import engine
import json

SEED_FILE_NAME = "../data/sample_data.json"

with open(SEED_FILE_NAME, 'r') as file:
    data = json.load(file)

locations_seed = data["locations"]
metrics_seed = data["metrics"]
climate_data_seeds = data["climate_data"]

def create_locations_from_seed():
    for location in locations_seed:
        seed_location = Locations(
            name=location["name"],
            country=location["country"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            region=location["region"]
        )
        create_location(seed_location)

def create_metrics_from_seed():
    for metrics in metrics_seed:
        seed_metric = Metrics(
            name=metrics["name"],
            display_name=metrics["display_name"],
            unit=metrics["unit"],
            description=metrics["description"],
        )
        create_metric(seed_metric)

def create_climate_data_from_seed():
    for climate_data_seed in climate_data_seeds:
        climate_data = ClimateData(
            location_id=climate_data_seed["location_id"],
            metric_id=climate_data_seed["metric_id"],
            date=climate_data_seed["date"],
            value=climate_data_seed["value"],
            quality=climate_data_seed["quality"]
        )
        create_climate_data(climate_data)
