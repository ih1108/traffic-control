class EventManagementService:
    def receive_event(self, payload: dict):
        return {"message": "이벤트 수신 구조 준비 완료", "payload": payload}

    def list_events(self, event_type: str | None = None, sort: str = "desc"):
        return {
            "message": "이벤트 목록/정렬/필터 구조 준비 완료",
            "event_type": event_type,
            "sort": sort,
        }

    def get_event_detail(self, event_id: int):
        return {"message": "이벤트 상세 조회 구조 준비 완료", "event_id": event_id}

    def get_event_metadata(self, event_id: int):
        return {"message": "이벤트 metadata 조회 구조 준비 완료", "event_id": event_id}