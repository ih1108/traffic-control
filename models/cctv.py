from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database.config import Base

class CCTV(Base):
    __tablename__ = "cctv"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False)
    stream_url = Column(Text, nullable=False)
    direction = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<CCTV(id={self.id}, location={self.location}, direction={self.direction})>"