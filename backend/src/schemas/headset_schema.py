from pydantic import BaseModel


class HeadsetSchema(BaseModel):
    headset_id: int
    headset_name: str
    cost: int

    class Config:
        from_attributes = True