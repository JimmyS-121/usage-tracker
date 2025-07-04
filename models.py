from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    tool_name = Column(String)
    usage_time = Column(Float)  # e.g., minutes used
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
