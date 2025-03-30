from fastapi import FastAPI, Query, APIRouter
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, List
from sqlmodel import SQLModel
from .dal.models import climate_data, metrics, locations
from .dal.engine import engine
from .routes import climate, locations, metrics, summary, trends
from .seed import create_locations_from_seed, create_metrics_from_seed, create_climate_data_from_seed
from dotenv import load_dotenv
import os

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")

def load_db():
    if ENVIRONMENT == "dev":
        print("CREATING TABLES...") 
        SQLModel.metadata.create_all(engine)
        print("SEEDING DATA...")
        create_locations_from_seed()
        create_metrics_from_seed()
        create_climate_data_from_seed()

def drop_db():
   if ENVIRONMENT == "dev":
        print("DROPPING TABLES")
        SQLModel.metadata.drop_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("STARTING SERVER...")
    load_db()
    yield
    drop_db()
    print("TERMINATING SERVER")

app = FastAPI(title="EcoVision API", lifespan=lifespan)
app.include_router(climate.router)
app.include_router(locations.router)
app.include_router(metrics.router)
app.include_router(summary.router)
app.include_router(trends.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
