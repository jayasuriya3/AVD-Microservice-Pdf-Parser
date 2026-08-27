from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "healthy", "service": settings.service_name, "version": settings.version}


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
