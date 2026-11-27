from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import ReporteIn, ReporteOut

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def _row(row) -> ReporteOut:
    return ReporteOut(**dict(row))


@router.get("", response_model=list[ReporteOut])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM reportes ORDER BY mes").fetchall()
    return [_row(r) for r in rows]


@router.post("", response_model=ReporteOut)
def guardar(r: ReporteIn):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO reportes (mes,ven,gas) VALUES (?,?,?) "
            "ON CONFLICT(mes) DO UPDATE SET ven=excluded.ven, gas=excluded.gas",
            (r.mes, r.ven, r.gas),
        )
        row = conn.execute("SELECT * FROM reportes WHERE mes=?", (r.mes,)).fetchone()
    return _row(row)


@router.delete("/{mes}", status_code=204)
def eliminar(mes: str):
    with get_conn() as conn:
        conn.execute("DELETE FROM reportes WHERE mes=?", (mes,))
