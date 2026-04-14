from database.config import SessionLocal
from database.event_repository import create_event_with_detection


class AbandonedObjectService:
    def detect_abandoned_object(self, cctv_id: int = 1):
        db = SessionLocal()
        try:
            detection, event = create_event_with_detection(
                db=db,
                cctv_id=cctv_id,
                event_type="abandoned_object",
                description="5초 이상 정지된 부화물 감지",
                metadata={"duration_sec": 5, "source": "abandoned_object_service"},
                object_type="abandoned_object",
            )
            db.commit()
            return {
                "message": "Abandoned object detected and event created",
                "detection_id": detection.id,
                "event_id": event.id,
            }
        except Exception as e:
            db.rollback()
            return {"message": "Abandoned object detection failed", "error": str(e)}
        finally:
            db.close()