from typing import List
from pydantic import BaseModel


class AsistenciaBase(BaseModel):
    fecha: str
    ids: List[int]


class AsistenciaCreate(AsistenciaBase):
    pass


class Asistencia(AsistenciaBase):
    model_config = {"from_attributes": True}
