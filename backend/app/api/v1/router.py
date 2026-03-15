from fastapi import APIRouter
from app.api.v1 import processes, contracts, suppliers, risk, download

api_router = APIRouter()

api_router.include_router(processes.router, prefix="/processes", tags=["Procesos de Contratación"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contratos"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Proveedores"])
api_router.include_router(risk.router, prefix="/risk", tags=["Alertas de Riesgo"])
api_router.include_router(download.router, prefix="/download", tags=["Descargas"])
