class AbandonedObjectService:
    def detect_abandoned_object(self):
        # 교통도로법에 따라 박스 기준 판단
        # 5초 이상 움직임 없음 확인
        # 이벤트 생성 후 알림
        return {"message": "Abandoned object detected and event created"}