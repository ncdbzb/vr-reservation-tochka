from pydantic import BaseModel
from datetime import datetime


class BookingTimeSchema(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

class BookingCreateSchema(BaseModel):
    headset_id: int
    start_time: datetime
    end_time: datetime
