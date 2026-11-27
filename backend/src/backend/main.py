from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.apis import beneficiarios, insumos, asistencias, reportes, panel

app = FastAPI(title="Comedores Populares API", version="1.0.0")

# CORS – permite peticiones desde el frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar
init_db()

# Registrar routers
app.include_router(beneficiarios.router)
app.include_router(insumos.router)
app.include_router(asistencias.router)
app.include_router(reportes.router)
app.include_router(panel.router)


@app.get("/")
def read_root():
    return {"mensaje": "Servidor activo - Comedores Populares API"}