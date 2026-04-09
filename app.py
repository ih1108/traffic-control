from fastapi import FastAPI

app = FastAPI(title="Traffic Control System", description="교통 관제 시스템 API")

# Import routers from each module
from fire.view.router import router as fire_router
from abandoned_object.view.router import router as abandoned_object_router
from traffic_jam.view.router import router as traffic_jam_router
from wrong_way.view.router import router as wrong_way_router
from emergency_vehicle.view.router import router as emergency_vehicle_router

# Include routers
app.include_router(fire_router, prefix="/fire", tags=["Fire Detection"])
app.include_router(abandoned_object_router, prefix="/abandoned-object", tags=["Abandoned Object Detection"])
app.include_router(traffic_jam_router, prefix="/traffic-jam", tags=["Traffic Jam Detection"])
app.include_router(wrong_way_router, prefix="/wrong-way", tags=["Wrong Way Detection"])
app.include_router(emergency_vehicle_router, prefix="/emergency-vehicle", tags=["Emergency Vehicle Detection"])

@app.get("/")
async def root():
    return {"message": "Traffic Control System API"}