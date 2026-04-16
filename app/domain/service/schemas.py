from uuid import UUID
from pydantic import BaseModel
from app.shared.base_domain.schemas import BaseSchemaResponse


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    created_by_id: UUID


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ServiceResponse(BaseSchemaResponse):
    name: str
    description: str | None
    created_by_id: UUID
    is_active: bool