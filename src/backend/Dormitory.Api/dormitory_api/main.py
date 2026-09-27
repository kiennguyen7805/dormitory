from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from dormitory_api.controllers import (
    auth_router,
    billing_router,
    contracts_router,
    housing_router,
    identity_router,
    students_router,
    utilities_router,
)
from dormitory_api.middleware import register_error_handlers
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.config import get_settings

settings = get_settings()

tags_metadata = [
    {"name": "System", "description": "Trạng thái hoạt động của API và PostgreSQL."},
    {"name": "Auth", "description": "Đăng nhập, đăng xuất và thông tin phiên hiện tại."},
    {"name": "Identity", "description": "Người dùng, quyền và hồ sơ sinh viên."},
    {"name": "Students", "description": "CRUD sinh viên và phân trang theo Bài 2."},
    {"name": "Housing", "description": "Tòa nhà, loại phòng, phòng, giường và sơ đồ phòng."},
    {"name": "Contracts", "description": "Đơn đăng ký, hợp đồng và lịch sử phân giường."},
    {"name": "Utilities", "description": "Công tơ, biểu giá, ghi chỉ số và nhập Excel điện nước."},
    {"name": "Billing", "description": "Sinh và tra cứu hóa đơn tiền phòng, điện, nước."},
]

app = FastAPI(
    title="Dormitory Management API",
    description=(
        "API quản lý ký túc xá. Dùng POST /api/v1/auth/login để lấy access_token, "
        "sau đó bấm Authorize và nhập token để thử các chức năng có bảo vệ."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_error_handlers(app)
for api_router in (
    auth_router,
    housing_router,
    contracts_router,
    identity_router,
    students_router,
    utilities_router,
    billing_router,
):
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(api_router, prefix="/api", include_in_schema=False)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/healthz", tags=["System"], summary="Kiểm tra API đang sống")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health", tags=["System"], include_in_schema=False)
def legacy_health() -> dict[str, str]:
    return health()


@app.get("/readyz", tags=["System"], summary="Kiểm tra kết nối PostgreSQL")
def readiness(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "errorCode": "DATABASE_NOT_READY",
                "message": "PostgreSQL chưa sẵn sàng.",
            },
        )
    return {"status": "ready", "database": "ok"}
