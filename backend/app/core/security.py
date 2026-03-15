from fastapi import Header, HTTPException
from app.core.config import settings


async def require_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != settings.SECRET_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
