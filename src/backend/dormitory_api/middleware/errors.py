import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from dormitory_application.common import BusinessRuleError, ConflictError, NotFoundError

logger = logging.getLogger(__name__)


def _uses_v1_contract(request: Request) -> bool:
    return request.url.path.startswith("/api/v1")


def _problem(
    request: Request,
    status_code: int,
    title: str,
    detail: str,
    error_code: str,
    **extensions,
) -> JSONResponse:
    trace_id = request.headers.get("X-Request-ID") or str(uuid4())
    content = {
        "type": f"https://dormitory.local/problems/{error_code.lower().replace('_', '-')}",
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": request.url.path,
        "errorCode": error_code,
        "traceId": trace_id,
        **extensions,
    }
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
        media_type="application/problem+json",
    )


def _legacy(status_code: int, error_code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"errorCode": error_code, "message": message},
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        if not _uses_v1_contract(request):
            return _legacy(404, "RESOURCE_NOT_FOUND", str(exc))
        return _problem(
            request, 404, "Resource Not Found", str(exc), "RESOURCE_NOT_FOUND"
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        if not _uses_v1_contract(request):
            return _legacy(409, "RESOURCE_CONFLICT", str(exc))
        return _problem(
            request, 409, "Resource Conflict", str(exc), "RESOURCE_CONFLICT"
        )

    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
        if not _uses_v1_contract(request):
            return _legacy(exc.status_code, exc.error_code, str(exc))
        return _problem(
            request,
            exc.status_code,
            "Business Rule Violation",
            str(exc),
            exc.error_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        if not _uses_v1_contract(request):
            return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())})
        return _problem(
            request,
            400,
            "Validation Failed",
            "Dữ liệu đầu vào không hợp lệ.",
            "VALIDATION_ERROR",
            errors=exc.errors(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        if not _uses_v1_contract(request):
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": jsonable_encoder(exc.detail)},
                headers=exc.headers,
            )
        detail = exc.detail
        error_code = f"HTTP_{exc.status_code}"
        message = str(detail)
        if isinstance(detail, dict):
            error_code = detail.get("errorCode", error_code)
            message = detail.get("message", message)
        titles = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Resource Not Found",
            409: "Resource Conflict",
            422: "Unprocessable Entity",
            429: "Too Many Requests",
        }
        response = _problem(
            request,
            exc.status_code,
            titles.get(exc.status_code, "HTTP Error"),
            message,
            error_code,
        )
        if exc.headers:
            response.headers.update(exc.headers)
        return response

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        trace_id = request.headers.get("X-Request-ID") or str(uuid4())
        logger.exception("Unhandled API error trace_id=%s path=%s", trace_id, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "type": "https://dormitory.local/problems/internal-server-error",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "Đã có lỗi xảy ra phía máy chủ.",
                "instance": request.url.path,
                "errorCode": "INTERNAL_SERVER_ERROR",
                "traceId": trace_id,
            },
            media_type="application/problem+json",
        )
