from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json

from app.core.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} iniciando...")
    yield
    print("Cerrando conexiones...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## Plataforma Abierta Anticorrupción Venezuela

API pública para transparencia de contratación y gasto público.

### Características
- **OCDS Compatible**: Datos estructurados según Open Contracting Data Standard
- **Alertas de riesgo**: Motor de detección con revisión humana obligatoria
- **Descarga masiva**: CSV y JSON OCDS disponibles sin autenticación
- **Paginación estándar**: Metadatos completos en todas las respuestas

### Licencia
MIT — Uso libre con atribución al autor.

**Autor:** Jesús Alexander León Cordero
    """,
    openapi_tags=[
        {"name": "Procesos de Contratación", "description": "Licitaciones y procesos de compra pública"},
        {"name": "Contratos", "description": "Contratos firmados con trazabilidad de adendas y pagos"},
        {"name": "Proveedores", "description": "Registro de empresas y proveedores del Estado"},
        {"name": "Alertas de Riesgo", "description": "Banderas rojas con revisión human-in-the-loop"},
        {"name": "Descargas", "description": "Exportaciones masivas CSV y OCDS JSON"},
    ],
    lifespan=lifespan
)

# CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else json.loads(settings.CORS_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"], summary="Raíz de la API")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "api": "/api/v1",
        "license": "MIT",
        "author": "Jesús Alexander León Cordero",
        "standard": "OCDS v1.1",
    }


@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {"status": "ok"}
