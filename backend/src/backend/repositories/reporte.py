import pyodbc
from backend.schemas.reporte import ReporteCreate


def _row_to_dict(cursor: pyodbc.Cursor, row) -> dict:
    keys = [col[0] for col in cursor.description]
    return dict(zip(keys, row))


def get_all(conn: pyodbc.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT mes, ven, gas FROM dbo.Reporte")
    return [_row_to_dict(cursor, row) for row in cursor.fetchall()]


def upsert(conn: pyodbc.Connection, data: ReporteCreate) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        MERGE dbo.Reporte AS target
        USING (SELECT ? AS mes, ? AS ven, ? AS gas) AS src
            ON target.mes = src.mes
        WHEN MATCHED THEN
            UPDATE SET ven = src.ven, gas = src.gas
        WHEN NOT MATCHED THEN
            INSERT (mes, ven, gas) VALUES (src.mes, src.ven, src.gas);
        """,
        data.mes, data.ven, data.gas,
    )
    conn.commit()


def delete_by_mes(conn: pyodbc.Connection, mes: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.Reporte WHERE mes = ?", mes)
    conn.commit()
    return cursor.rowcount > 0
