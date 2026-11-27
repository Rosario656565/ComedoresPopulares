import json
from datetime import date
from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import InsumoIn, InsumoOut, DescontarIn

router = APIRouter(prefix="/insumos", tags=["Insumos"])


def _row(row) -> InsumoOut:
    return InsumoOut(**dict(row))


@router.get("", response_model=list[InsumoOut])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM insumos ORDER BY venc").fetchall()
    return [_row(r) for r in rows]


@router.post("", response_model=InsumoOut, status_code=201)
def crear(i: InsumoIn):
    if i.tipo == "Donación":
        i.costo = 0
    if not i.reg:
        i.reg = date.today().strftime("%Y-%m")
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO insumos (nom,cant,min,tipo,costo,don,venc,reg) VALUES (?,?,?,?,?,?,?,?)",
            (i.nom, i.cant, i.min, i.tipo, i.costo, i.don, i.venc, i.reg),
        )
        row = conn.execute("SELECT * FROM insumos WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(row)


@router.put("/{id}", response_model=InsumoOut)
def actualizar(id: int, i: InsumoIn):
    if i.tipo == "Donación":
        i.costo = 0
    with get_conn() as conn:
        conn.execute(
            "UPDATE insumos SET nom=?,cant=?,min=?,tipo=?,costo=?,don=?,venc=?,reg=? WHERE id=?",
            (i.nom, i.cant, i.min, i.tipo, i.costo, i.don, i.venc, i.reg, id),
        )
        row = conn.execute("SELECT * FROM insumos WHERE id=?", (id,)).fetchone()
    if not row:
        raise HTTPException(404, "Insumo no encontrado")
    return _row(row)


@router.delete("/{id}", status_code=204)
def eliminar(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM insumos WHERE id=?", (id,))


@router.post("/{id}/descontar", response_model=InsumoOut)
def descontar(id: int, body: DescontarIn):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM insumos WHERE id=?", (id,)).fetchone()
        if not row:
            raise HTTPException(404, "Insumo no encontrado")
        if body.cantidad <= 0:
            raise HTTPException(400, "La cantidad debe ser mayor a 0")
        if body.cantidad > row["cant"]:
            raise HTTPException(400, f"Solo hay {row['cant']} en stock de {row['nom']}")
        conn.execute(
            "UPDATE insumos SET cant=cant-? WHERE id=?",
            (body.cantidad, id),
        )
        row = conn.execute("SELECT * FROM insumos WHERE id=?", (id,)).fetchone()
    return _row(row)
