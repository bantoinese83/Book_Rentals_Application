# middleware.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException


def setup_middleware(app: FastAPI):
    # Add GZip middleware to compress responses for improved network efficiency
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ]
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class CatchInvalidHTTPRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except (RequestValidationError, HTTPException) as exc:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid HTTP request received."},
            )
