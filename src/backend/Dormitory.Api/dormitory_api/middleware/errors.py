from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dormitory_application.common import BusinessRuleError, ConflictError, NotFoundError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"errorCode": "RESOURCE_NOT_FOUND", "message": str(exc)},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"errorCode": "RESOURCE_CONFLICT", "message": str(exc)},
        )

    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(_: Request, exc: BusinessRuleError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"errorCode": exc.error_code, "message": str(exc)},
        )
