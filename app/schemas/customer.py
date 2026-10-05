from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Any


class CustomerCreate(BaseModel):
    external_id: str
    name: str
    email: EmailStr
    status: str = "active"
    metadata: dict[str, Any] = {}


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None
    metadata: dict[str, Any] | None = None


class CustomerResponse(BaseModel):
    id: int
    external_id: str
    name: str
    email: str
    status: str
    metadata: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)
