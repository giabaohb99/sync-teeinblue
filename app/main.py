from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from contextlib import asynccontextmanager

from . import models, schemas, crud, database, services, scheduler

# Create Tables if not exist
models.Base.metadata.create_all(bind=database.engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown_scheduler()

app = FastAPI(title="Teeinblue Order Sync", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "active", "service": "Teeinblue Sync"}

@app.get("/orders", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.post("/sync")
def trigger_sync(request: schemas.SyncRequest, background_tasks: BackgroundTasks):
    """
    Manually trigger Bot 1 (Sync Teeinblue) with options:
    - option: "1d", "7d", "30d"
    - or custom: days_start, days_end
    """
    start = 1
    end = 0
    
    if request.days_start is not None:
        start = request.days_start
        end = request.days_end if request.days_end is not None else 0
    else:
        if request.option == schemas.TimeRangeOption.LAST_24H:
            start = 1
        elif request.option == schemas.TimeRangeOption.LAST_7D:
            start = 7
        elif request.option == schemas.TimeRangeOption.LAST_30D:
            start = 30
            
    # Add task with calculated args
    background_tasks.add_task(services.sync_teeinblue_orders_service, start, end)
    
    return {
        "message": "Sync started in background", 
        "range": f"{start} days ago to {end} days ago"
    }
