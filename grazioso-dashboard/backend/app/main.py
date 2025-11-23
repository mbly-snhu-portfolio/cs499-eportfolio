"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.database import db_manager
from app.core.redis import get_redis_client, close_redis_connection, is_redis_available
from app.core.errors import DatabaseError
from app.core.rate_limit import limiter, _rate_limit_exceeded_handler
from app.core.security import SecurityHeadersMiddleware
from slowapi.errors import RateLimitExceeded
from app.api import auth, endpoints

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        db_manager.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        logger.warning("Server will start but database operations will fail until MongoDB is configured")
    
    # Initialize Redis connection
    if settings.redis_enabled:
        try:
            get_redis_client()
            if is_redis_available():
                logger.info("Redis connection established")
            else:
                logger.warning("Redis is configured but not available, using in-memory cache fallback")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            logger.warning("Using in-memory cache fallback")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    try:
        db_manager.disconnect()
    except Exception:
        pass
    
    try:
        close_redis_connection()
    except Exception:
        pass


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)


@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    """Handle database errors."""
    logger.error(f"Database error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        db_manager.client.admin.command('ping')
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    # Check Redis connection
    redis_status = "unavailable"
    if settings.redis_enabled:
        redis_status = "connected" if is_redis_available() else "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "redis": redis_status,
        "version": settings.app_version
    }


# Include routers
app.include_router(auth.router)
app.include_router(endpoints.animals.router)
app.include_router(endpoints.analytics.router)

