from collections import defaultdict
import pyodbc
from backend.schemas.asistencia import AsistenciaCreate


def get_all(conn: pyodbc.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CONVERT(VARCHAR(10), fecha, 23), beneficiario_id "
        "FROM dbo.Asistencia ORDER BY fecha"
    )
    agrupado: dict[str, list[int]] = defaultdict(list)
    for fecha, beneficiario_id in cursor.fetchall():
        agrupado[fecha].append(beneficiario_id)

    return [{"fecha": fecha, "ids": ids} for fecha, ids in agrupado.items()]


def upsert(conn: pyodbc.Connection, data: AsistenciaCreate) -> None:
    cursor = conn.cursor()
    # 1. Limpiamos los registros previos de esa fecha para sincronizar la lista
    cursor.execute("DELETE FROM dbo.Asistencia WHERE fecha = ?", data.fecha)

    # 2. Insertamos una fila normalizada (3FN) por cada beneficiario que asistió
    for beneficiario_id in set(data.ids):
        cursor.execute(
            "INSERT INTO dbo.Asistencia (fecha, beneficiario_id) VALUES (?, ?)",
            data.fecha,
            beneficiario_id,
        )
    conn.commit()