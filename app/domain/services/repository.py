from abc import ABC, abstractmethod
from sqlmodel import Session, select

from app.shared.base_domain.repository import IBaseRepository, BaseRepository
from app.domain.servicio.model import Servicio


# ── Servicio ──────────────────────────────────────────────
class IServicioRepository(IBaseRepository[Servicio], ABC):
    pass  # CRUD base es suficiente


class ServicioRepository(BaseRepository[Servicio], IServicioRepository):
    model = Servicio


# ── Usuario ───────────────────────────────────────────────
class IUsuarioRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str):
        raise NotImplementedError


class UsuarioRepository(IUsuarioRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        from app.domain.servicio.model import Usuario, DatosSensibles
        return self.session.exec(
            select(Usuario)
            .join(DatosSensibles)
            .where(DatosSensibles.email == email)
        ).first()