# app/models.py

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    tool_name = Column(String, nullable=False)
    usage_time = Column(Float, nullable=False)  # e.g., minutes used
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
