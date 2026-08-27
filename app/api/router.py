from fastapi import APIRouter

from app.api.routes import health, parse

router = APIRouter()
router.include_router(health.router)
router.include_router(parse.router)
