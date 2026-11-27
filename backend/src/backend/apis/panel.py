import json
from datetime import date, datetime
from fastapi import APIRouter
from backend.database import get_conn
from backend.models import Alerta, PanelOut

router = APIRouter(prefix="/panel", tags=["Panel"])


def _dias(venc: str) -> int:
    """Días que faltan hasta venc (negativo si ya venció)."""
    try:
        hoy = date.today()
        d = date.fromisoformat(venc)
        return (d - hoy).days
    except Exception:
        return 999


@router.get("", response_model=PanelOut)
def panel():
    hoy_str = date.today().isoformat()
    with get_conn() as conn:
        beneficiarios = conn.execute("SELECT * FROM beneficiarios").fetchall()
        insumos = conn.execute("SELECT * FROM insumos").fetchall()
        asistencia_hoy = conn.execute(
            "SELECT ids FROM asistencias WHERE fecha=?", (hoy_str,)
        ).fetchone()

    activos = sum(1 for b in beneficiarios if b["est"] == "Activo")

    raciones_hoy = 0
    if asistencia_hoy:
        try:
            raciones_hoy = len(json.loads(asistencia_hoy["ids"]))
        except Exception:
            pass

    stock_bajo = 0
    por_vencer = 0
    alertas: list[Alerta] = []

    for i in insumos:
        bajo = i["cant"] <= i["min"]
        if bajo:
            stock_bajo += 1
            alertas.append(Alerta(
                nom=i["nom"],
                txt=f"stock bajo ({i['cant']} de mínimo {i['min']})",
                acc="Comprar",
                rojo=True,
            ))
        if i["venc"]:
            d = _dias(i["venc"])
            if d < 0:
                alertas.append(Alerta(
                    nom=i["nom"],
                    txt=f"venció hace {-d} días",
                    acc="Retirar",
                    rojo=True,
                ))
            elif d <= 30:
                por_vencer += 1
                alertas.append(Alerta(
                    nom=i["nom"],
                    txt=f"vence en {d} días ({i['venc']})",
                    acc="Usar pronto",
                    rojo=False,
                ))

    return PanelOut(
        activos=activos,
        raciones_hoy=raciones_hoy,
        stock_bajo=stock_bajo,
        por_vencer=por_vencer,
        alertas=alertas,
    )
