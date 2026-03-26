from fastapi import APIRouter, Depends
from fastapi import status

from app.shared.base_domain.controller import FullCrudApiController
from app.domain.servicio.schemas import (
    ServicioCreate,
    ServicioResponse,
    ServicioUpdate,
    UsuarioLogin,
    TokenResponse,
)
from app.domain.servicio.service import (
    ServicioServiceDep,
    UsuarioAuthServiceDep,
)
from app.shared.pagination import PageResponse


# ── Servicio CRUD ─────────────────────────────────────────
class ServicioController(FullCrudApiController):
    prefix = "/service"
    tags = ["Servicio"]
    service_dep = ServicioServiceDep
    response_schema = ServicioResponse
    create_schema = ServicioCreate
    update_schema = ServicioUpdate


router = ServicioController().router


# ── Usuario Auth ──────────────────────────────────────────
@router.post(
    "/users/login",
    response_model=TokenResponse,
    tags=["Usuario"],
)
def login(
    payload: UsuarioLogin,
    service: UsuarioAuthServiceDep,
):
    return service.login(payload.email, payload.password)


@router.post(
    "/users/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Usuario"],
)
def logout(service: UsuarioAuthServiceDep):
    service.logout()