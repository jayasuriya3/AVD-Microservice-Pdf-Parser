from fastapi import FastAPI

from app.api.router import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.middleware import CorrelationIdMiddleware

configure_logging()
settings = get_settings()
app = FastAPI(title="AdvisorDesk CAS Parser", version=settings.version)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)
