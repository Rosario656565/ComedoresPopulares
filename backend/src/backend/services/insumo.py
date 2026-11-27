from fastapi import HTTPException
from backend.db.connection import get_connection
from backend.schemas.insumo import InsumoCreate, InsumoUpdate
import backend.repositories.insumo as repo


def list_all() -> list[dict]:
    with get_connection() as conn:
        return repo.get_all(conn)


def get_one(id: int) -> dict:
    with get_connection() as conn:
        item = repo.get_by_id(conn, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return item


def create(data: InsumoCreate) -> dict:
    with get_connection() as conn:
        return repo.create(conn, data)


def update(id: int, data: InsumoUpdate) -> dict:
    with get_connection() as conn:
        item = repo.update(conn, id, data)
    if item is None:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return item


def remove(id: int) -> None:
    with get_connection() as conn:
        found = repo.delete(conn, id)
    if not found:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
