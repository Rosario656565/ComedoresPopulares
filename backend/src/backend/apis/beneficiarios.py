from fastapi import APIRouter, status
from backend.schemas.beneficiario import Beneficiario, BeneficiarioCreate, BeneficiarioUpdate
import backend.services.beneficiario as svc

router = APIRouter()


@router.get("/", response_model=list[Beneficiario])
def list_beneficiarios():
    return svc.list_all()


@router.post("/", response_model=Beneficiario, status_code=status.HTTP_201_CREATED)
def create_beneficiario(data: BeneficiarioCreate):
    return svc.create(data)


@router.put("/{id}", response_model=Beneficiario)
def update_beneficiario(id: int, data: BeneficiarioUpdate):
    return svc.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_beneficiario(id: int):
    svc.remove(id)
