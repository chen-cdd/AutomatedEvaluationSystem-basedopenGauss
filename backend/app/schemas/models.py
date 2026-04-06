from datetime import datetime

from pydantic import BaseModel


class ModelBase(BaseModel):
    name: str
    version: str = "v1"
    model_type: str = "judge"
    description: str = ""


class ModelCreate(ModelBase):
    pass


class ModelRead(ModelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
