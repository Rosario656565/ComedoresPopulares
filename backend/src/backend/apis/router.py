from fastapi import APIRouter
from backend.apis import beneficiarios, insumos, reportes, asistencias

api_router = APIRouter()

api_router.include_router(
    beneficiarios.router,
    prefix="/beneficiarios",
    tags=["Beneficiarios"],
)
api_router.include_router(
    insumos.router,
    prefix="/insumos",
    tags=["Insumos"],
)
api_router.include_router(
    reportes.router,
    prefix="/reportes",
    tags=["Reportes"],
)
api_router.include_router(
    asistencias.router,
    prefix="/asistencias",
    tags=["Asistencias"],
)
