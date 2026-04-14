from database.config import SessionLocal
from database.event_repository import create_event_with_detection


class WrongWayService:
    def detect_wrong_way(self, cctv_id: int = 1):
        db = SessionLocal()
        try:
            detection, event = create_event_with_detection(
                db=db,
                cctv_id=cctv_id,
                event_type="wrong_way",
                description="차량 진행 방향 역주행 감지",
                metadata={"source": "wrong_way_service"},
                object_type="vehicle",
            )
            db.commit()
            return {
                "message": "Wrong way detected and event created",
                "detection_id": detection.id,
                "event_id": event.id,
            }
        except Exception as e:
            db.rollback()
            return {"message": "Wrong way detection failed", "error": str(e)}
        finally:
            db.close()