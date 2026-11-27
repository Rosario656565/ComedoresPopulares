from typing import Literal
from pydantic import BaseModel


class BeneficiarioBase(BaseModel):
    nom: str
    dni: str  # 8 dígitos
    dir: str
    nac: str
    mail: str
    est: Literal["Activo", "Inactivo"]


class BeneficiarioCreate(BeneficiarioBase):
    pass


class BeneficiarioUpdate(BeneficiarioBase):
    pass


class Beneficiario(BeneficiarioBase):
    id: int

    model_config = {"from_attributes": True}
