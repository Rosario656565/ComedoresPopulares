import pyodbc
from backend.schemas.insumo import InsumoCreate, InsumoUpdate


_COLS = "id, nom, cant, min, tipo, costo, don, venc, reg"


def _row_to_dict(cursor: pyodbc.Cursor, row) -> dict:
    keys = [col[0] for col in cursor.description]
    return dict(zip(keys, row))


def get_all(conn: pyodbc.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_COLS} FROM dbo.Insumo")
    return [_row_to_dict(cursor, row) for row in cursor.fetchall()]


def get_by_id(conn: pyodbc.Connection, id: int) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_COLS} FROM dbo.Insumo WHERE id = ?", id)
    row = cursor.fetchone()
    return _row_to_dict(cursor, row) if row else None


def create(conn: pyodbc.Connection, data: InsumoCreate) -> dict:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.Insumo (nom, cant, min, tipo, costo, don, venc, reg) "
        "OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        data.nom, data.cant, data.min, data.tipo,
        data.costo, data.don, data.venc, data.reg,
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    return get_by_id(conn, new_id)


def update(conn: pyodbc.Connection, id: int, data: InsumoUpdate) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE dbo.Insumo "
        "SET nom=?, cant=?, min=?, tipo=?, costo=?, don=?, venc=?, reg=? "
        "WHERE id=?",
        data.nom, data.cant, data.min, data.tipo,
        data.costo, data.don, data.venc, data.reg, id,
    )
    conn.commit()
    return get_by_id(conn, id)


def delete(conn: pyodbc.Connection, id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.Insumo WHERE id = ?", id)
    conn.commit()
    return cursor.rowcount > 0
