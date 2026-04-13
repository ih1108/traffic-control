from fastapi import FastAPI
from database.config import engine, Base
from models import CCTV, Event, Detection
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="Traffic Control System", description="교통 관제 시스템 API")


@app.on_event("startup")
def init_db_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        # Keep API alive even when DB is temporarily unavailable.
        print(f"[WARN] DB initialization skipped: {exc}")

# Import routers from each module
from fire.view.router import router as fire_router
from abandoned_object.view.router import router as abandoned_object_router
from traffic_jam.view.router import router as traffic_jam_router
from wrong_way.view.router import router as wrong_way_router
from emergency_vehicle.view.router import router as emergency_vehicle_router
from cctv_management.view.router import router as cctv_router
from event_management.view.router import router as event_router
from test_feature.view.router import router as test_router
from map_feature.view.router import router as map_router
from notification_feature.view.router import router as notification_router
from location_feature.view.router import router as location_router
from route_feature.view.router import router as route_router

# Include routers
app.include_router(fire_router, prefix="/fire", tags=["Fire Detection"])
app.include_router(abandoned_object_router, prefix="/abandoned-object", tags=["Abandoned Object Detection"])
app.include_router(traffic_jam_router, prefix="/traffic-jam", tags=["Traffic Jam Detection"])
app.include_router(wrong_way_router, prefix="/wrong-way", tags=["Wrong Way Detection"])
app.include_router(emergency_vehicle_router, prefix="/emergency-vehicle", tags=["Emergency Vehicle Detection"])
app.include_router(cctv_router, prefix="/cctvs", tags=["CCTV Management"])
app.include_router(event_router, prefix="/events", tags=["Event Management"])
app.include_router(test_router, prefix="/tests", tags=["Test Feature"])
app.include_router(map_router, prefix="/map", tags=["Map Feature"])
app.include_router(notification_router, prefix="/notifications", tags=["Notification Feature"])
app.include_router(location_router, prefix="/location", tags=["Location Feature"])
app.include_router(route_router, prefix="/routes", tags=["Route Feature"])

@app.get("/")
async def root():
    return {"message": "Traffic Control System API"}