from backend.db.connection import get_connection
from backend.schemas.asistencia import AsistenciaCreate
import backend.repositories.asistencia as repo


def list_all() -> list[dict]:
    with get_connection() as conn:
        return repo.get_all(conn)


def upsert(data: AsistenciaCreate) -> None:
    with get_connection() as conn:
        repo.upsert(conn, data)
