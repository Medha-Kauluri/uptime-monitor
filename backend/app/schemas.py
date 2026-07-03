from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator


class MonitorStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


class URLCreate(BaseModel):
    url: HttpUrl

    @field_validator("url", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v


class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    status: MonitorStatus
    status_code: int | None = None
    response_time_ms: float | None = None
    checked_at: datetime | None = None
    created_at: datetime
