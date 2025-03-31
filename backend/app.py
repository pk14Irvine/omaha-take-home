from fastapi import FastAPI, Query, APIRouter
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, List
from sqlmodel import SQLModel

# NOTE: we need to import the models before starting the seed flow
from .dal.models import climate_data, metrics, locations
from .dal.engine import engine

from .routes import climate, locations, metrics, summary, trends
from .seed import create_locations_from_seed, create_metrics_from_seed, create_climate_data_from_seed
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")

"""
Creates new tables and seeds the data

NOTE: only if ENVIRONMENT value is "dev"
"""
def load_db():
    if ENVIRONMENT == "dev":
        print("CREATING TABLES...") 
        SQLModel.metadata.create_all(engine)
        print("SEEDING DATA...")
        create_locations_from_seed()
        create_metrics_from_seed()
        create_climate_data_from_seed()

"""
Drops tables

NOTE: only if ENVIRONMENT value is "dev"
"""
def drop_db():
   if ENVIRONMENT == "dev":
        print("DROPPING TABLES")
        SQLModel.metadata.drop_all(engine)

"""
Lifecycle hook to init DB and seed data

NOTE: async here is important
1. yields control after seeding is done
2. restarts from yield point once server termination is started

More info can be found in the README.md in the root of this folder.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("STARTING SERVER...")
    load_db()
    yield
    drop_db()
    print("TERMINATING SERVER")

# init server and add routes
app = FastAPI(title="EcoVision API", lifespan=lifespan)
app.include_router(climate.router)
app.include_router(locations.router)
app.include_router(metrics.router)
app.include_router(summary.router)
app.include_router(trends.router)

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# base test route
@app.get("/")
async def read_root():
    return {"Hello": "World"}
