# Hệ thống Quản lý Ký túc xá (MVP)

Ứng dụng được tổ chức theo Modular Monolith và feature folders trong `docs/02-cau-truc-du-an.md`.
Theo yêu cầu triển khai bằng Python, bốn lớp trong thiết kế được giữ nguyên về trách nhiệm nhưng dùng
FastAPI + SQLAlchemy + Alembic thay cho ASP.NET Core + EF Core.

## Công nghệ

- Backend: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16.
- Xác thực: JWT, Argon2, ba vai trò cố định `Admin`, `Staff`, `Student`.
- Frontend: React 19, TypeScript, Vite, Ant Design.
- Test: pytest + FastAPI TestClient; frontend được kiểm tra bằng TypeScript/Vite build.

## Cấu trúc

```text
src/
├── backend/
│   ├── Dormitory.Domain/dormitory_domain/                 # entity, enum, business rules
│   ├── Dormitory.Application/dormitory_application/       # schema, interface, use case
│   ├── Dormitory.Infrastructure/dormitory_infrastructure/ # SQLAlchemy, migration, auth, seed
│   ├── Dormitory.Api/dormitory_api/                       # FastAPI router, middleware, authorization
│   ├── alembic.ini
│   └── pyproject.toml
└── frontend/
    ├── src/app, api, auth, components, layouts, features, routes
    └── prototype-html/                                    # prototype gốc để tham chiếu

tests/
├── Dormitory.Domain.Tests/
└── Dormitory.Api.IntegrationTests/
```

Các feature folders dành cho tuần sau vẫn được giữ đúng thiết kế: Contracts, Utilities, Billing,
Violations, Reports và AI.

## Chạy dự án

### 1. Backend

```bash
cp .env.example .env
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -e "src/backend[dev]"
docker compose up -d postgres
cd src/backend
alembic upgrade head
python -m dormitory_infrastructure.identity.seed_cli
uvicorn dormitory_api.main:app --reload
```

API chạy tại `http://localhost:8000`; Swagger UI tại `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd src/frontend
npm install
npm run dev
```

Frontend chạy tại `http://localhost:5173`.

## Tài khoản demo tuần 1

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@dormitory.local` | `Admin@123` |
| Staff | `staff@dormitory.local` | `Staff@123` |
| Student | `student@dormitory.local` | `Student@123` |

Chỉ dùng các mật khẩu này cho môi trường phát triển.

## Phạm vi hoàn thành tuần 1

- Docker Compose cho PostgreSQL và migration đầu tiên.
- Seed ba role và một tài khoản demo cho mỗi role.
- API đăng nhập, đăng xuất, xem người dùng hiện tại; JWT + role guard.
- F01–F04: CRUD tòa nhà, loại phòng, phòng, giường.
- F05: room matrix; trạng thái giường là dữ liệu suy ra, không nhận từ request.
- Frontend login, layout Admin/Staff và Student, routing theo role.
- Frontend quản lý cơ sở vật chất và xem room matrix.
- Test tích hợp luồng demo cuối tuần 1.

## Kiểm tra

```bash
cd src/backend && pytest
cd src/frontend && npm run build
```
