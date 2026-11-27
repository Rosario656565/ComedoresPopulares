import pyodbc
from backend.schemas.beneficiario import BeneficiarioCreate, BeneficiarioUpdate


_COLS = "id, nom, dni, dir, nac, mail, est"


def _row_to_dict(cursor: pyodbc.Cursor, row) -> dict:
    keys = [col[0] for col in cursor.description]
    return dict(zip(keys, row))


def get_all(conn: pyodbc.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_COLS} FROM dbo.Beneficiario")
    return [_row_to_dict(cursor, row) for row in cursor.fetchall()]


def get_by_id(conn: pyodbc.Connection, id: int) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_COLS} FROM dbo.Beneficiario WHERE id = ?", id)
    row = cursor.fetchone()
    return _row_to_dict(cursor, row) if row else None


def create(conn: pyodbc.Connection, data: BeneficiarioCreate) -> dict:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.Beneficiario (nom, dni, dir, nac, mail, est) "
        "OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)",
        data.nom, data.dni, data.dir, data.nac, data.mail, data.est,
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    return get_by_id(conn, new_id)


def update(conn: pyodbc.Connection, id: int, data: BeneficiarioUpdate) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE dbo.Beneficiario "
        "SET nom=?, dni=?, dir=?, nac=?, mail=?, est=? "
        "WHERE id=?",
        data.nom, data.dni, data.dir, data.nac, data.mail, data.est, id,
    )
    conn.commit()
    return get_by_id(conn, id)


def delete(conn: pyodbc.Connection, id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.Beneficiario WHERE id = ?", id)
    conn.commit()
    return cursor.rowcount > 0
