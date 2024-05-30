# exception_handler.py
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.logging_config import setup_logging

logger = setup_logging()


async def global_exception_handler(request: Request, exc: Exception):
    error_id = uuid.uuid4()
    logger.error(f"Unhandled error occurred. Error ID: {error_id}, Details: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error_id": str(error_id),
            "message": "An error occurred. Please try again.",
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    error_id = uuid.uuid4()
    logger.error(f"Database error occurred. Error ID: {error_id}, Details: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error_id": str(error_id),
            "message": "A database error occurred. Please try again.",
        },
    )
