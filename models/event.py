from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from database.config import Base

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    cctv_id = Column(Integer, ForeignKey("cctv.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_time = Column(TIMESTAMP, server_default=func.now())
    description = Column(Text)
    metadata = Column(JSON)

    def __repr__(self):
        return f"<Event(id={self.id}, cctv_id={self.cctv_id}, event_type={self.event_type})>"