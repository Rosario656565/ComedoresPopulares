from typing import Literal, Optional
from pydantic import BaseModel


class InsumoBase(BaseModel):
    nom: str
    cant: float
    min: float
    tipo: Literal["Compra", "Donación"]
    costo: float
    don: Optional[str] = None
    venc: str
    reg: str


class InsumoCreate(InsumoBase):
    pass


class InsumoUpdate(InsumoBase):
    pass


class Insumo(InsumoBase):
    id: int

    model_config = {"from_attributes": True}
