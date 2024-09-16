from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models.responses import FailResponse


async def value_error_handler(request: Request, exc: ValueError):
    response_content = FailResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        status_message=str(exc)
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response_content.model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_content = FailResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        status_message=exc.errors()[0]['msg']
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response_content.model_dump(),
    )
