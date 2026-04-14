from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database.config import Base

class Detection(Base):
    __tablename__ = "detection"

    id = Column(Integer, primary_key=True, index=True)
    cctv_id = Column(Integer, ForeignKey("cctv.id"), nullable=False)
    object_type = Column(String(50), nullable=False)
    detected_at = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<Detection(id={self.id}, cctv_id={self.cctv_id}, object_type={self.object_type})>"   