from datetime import datetime

from pydantic import BaseModel


class TaskRead(BaseModel):
    id: int
    name: str
    status: str
    file_name: str
    file_path: str
    file_format: str
    is_desensitized: bool
    error_message: str
    created_at: datetime
    updated_at: datetime
    model_id: int | None = None

    class Config:
        from_attributes = True


class TaskDetail(TaskRead):
    parsed_trace: dict | None = None
    score_result: dict | None = None
    metrics: dict | None = None
