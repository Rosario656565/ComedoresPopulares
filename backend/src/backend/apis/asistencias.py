from fastapi import APIRouter, status
from backend.schemas.asistencia import Asistencia, AsistenciaCreate
import backend.services.asistencia as svc

router = APIRouter()


@router.get("/", response_model=list[Asistencia])
def list_asistencias():
    return svc.list_all()


@router.post("/", response_model=Asistencia, status_code=status.HTTP_200_OK)
def upsert_asistencia(data: AsistenciaCreate):
    svc.upsert(data)
    return data