from fastapi import APIRouter, HTTPException
from ..service.service import AbandonedObjectService

router = APIRouter()

abandoned_object_service = AbandonedObjectService()


@router.post("/detect-floating")
async def detect_floating_object():
    result = abandoned_object_service.detect_floating_object()
    return {"event": "floating_object_detected", "details": result}

@router.post("/detect")
async def detect_abandoned_object():
    # 부화물 감지 로직 호출
    result = abandoned_object_service.detect_abandoned_object()
    return {"event": "abandoned_object_detected", "details": result}