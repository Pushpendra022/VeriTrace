from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.routes.claims import router as claims_router
from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.samples import router as samples_router
from app.api.routes.verification import router as verification_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.db.session import SessionLocal
from app.services.retention_service import delete_expired_reviews

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting %s in %s", settings.app_name, settings.app_env)
    try:
        with SessionLocal() as db:
            removed = delete_expired_reviews(db, settings.review_retention_days)
            if removed:
                logger.info("Removed %d expired reviews", removed)
    except Exception:
        logger.exception("Review retention cleanup failed")
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
)
app.include_router(health_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(claims_router, prefix="/api")
app.include_router(verification_router, prefix="/api")
app.include_router(reviews_router, prefix="/api")
app.include_router(samples_router, prefix="/api")


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "The service encountered an unexpected error.", "details": {}}},
    )
