from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from .database import Base


class URLMonitor(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    status = Column(String(10), nullable=False, default="UNKNOWN")
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    checked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
