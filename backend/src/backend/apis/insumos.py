from fastapi import APIRouter, status
from backend.schemas.insumo import Insumo, InsumoCreate, InsumoUpdate
import backend.services.insumo as svc

router = APIRouter()


@router.get("/", response_model=list[Insumo])
def list_insumos():
    return svc.list_all()


@router.post("/", response_model=Insumo, status_code=status.HTTP_201_CREATED)
def create_insumo(data: InsumoCreate):
    return svc.create(data)


@router.put("/{id}", response_model=Insumo)
def update_insumo(id: int, data: InsumoUpdate):
    return svc.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_insumo(id: int):
    svc.remove(id)
