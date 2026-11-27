from fastapi import APIRouter, status
from backend.schemas.reporte import Reporte, ReporteCreate
import backend.services.reporte as svc

router = APIRouter()


@router.get("/", response_model=list[Reporte])
def list_reportes():
    return svc.list_all()


@router.post("/", response_model=Reporte)
def upsert_reporte(data: ReporteCreate):
    svc.upsert(data)
    return data


@router.delete("/{mes}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reporte(mes: str):
    svc.remove(mes)
