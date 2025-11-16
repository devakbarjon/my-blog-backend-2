from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.models.schemas.errors import ErrorResponse


limiter = Limiter(key_func=get_remote_address)

def add_rate_limit_exception_handler(app: FastAPI):
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        error_response = ErrorResponse(
            code="rate_limit_exceeded",
            message="Too many requests. Please try again later."
        )
        return JSONResponse(
            status_code=429,
            content=error_response.model_dump()
        )