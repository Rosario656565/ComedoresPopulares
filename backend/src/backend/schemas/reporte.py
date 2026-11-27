from pydantic import BaseModel


class ReporteBase(BaseModel):
    mes: str
    ven: float
    gas: float


class ReporteCreate(ReporteBase):
    pass


class Reporte(ReporteBase):
    model_config = {"from_attributes": True}
