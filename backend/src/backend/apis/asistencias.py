import json
from fastapi import APIRouter
from backend.database import get_conn
from backend.models import AsistenciaIn, AsistenciaOut

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


def _row(row) -> AsistenciaOut:
    return AsistenciaOut(fecha=row["fecha"], ids=json.loads(row["ids"]))


@router.get("", response_model=list[AsistenciaOut])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM asistencias ORDER BY fecha DESC").fetchall()
    return [_row(r) for r in rows]


@router.get("/{fecha}", response_model=AsistenciaOut)
def obtener(fecha: str):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM asistencias WHERE fecha=?", (fecha,)).fetchone()
    if not row:
        return AsistenciaOut(fecha=fecha, ids=[])
    return _row(row)


@router.post("", response_model=AsistenciaOut)
def guardar(a: AsistenciaIn):
    ids_json = json.dumps(a.ids)
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO asistencias (fecha,ids) VALUES (?,?) "
            "ON CONFLICT(fecha) DO UPDATE SET ids=excluded.ids",
            (a.fecha, ids_json),
        )
        row = conn.execute("SELECT * FROM asistencias WHERE fecha=?", (a.fecha,)).fetchone()
    return _row(row)
