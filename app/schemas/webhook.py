from pydantic import BaseModel
from typing import Any


class WebhookPayload(BaseModel):
    event_id: str
    event_type: str
    data: dict[str, Any]
