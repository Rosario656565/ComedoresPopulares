from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.apis.router import api_router

app = FastAPI(
    title="Comedores Populares API",
    version="1.0.0",
    description="API REST para el sistema de Comedores Populares.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
