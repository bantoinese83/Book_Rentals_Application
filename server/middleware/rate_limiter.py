import os

from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.logging_config import logger


def ratelimit_handler(request, exc):
    logger.error(f"Rate limit exceeded for request {request.url}")
    return HTTPException(status_code=429, detail="Rate limit exceeded")


# Get rate limit value from environment variable with a default
RATELIMIT_VALUE = os.getenv('RATELIMIT_VALUE', '100/hour')

limiter = Limiter(key_func=get_remote_address, default_limits=[RATELIMIT_VALUE])
