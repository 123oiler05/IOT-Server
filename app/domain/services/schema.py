from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


# ── Servicio ──────────────────────────────
class ServicioCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    administrador_id: UUID


class ServicioUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None


class ServicioResponse(BaseModel):
    id: UUID
    nombre: str
    descripcion: str | None
    administrador_id: UUID
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Usuario ───────────────────────────────
class UsuarioLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"