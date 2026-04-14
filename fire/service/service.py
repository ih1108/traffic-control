from database.config import SessionLocal
from database.event_repository import create_event_with_detection


class FireDetectionService:
    def detect_fire(self, cctv_id: int = 1):
        db = SessionLocal()
        try:
            detection, event = create_event_with_detection(
                db=db,
                cctv_id=cctv_id,
                event_type="fire",
                description="불/연기 5초 이상 감지",
                metadata={"duration_sec": 5, "source": "fire_service"},
                object_type="fire",
            )
            db.commit()
            return {
                "message": "Fire detected and event created",
                "detection_id": detection.id,
                "event_id": event.id,
            }
        except Exception as e:
            db.rollback()
            return {"message": "Fire detection failed", "error": str(e)}
        finally:
            db.close()