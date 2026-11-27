from fastapi import HTTPException
from backend.db.connection import get_connection
from backend.schemas.reporte import ReporteCreate
import backend.repositories.reporte as repo


def list_all() -> list[dict]:
    with get_connection() as conn:
        return repo.get_all(conn)


def upsert(data: ReporteCreate) -> None:
    with get_connection() as conn:
        repo.upsert(conn, data)


def remove(mes: str) -> None:
    with get_connection() as conn:
        found = repo.delete_by_mes(conn, mes)
    if not found:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
