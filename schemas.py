from pydantic import BaseModel
from datetime import datetime

class UsageRecordCreate(BaseModel):
    user_id: str
    tool_name: str
    usage_time: float

class UsageRecord(UsageRecordCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
