# exceptions.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

# Global handler for HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": True}
    )

# Handler for validation errors (e.g., invalid request body)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "error": True}
    )

# Handler for IntegrityError (e.g., duplicate entries)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error", "error": True}
    )

# Handler for NoResultFound (e.g., record not found)
async def no_result_found_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "error": True}
    )
