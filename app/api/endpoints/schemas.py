from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional


class EndpointCreate(BaseModel):
    name: str
    url: HttpUrl
    check_interval_seconds: int = 60


class EndpointUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    check_interval_seconds: Optional[int] = None
    is_active: Optional[bool] = None


class EndpointResponse(BaseModel):
    id: UUID
    name: str
    url: str
    check_interval_seconds: int
    is_active: bool
    created_at: datetime
    uptime_percentage: Optional[float] = None
    current_status: Optional[str] = None

    model_config = {"from_attributes": True}

# we are not returning user_id in EndpointsRespons, This principle is called minimum necessary exposure — your API returns exactly what the client needs to function, nothing more. Applied consistently it's also called information hiding.