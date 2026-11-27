from typing import Literal, Optional
from pydantic import BaseModel


# ── Beneficiarios ──────────────────────────────────────────────────────────────

class BeneficiarioIn(BaseModel):
    nom:  str
    dni:  str
    dir:  str = ""
    nac:  str = ""
    mail: str = ""
    est:  Literal["Activo", "Inactivo"] = "Activo"


class BeneficiarioOut(BeneficiarioIn):
    id: int


# ── Insumos ────────────────────────────────────────────────────────────────────

class InsumoIn(BaseModel):
    nom:  str
    cant: float = 0
    min:  float = 0
    tipo: Literal["Compra", "Donación"] = "Compra"
    costo: float = 0
    don:  str = ""
    venc: str = ""
    reg:  str = ""


class InsumoOut(InsumoIn):
    id: int


class DescontarIn(BaseModel):
    cantidad: float


# ── Asistencias ────────────────────────────────────────────────────────────────

class AsistenciaIn(BaseModel):
    fecha: str
    ids:   list[int]


class AsistenciaOut(BaseModel):
    fecha: str
    ids:   list[int]


# ── Reportes ───────────────────────────────────────────────────────────────────

class ReporteIn(BaseModel):
    mes: str
    ven: float = 0
    gas: float = 0


class ReporteOut(ReporteIn):
    pass


# ── Panel ──────────────────────────────────────────────────────────────────────

class Alerta(BaseModel):
    nom:  str
    txt:  str
    acc:  str
    rojo: bool


class PanelOut(BaseModel):
    activos:      int
    raciones_hoy: int
    stock_bajo:   int
    por_vencer:   int
    alertas:      list[Alerta]
