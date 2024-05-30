# main.py
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.applications import State

from api import auth_routes, user_routes, book_routes
from core.events import create_start_app_handler, create_stop_app_handler
from core.logging_config import setup_logging
from exceptions.exception_handler import global_exception_handler, http_exception_handler, sqlalchemy_exception_handler
from middleware.middleware import CatchInvalidHTTPRequestsMiddleware, setup_middleware
from middleware.rate_limiter import limiter

# Create FastAPI application
app = FastAPI(title="Book_Rentals_Application", version="1.0", debug=True)

# Create a state instance and add the limiter to it
app.state = State()
app.state.limiter = limiter

app.exception_handler(Exception)(global_exception_handler)
app.exception_handler(StarletteHTTPException)(http_exception_handler)
app.exception_handler(SQLAlchemyError)(sqlalchemy_exception_handler)

# Include routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(book_routes.router)

setup_logging()

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))
app.add_middleware(CatchInvalidHTTPRequestsMiddleware)

setup_middleware(app)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Book_Rentals_Application!"}
