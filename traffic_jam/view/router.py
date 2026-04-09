from fastapi import APIRouter, HTTPException
from ..service.service import TrafficJamService

router = APIRouter()

traffic_jam_service = TrafficJamService()

@router.post("/detect")
async def detect_traffic_jam():
    # 교통체증 감지 로직 호출
    result = traffic_jam_service.detect_traffic_jam()
    return {"event": "traffic_jam_detected", "details": result}