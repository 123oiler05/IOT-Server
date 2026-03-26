from abc import ABC, abstractmethod
from uuid import UUID
from typing import Annotated
from datetime import timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from app.shared.base_domain.service import BaseService, IBaseService
from app.domain.servicio.model import Servicio
from app.domain.servicio.repository import ServicioRepository
from app.database import SessionDep
from app.shared.exceptions import BadRequestException


# ── Configuración JWT ─────────────────────────────────────
SECRET_KEY = "cambiar_esto_por_settings"  # mover a config.py
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ── Servicio CRUD ─────────────────────────────────────────
class IServicioService(IBaseService[Servicio], ABC):
    pass  # sin métodos extra por ahora


class ServicioService(BaseService[Servicio], IServicioService):
    entity_name = "Servicio"
    repository_class = ServicioRepository


# ── Usuario Auth ──────────────────────────────────────────
class UsuarioAuthService:

    def __init__(self, session: Session):
        self.session = session

    def login(self, email: str, password: str) -> dict:
        # 1. Buscar usuario por email (a través de DatosSensibles)
        usuario = self._get_by_email(email)

        # 2. ¿Existe?
        if not usuario:
            raise BadRequestException("Credenciales inválidas")

        # 3. ¿Está activo?
        if not usuario.activo:
            raise BadRequestException("Usuario inactivo")

        # 4. ¿Password correcto?
        if not pwd_context.verify(password, usuario.datos_sensibles.password_hash):
            raise BadRequestException("Credenciales inválidas")

        # 5. Generar token
        token = self._create_token({"sub": str(usuario.id)})
        return {"access_token": token, "token_type": "bearer"}

    def logout(self) -> None:
        # Con tokens de corta duración el cliente bota el token
        # No hay nada que hacer en el servidor
        pass

    def _get_by_email(self, email: str):
        # El repository lo implementará
        from app.domain.servicio.repository import UsuarioRepository
        repo = UsuarioRepository(self.session)
        return repo.get_by_email(email)

    def _create_token(self, data: dict) -> str:
        expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(
            {**data, "exp": expire},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )


# ── Dependencies ──────────────────────────────────────────
def get_servicio_service(session: SessionDep) -> ServicioService:
    return ServicioService(session)


def get_usuario_auth_service(session: SessionDep) -> UsuarioAuthService:
    return UsuarioAuthService(session)


ServicioServiceDep = Annotated[ServicioService, Depends(get_servicio_service)]
UsuarioAuthServiceDep = Annotated[UsuarioAuthService, Depends(get_usuario_auth_service)]