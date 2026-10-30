# Source repo backend — bản chụp để đọc trên web
Ngày tạo (UTC): 2026-10-05 03:17:20.
Đây là bản chụp chỉ để tham khảo; hãy sửa các file gốc trong repo, không sửa file tổng hợp này.
Bao gồm backend Python, stored SQL, Alembic migrations, test, script chạy và cấu hình chính.
Không gồm `.env`, khóa bí mật, `.git`, môi trường ảo, frontend, tài liệu khác, file nhị phân hoặc file build.
Các URL chứa `changeme` trong cấu hình là giá trị mẫu, không phải mật khẩu nên dùng khi triển khai.
Tổng số file: **121**. Mỗi mục bên dưới giữ nguyên nội dung file gốc và kèm SHA-256.

## Danh sách file
- `.github/workflows/ci.yml`
- `Dockerfile`
- `README.md`
- `docker-compose.yml`
- `scripts/dev-up.sh`
- `scripts/migrate.sh`
- `scripts/render-erd.ps1`
- `scripts/seed.sh`
- `src/backend/alembic.ini`
- `src/backend/dormitory_api/__init__.py`
- `src/backend/dormitory_api/authorization/__init__.py`
- `src/backend/dormitory_api/controllers/__init__.py`
- `src/backend/dormitory_api/controllers/auth.py`
- `src/backend/dormitory_api/controllers/billing.py`
- `src/backend/dormitory_api/controllers/contracts.py`
- `src/backend/dormitory_api/controllers/housing.py`
- `src/backend/dormitory_api/controllers/identity.py`
- `src/backend/dormitory_api/controllers/students.py`
- `src/backend/dormitory_api/controllers/utilities.py`
- `src/backend/dormitory_api/dependencies.py`
- `src/backend/dormitory_api/main.py`
- `src/backend/dormitory_api/middleware/__init__.py`
- `src/backend/dormitory_api/middleware/errors.py`
- `src/backend/dormitory_application/__init__.py`
- `src/backend/dormitory_application/ai/__init__.py`
- `src/backend/dormitory_application/billing/__init__.py`
- `src/backend/dormitory_application/billing/schemas.py`
- `src/backend/dormitory_application/billing/service.py`
- `src/backend/dormitory_application/common/__init__.py`
- `src/backend/dormitory_application/common/errors.py`
- `src/backend/dormitory_application/contracts/__init__.py`
- `src/backend/dormitory_application/contracts/schemas.py`
- `src/backend/dormitory_application/contracts/service.py`
- `src/backend/dormitory_application/housing/__init__.py`
- `src/backend/dormitory_application/housing/interfaces.py`
- `src/backend/dormitory_application/housing/schemas.py`
- `src/backend/dormitory_application/housing/service.py`
- `src/backend/dormitory_application/identity/__init__.py`
- `src/backend/dormitory_application/identity/schemas.py`
- `src/backend/dormitory_application/reports/__init__.py`
- `src/backend/dormitory_application/utilities/__init__.py`
- `src/backend/dormitory_application/utilities/schemas.py`
- `src/backend/dormitory_application/utilities/service.py`
- `src/backend/dormitory_application/violations/__init__.py`
- `src/backend/dormitory_domain/__init__.py`
- `src/backend/dormitory_domain/billing/__init__.py`
- `src/backend/dormitory_domain/billing/calculator.py`
- `src/backend/dormitory_domain/common/__init__.py`
- `src/backend/dormitory_domain/common/enums.py`
- `src/backend/dormitory_domain/contracts/__init__.py`
- `src/backend/dormitory_domain/housing/__init__.py`
- `src/backend/dormitory_domain/housing/entities.py`
- `src/backend/dormitory_domain/utilities/__init__.py`
- `src/backend/dormitory_domain/violations/__init__.py`
- `src/backend/dormitory_infrastructure/__init__.py`
- `src/backend/dormitory_infrastructure/ai/__init__.py`
- `src/backend/dormitory_infrastructure/identity/__init__.py`
- `src/backend/dormitory_infrastructure/identity/security.py`
- `src/backend/dormitory_infrastructure/identity/seed_cli.py`
- `src/backend/dormitory_infrastructure/identity/seeder.py`
- `src/backend/dormitory_infrastructure/persistence/__init__.py`
- `src/backend/dormitory_infrastructure/persistence/config.py`
- `src/backend/dormitory_infrastructure/persistence/database.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/env.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260912_0001_initial.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260919_0002_contracts.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0003_identity_permissions_profiles_audit.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0004_housing_scope_contract_events.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0005_utilities_files.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0006_billing_payments.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0007_violations_maintenance.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0008_notifications.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0009_schema_hardening.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260927_0010_refresh_tokens.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0011_identity_list_function.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0012_identity_operations.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0013_auth_functions.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0014_student_reads.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0015_identity_profiles.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0016_housing_reads.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0017_housing_writes.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0018_contract_reads.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0019_contract_writes.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260929_0020_simplify_to_17_tables.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20261004_0021_utility_billing_functions.py`
- `src/backend/dormitory_infrastructure/persistence/migrations/versions/20261004_0022_seed_functions.py`
- `src/backend/dormitory_infrastructure/persistence/models.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/__init__.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/auth.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/billing.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/contract_reads.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/contract_writes.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/contracts.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/housing.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/housing_reads.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/housing_writes.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/identity.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/students.py`
- `src/backend/dormitory_infrastructure/persistence/repositories/utilities.py`
- `src/backend/dormitory_infrastructure/persistence/sql/auth.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/billing_functions.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/contract_reads.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/contract_writes.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/housing_reads.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/housing_writes.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/identity.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/identity_operations.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/identity_profiles.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/seed_functions.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/students.sql`
- `src/backend/dormitory_infrastructure/persistence/sql/utility_functions.sql`
- `src/backend/pyproject.toml`
- `tests/integration/conftest.py`
- `tests/integration/test_curriculum_alignment.py`
- `tests/integration/test_identity_foundation.py`
- `tests/integration/test_week1_flow.py`
- `tests/integration/test_week2_flow.py`
- `tests/integration/test_week3_flow.py`
- `tests/unit/test_billing_calculator.py`
- `tests/unit/test_housing_entities.py`
- `tests/unit/test_stored_repository_boundary.py`

## File: `.github/workflows/ci.yml`

SHA-256: `b79518abb8bed2323fd8238567e30efc386debad3098521c911e0307911899fe`  
Dòng: 41

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: dormitory_test
          POSTGRES_USER: dormitory
          POSTGRES_PASSWORD: test-only
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U dormitory -d dormitory_test"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      DATABASE_URL: postgresql+psycopg://dormitory:test-only@localhost:5432/dormitory_app
      TEST_DATABASE_URL: postgresql+psycopg://dormitory:test-only@localhost:5432/dormitory_test
    defaults:
      run:
        working-directory: src/backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - name: Install
        run: pip install -e ".[dev]"
      - name: Test with PostgreSQL
        run: pytest
```

## File: `Dockerfile`

SHA-256: `4d509a965c8a3a9a72f39cdcd4854762f7301546db90807a53194948d6a5530b`  
Dòng: 15

```text
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/src/backend

COPY src/backend/ ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "dormitory_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## File: `README.md`

SHA-256: `416e6bd7a316352cdb548f7e4b32df300ae52de0d97eeee85a676eddaef6ce53`  
Dòng: 194

````markdown
# Hệ thống Quản lý Ký túc xá (MVP)

Đây là dự án **backend-only**. Không có frontend React và không có chức năng
import Excel. Swagger UI tại `/docs` và Postman được dùng để thao tác, kiểm thử
và demo API. Kế hoạch chính thức đã điều chỉnh từ workbook 8 tuần nằm tại
[`docs/05-ke-hoach-backend-only.md`](docs/05-ke-hoach-backend-only.md).

Schema hiện hành gồm **17 bảng**. API dùng ba vai trò cố định `Admin`, `Staff`,
`Student`; chỉ số điện/nước được nhập thủ công. Migration `20260929_0020`
chuyển database cũ sang phạm vi này và xóa dữ liệu ở các bảng ngoài phạm vi.
Xem [phân tích lựa chọn schema](docs/04-de-xuat-gian-luoc-database-cho-muc-tieu-hoc-api.md).

Ứng dụng được tổ chức theo Modular Monolith và feature folders trong `docs/02-cau-truc-du-an.md`.
Theo yêu cầu triển khai bằng Python, bốn lớp trong thiết kế được giữ nguyên về trách nhiệm.
Backend dùng FastAPI, PostgreSQL và SQL có tham số; **không dùng ORM**. SQLAlchemy chỉ
được dùng để quản lý kết nối/thực thi SQL, Alembic dùng để chạy migration.

## Phân tích bài toán, nghiệp vụ và database

Hệ thống quản lý vòng đời chỗ ở: sinh viên gửi đơn → cán bộ duyệt → phân giường và
tạo hợp đồng → ghi chỉ số điện/nước → sinh hóa đơn → chuyển giường hoặc chấm dứt
hợp đồng. `Admin` quản lý tài khoản, danh mục và biểu giá; `Staff` xử lý đơn,
chỗ ở và hóa đơn; `Student` gửi đơn và chỉ xem dữ liệu của mình. Quy tắc trọng
tâm là không phân một giường cho hai hợp đồng cùng thời điểm, chỉ phân giường
cho đơn đã duyệt, giữ lịch sử khi chuyển chỗ và không sinh trùng hóa đơn cùng kỳ.

PostgreSQL hiện có 17 bảng sau migration `20260929_0020`, tập trung vào tài khoản
và hồ sơ sinh viên, tòa/phòng/giường, đơn đăng ký/hợp đồng/phân giường, công tơ/
biểu giá/chỉ số và hóa đơn. Alembic quản lý schema; repository dùng SQL có tham số
và PostgreSQL stored function (migration `20261004_0021` bổ sung điện/nước và hóa đơn;
`20261004_0022` bổ sung hàm seed dữ liệu mẫu và kiểm tra kết nối database).
Xem [phân tích nghiệp vụ và dữ liệu](docs/03-phan-tich-nghiep-vu-va-database-hien-trang.md)
để biết quan hệ, bất biến và các khoảng trống nghiệp vụ. Một số mô tả trong tài
liệu đó là mục tiêu thiết kế, chưa phải API đã triển khai; phạm vi schema hiện
hành được chốt tại [phân tích 17 bảng](docs/04-de-xuat-gian-luoc-database-cho-muc-tieu-hoc-api.md).

## Chạy API và kiểm thử thủ công trên Postman

Container `api` được giới hạn RAM và tổng RAM/swap ở 2 GB trong `docker-compose.yml`.
API chạy trực tiếp tại `http://localhost:8000`; không cần gateway hay collection
được lưu trong dự án để thử từng endpoint.

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
```

Trong Postman, tự tạo request `POST http://localhost:8000/api/v1/auth/login`, chọn
Body → raw → JSON và nhập email/mật khẩu demo ở phần dưới. Lấy `access_token`
trong response, rồi thêm header `Authorization: Bearer <access_token>` cho các
endpoint cần đăng nhập. Có thể gõ lần lượt các URL trong các bảng API bên dưới;
Swagger tại `http://localhost:8000/docs` cho biết body và response của từng API.
Kiểm tra mã HTTP và nội dung trả về sau mỗi request.

## Công nghệ

- Backend: Python 3.12, FastAPI, PostgreSQL 16, SQLAlchemy Core (không ORM), Alembic.
- Xác thực: JWT, Argon2, ba vai trò cố định `Admin`, `Staff`, `Student`.
- Giao diện kiểm thử API: Swagger UI và Postman.
- Test: pytest + FastAPI TestClient.

## Cấu trúc

```text
src/
└── backend/
    ├── dormitory_domain/          # entity, enum, business rules
    ├── dormitory_application/     # schema, interface, use case
    ├── dormitory_infrastructure/  # stored SQL, migration, auth, seed
    ├── dormitory_api/             # FastAPI router, middleware, authorization
    ├── alembic.ini
    └── pyproject.toml

tests/
├── unit/
└── integration/
```

Các module backend theo kế hoạch gồm Contracts, Utilities, Billing, Violations và AI;
không triển khai Reports/dashboard trong MVP này.

## Chạy dự án

### 1. Backend

```bash
cp .env.example .env
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -e "src/backend[dev]"
docker compose up -d postgres
cd src/backend
alembic upgrade head
python -m dormitory_infrastructure.identity.seed_cli
uvicorn dormitory_api.main:app --reload
```

API chạy tại `http://localhost:8000`; Swagger UI tại `http://localhost:8000/docs`.

## Truy vấn SQL trong PostgreSQL

API danh sách tài khoản `GET /api/v1/users` là một ví dụ truy vấn bằng PostgreSQL function:

```text
API /users → IdentityReadRepository.list_users(role)
           → SELECT * FROM public.fn_list_users(:role)
           → PostgreSQL
```

Định nghĩa SQL nằm trong `src/backend/dormitory_infrastructure/persistence/sql/`.
Các migration `20260928_0011`–`20260928_0019` cài function vào PostgreSQL khi chạy
`alembic upgrade head`. Hiện các API tài khoản/xác thực, sinh viên, tòa nhà/phòng/giường,
đăng ký và hợp đồng gọi stored function qua repository; PostgreSQL giữ phần truy vấn
và các thao tác ghi tương ứng. Test tích hợp cần một PostgreSQL test database riêng;
không có nhánh SQLite hay ORM.
Tham số `role` là tùy chọn; ví dụ `GET /api/v1/users?role=Student`.
API kiểm tra vai trò `Admin` và trả kết quả `UserRead`.

Có thể tối ưu SQL bằng `CREATE OR REPLACE FUNCTION` trực tiếp trong PostgreSQL
mà không đổi API, miễn là giữ nguyên tên function, tham số, cột trả về và ngữ nghĩa
mã kết quả/lỗi. Sau khi thử trong database, ghi lại định nghĩa mới trong file SQL
và thêm migration mới để các môi trường khác nhận cùng thay đổi. API điện/nước
và hóa đơn gọi các stored function cài bởi migration `20261004_0021`; phép tính
tiền điện/nước thuần nghiệp vụ vẫn nằm trong Python. Không có ánh xạ model ORM.

## Tài khoản demo tuần 1

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@dormitory.local` | `Admin@123` |
| Staff | `staff@dormitory.local` | `Staff@123` |
| Student | `student@dormitory.local` | `Student@123` |

Chỉ dùng các mật khẩu này cho môi trường phát triển.

## Phạm vi hoàn thành tuần 1–3

- Docker Compose cho PostgreSQL và migration đầu tiên.
- Seed ba role và một tài khoản demo cho mỗi role.
- API đăng nhập, đăng xuất, xem người dùng hiện tại; JWT + role guard.
- F01–F04: CRUD tòa nhà, loại phòng, phòng, giường.
- F05: room matrix; trạng thái giường là dữ liệu suy ra, không nhận từ request.
- Test tích hợp luồng demo cuối tuần 1.
- F06–F07: Sinh viên gửi đăng ký; Staff/Admin lọc, duyệt hoặc từ chối kèm lý do.
- F08: Phân giường và tạo hợp đồng trong một transaction; khóa giường và chặn
  trùng khoảng thời gian bằng lỗi `BED_ASSIGNMENT_CONFLICT`.
- F09: Sinh viên/Staff xem hợp đồng và toàn bộ lịch sử phân giường.
- F10–F11: Chuyển giường giữ lịch sử; chấm dứt hợp đồng giải phóng giường.
- Room matrix suy ra đủ `Available`, `Occupied`, `Maintenance` từ assignment thực tế.
- Integration test bao phủ luồng tuần 2 từ đăng ký đến chấm dứt.
- F12: quản lý biểu giá điện/nước theo thời gian, đồng giá hoặc lũy tiến nhiều bậc.
- F13: ghi chỉ số thủ công, chặn chỉ số hiện tại nhỏ hơn chỉ số trước và lưu snapshot biểu giá.
- F15: bộ tính tiền điện/nước độc lập, có unit test cho biên bậc giá và làm tròn.
- F16: sinh hóa đơn gồm tiền phòng, điện, nước; khóa idempotency ngăn tạo trùng cùng kỳ.
- API tuần 3 được công khai tại `/api/v1`; `/api` tiếp tục được giữ để tương thích.

## API chính tuần 3

| Method | Endpoint | Chức năng |
|---|---|---|
| GET/POST | `/api/v1/utility-tariffs` | Danh sách và tạo biểu giá |
| GET/POST | `/api/v1/meters` | Danh sách và gắn công tơ vào phòng |
| GET/POST | `/api/v1/meter-readings` | Xem và ghi chỉ số thủ công |
| GET | `/api/v1/bills` | Danh sách hóa đơn |
| POST | `/api/v1/bills/generate` | Sinh hóa đơn chống trùng |

## API chính tuần 2

| Method | Endpoint | Vai trò |
|---|---|---|
| POST | `/api/housing-applications` | Student |
| GET | `/api/housing-applications?status=` | Student xem của mình; Admin/Staff xem toàn bộ |
| POST | `/api/housing-applications/{id}/approve` | Admin/Staff |
| POST | `/api/housing-applications/{id}/reject` | Admin/Staff |
| POST | `/api/contracts/{applicationId}/assign-bed` | Admin/Staff |
| GET | `/api/contracts`, `/api/contracts/me` | Theo quyền sở hữu |
| GET | `/api/contracts/{id}/assignment-history` | Theo quyền sở hữu |
| POST | `/api/contracts/{id}/transfer` | Admin/Staff |
| POST | `/api/contracts/{id}/terminate` | Admin/Staff |

## Kiểm tra

```bash
# Unit test chạy không cần database; integration test chỉ chạy khi có TEST_DATABASE_URL
cd src/backend
pytest
```

Đặt `TEST_DATABASE_URL` trỏ đến **database PostgreSQL riêng cho test**, khác
`DATABASE_URL`. Fixture sẽ chạy migration và xóa dữ liệu trong 17 bảng của database
test trước mỗi ca kiểm thử; nếu không đặt biến này, integration test sẽ được skip.
````

## File: `docker-compose.yml`

SHA-256: `87ad9acad379b23eaf9b356aa134ad3cf5c212a8c7ff6217097ee6aa9fbea952`  
Dòng: 53

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: dormitory
      POSTGRES_USER: dormitory
      POSTGRES_PASSWORD: changeme
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dormitory -d dormitory"]
      interval: 5s
      timeout: 5s
      retries: 10

  api:
    build:
      context: .
      dockerfile: Dockerfile
    mem_limit: 2g
    memswap_limit: 2g
    environment:
      DATABASE_URL: postgresql+psycopg://dormitory:changeme@postgres:5432/dormitory
      SECRET_KEY: local-development-secret-change-before-production
      JWT_ISSUER: dormitory-api
      JWT_AUDIENCE: dormitory-client
      ACCESS_TOKEN_EXPIRE_MINUTES: 15
      REFRESH_TOKEN_EXPIRE_DAYS: 7
      CORS_ORIGINS: ""
    command:
      - /bin/sh
      - -c
      - >-
        alembic upgrade head &&
        python -m dormitory_infrastructure.identity.seed_cli &&
        uvicorn dormitory_api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

  adminer:
    image: adminer:latest
    restart: always
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

## File: `scripts/dev-up.sh`

SHA-256: `4723cb7eecf0f0ea4a51a5b5b02ca6cdfbbf3ae0163aaa8dd0bbe844040f84a7`  
Dòng: 7

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"
docker compose up -d postgres
echo "PostgreSQL đang chạy tại localhost:5432."
```

## File: `scripts/migrate.sh`

SHA-256: `31d0913695887bfcb2d38d282a440b04d82f7ed92b21d7af0ce304e0e9a3731a`  
Dòng: 6

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root/src/backend"
python -m alembic upgrade head
```

## File: `scripts/render-erd.ps1`

SHA-256: `6d209325607bc1a22694037ee3aeb57e0b1fbf5507b3a3c13bbc25ff265a17d4`  
Dòng: 315

````powershell
param(
    [string]$InputMarkdown = "docs/ERD_33_BANG_POSTGRESQL.md",
    [string]$OutputSvg = "docs/ERD_33_BANG_POSTGRESQL.svg",
    [string]$OutputPng = "docs/ERD_33_BANG_POSTGRESQL.png"
)

$ErrorActionPreference = "Stop"

function Escape-Xml([string]$Value) {
    return [System.Security.SecurityElement]::Escape($Value)
}

$content = Get-Content -LiteralPath $InputMarkdown -Raw -Encoding UTF8
$match = [regex]::Match($content, '(?s)```mermaid\s*(erDiagram.*?)```')
if (-not $match.Success) {
    throw "Mermaid erDiagram block not found in $InputMarkdown"
}

$tables = [ordered]@{}
$relationships = [System.Collections.Generic.List[object]]::new()
$currentTable = $null

foreach ($rawLine in ($match.Groups[1].Value -split "`r?`n")) {
    $line = $rawLine.Trim()
    if (-not $line -or $line -eq "erDiagram") {
        continue
    }
    if ($line -match '^([A-Za-z0-9_]+)\s*\{$') {
        $currentTable = $Matches[1]
        $tables[$currentTable] = [System.Collections.Generic.List[object]]::new()
        continue
    }
    if ($line -eq '}') {
        $currentTable = $null
        continue
    }
    if ($null -ne $currentTable) {
        if ($line -match '^([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)(?:\s+(.+))?$') {
            $tables[$currentTable].Add([pscustomobject]@{
                Type = $Matches[1]
                Name = $Matches[2]
                Keys = if ($Matches.Count -ge 4) { $Matches[3] } else { "" }
            })
        }
        continue
    }
    if ($line -match '^([A-Za-z0-9_]+)\s+(\S+)\s+([A-Za-z0-9_]+)\s*:\s*(.+)$') {
        $relationships.Add([pscustomobject]@{
            Parent = $Matches[1]
            Cardinality = $Matches[2]
            Child = $Matches[3]
            Label = $Matches[4]
        })
    }
}

$modules = [ordered]@{
    Identity = @('roles', 'permissions', 'role_permissions', 'users', 'student_profiles')
    Housing = @('buildings', 'room_types', 'rooms', 'beds')
    Contracts = @('housing_applications', 'contracts', 'bed_assignments', 'room_transfer_requests', 'contract_events')
    Utilities = @('utilities', 'meters', 'utility_tariffs', 'tariff_tiers', 'utility_import_batches', 'meter_readings')
    Billing = @('bills', 'bill_items', 'payments')
    Violations = @('violation_types', 'violations', 'violation_evidences')
    Maintenance = @('maintenance_requests', 'maintenance_events', 'maintenance_plans')
    Notifications = @('notifications', 'notification_targets', 'notification_reads')
    Files = @('stored_files')
}

$moduleLane = @{
    Identity = 0
    Files = 0
    Housing = 1
    Contracts = 1
    Utilities = 2
    Billing = 3
    Violations = 3
    Maintenance = 4
    Notifications = 4
}

$moduleColors = @{
    Identity = '#2563eb'
    Housing = '#059669'
    Contracts = '#7c3aed'
    Utilities = '#0891b2'
    Billing = '#d97706'
    Violations = '#dc2626'
    Maintenance = '#4f46e5'
    Notifications = '#be185d'
    Files = '#475569'
}

$tableWidth = 510
$laneGap = 135
$leftMargin = 55
$topMargin = 75
$moduleTitleHeight = 30
$tableHeaderHeight = 31
$rowHeight = 19
$tablePaddingBottom = 9
$tableGap = 22
$moduleGap = 42
$positions = @{}
$laneY = @( $topMargin, $topMargin, $topMargin, $topMargin, $topMargin )
$moduleTitles = [System.Collections.Generic.List[object]]::new()

foreach ($moduleName in $modules.Keys) {
    $lane = $moduleLane[$moduleName]
    $x = $leftMargin + ($lane * ($tableWidth + $laneGap))
    $moduleTitles.Add([pscustomobject]@{ Module = $moduleName; X = $x; Y = $laneY[$lane] })
    $laneY[$lane] += $moduleTitleHeight
    foreach ($tableName in $modules[$moduleName]) {
        if (-not $tables.Contains($tableName)) {
            throw "Table $tableName does not exist in Mermaid"
        }
        $height = $tableHeaderHeight + ($tables[$tableName].Count * $rowHeight) + $tablePaddingBottom
        $positions[$tableName] = [pscustomobject]@{
            X = $x
            Y = $laneY[$lane]
            Width = $tableWidth
            Height = $height
            Module = $moduleName
        }
        $laneY[$lane] += $height + $tableGap
    }
    $laneY[$lane] += $moduleGap
}

$canvasWidth = $leftMargin * 2 + (5 * $tableWidth) + (4 * $laneGap)
$canvasHeight = ([Linq.Enumerable]::Max([int[]]$laneY)) + 45

$svg = [System.Text.StringBuilder]::new()
[void]$svg.AppendLine("<svg xmlns=`"http://www.w3.org/2000/svg`" width=`"$canvasWidth`" height=`"$canvasHeight`" viewBox=`"0 0 $canvasWidth $canvasHeight`">")
[void]$svg.AppendLine('<defs><filter id="shadow" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.14"/></filter><marker id="crow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L11,6 L1,11 M1,6 L11,6" fill="none" stroke="#64748b" stroke-width="1.2"/></marker></defs>')
[void]$svg.AppendLine('<rect width="100%" height="100%" fill="#f8fafc"/>')
[void]$svg.AppendLine('<text x="55" y="36" font-family="Segoe UI,Arial,sans-serif" font-size="23" font-weight="600" fill="#0f172a">Dormitory Management - PostgreSQL ERD (33 tables)</text>')
[void]$svg.AppendLine('<text x="55" y="58" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="#64748b">PK = Primary Key | FK = Foreign Key | UK = Unique Key | Alembic head 20260921_0009</text>')

# Draw relationships behind tables.
foreach ($rel in $relationships) {
    if (-not $positions.ContainsKey($rel.Parent) -or -not $positions.ContainsKey($rel.Child)) {
        continue
    }
    $p = $positions[$rel.Parent]
    $c = $positions[$rel.Child]
    $pCenterY = $p.Y + ($p.Height / 2)
    $cCenterY = $c.Y + ($c.Height / 2)
    if ($p.X -lt $c.X) {
        $x1 = $p.X + $p.Width
        $x2 = $c.X
        $bend = [Math]::Max(55, ($x2 - $x1) / 2)
        $d = "M $x1 $pCenterY C $($x1 + $bend) $pCenterY, $($x2 - $bend) $cCenterY, $x2 $cCenterY"
    } elseif ($p.X -gt $c.X) {
        $x1 = $p.X
        $x2 = $c.X + $c.Width
        $bend = [Math]::Max(55, ($x1 - $x2) / 2)
        $d = "M $x1 $pCenterY C $($x1 - $bend) $pCenterY, $($x2 + $bend) $cCenterY, $x2 $cCenterY"
    } else {
        $x1 = $p.X + $p.Width
        $x2 = $c.X + $c.Width
        $outsideX = $x1 + 42 + (($relationships.IndexOf($rel) % 4) * 10)
        $d = "M $x1 $pCenterY C $outsideX $pCenterY, $outsideX $cCenterY, $x2 $cCenterY"
    }
    [void]$svg.AppendLine("<path d=`"$d`" fill=`"none`" stroke=`"#94a3b8`" stroke-width=`"1.35`" opacity=`"0.72`" marker-end=`"url(#crow)`"/>")
}

foreach ($moduleTitle in $moduleTitles) {
    $color = $moduleColors[$moduleTitle.Module]
    $title = Escape-Xml $moduleTitle.Module
    [void]$svg.AppendLine("<text x=`"$($moduleTitle.X)`" y=`"$($moduleTitle.Y + 20)`" font-family=`"Segoe UI,Arial,sans-serif`" font-size=`"17`" font-weight=`"600`" fill=`"$color`">$title</text>")
}

foreach ($tableName in $tables.Keys) {
    if (-not $positions.ContainsKey($tableName)) {
        continue
    }
    $pos = $positions[$tableName]
    $color = $moduleColors[$pos.Module]
    [void]$svg.AppendLine("<g filter=`"url(#shadow)`">")
    [void]$svg.AppendLine("<rect x=`"$($pos.X)`" y=`"$($pos.Y)`" width=`"$($pos.Width)`" height=`"$($pos.Height)`" rx=`"4`" fill=`"#ffffff`" stroke=`"#cbd5e1`"/>")
    [void]$svg.AppendLine("<path d=`"M $($pos.X + 4) $($pos.Y) H $($pos.X + $pos.Width - 4) Q $($pos.X + $pos.Width) $($pos.Y) $($pos.X + $pos.Width) $($pos.Y + 4) V $($pos.Y + $tableHeaderHeight) H $($pos.X) V $($pos.Y + 4) Q $($pos.X) $($pos.Y) $($pos.X + 4) $($pos.Y)`" fill=`"$color`"/>")
    $escapedTable = Escape-Xml $tableName
    [void]$svg.AppendLine("<text x=`"$($pos.X + 12)`" y=`"$($pos.Y + 21)`" font-family=`"Consolas,Segoe UI,Arial,sans-serif`" font-size=`"14`" font-weight=`"600`" fill=`"#ffffff`">$escapedTable</text>")
    $rowIndex = 0
    foreach ($field in $tables[$tableName]) {
        $rowY = $pos.Y + $tableHeaderHeight + ($rowIndex * $rowHeight)
        if (($rowIndex % 2) -eq 1) {
            [void]$svg.AppendLine("<rect x=`"$($pos.X + 1)`" y=`"$rowY`" width=`"$($pos.Width - 2)`" height=`"$rowHeight`" fill=`"#f8fafc`"/>")
        }
        $keyText = Escape-Xml $field.Keys
        $typeText = Escape-Xml $field.Type
        $nameText = Escape-Xml $field.Name
        $keyColor = if ($field.Keys -match 'PK') { '#b45309' } elseif ($field.Keys -match 'FK') { '#7c3aed' } else { '#64748b' }
        [void]$svg.AppendLine("<text x=`"$($pos.X + 10)`" y=`"$($rowY + 14)`" font-family=`"Consolas,monospace`" font-size=`"11`" font-weight=`"600`" fill=`"$keyColor`">$keyText</text>")
        [void]$svg.AppendLine("<text x=`"$($pos.X + 76)`" y=`"$($rowY + 14)`" font-family=`"Consolas,monospace`" font-size=`"12`" fill=`"#0f172a`">$nameText</text>")
        [void]$svg.AppendLine("<text x=`"$($pos.X + $pos.Width - 10)`" y=`"$($rowY + 14)`" text-anchor=`"end`" font-family=`"Consolas,monospace`" font-size=`"11`" fill=`"#64748b`">$typeText</text>")
        $rowIndex++
    }
    [void]$svg.AppendLine('</g>')
}

[void]$svg.AppendLine('</svg>')
[System.IO.File]::WriteAllText((Join-Path (Get-Location) $OutputSvg), $svg.ToString(), [System.Text.UTF8Encoding]::new($false))

# Render a large PNG using System.Drawing for easy viewing in ordinary image viewers.
Add-Type -AssemblyName System.Drawing
$bitmap = [System.Drawing.Bitmap]::new($canvasWidth, $canvasHeight)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$graphics.Clear([System.Drawing.ColorTranslator]::FromHtml('#f8fafc'))

$titleFont = [System.Drawing.Font]::new('Segoe UI', 17, [System.Drawing.FontStyle]::Bold)
$subtitleFont = [System.Drawing.Font]::new('Segoe UI', 9)
$moduleFont = [System.Drawing.Font]::new('Segoe UI', 13, [System.Drawing.FontStyle]::Bold)
$headerFont = [System.Drawing.Font]::new('Consolas', 10, [System.Drawing.FontStyle]::Bold)
$fieldFont = [System.Drawing.Font]::new('Consolas', 8)
$keyFont = [System.Drawing.Font]::new('Consolas', 7, [System.Drawing.FontStyle]::Bold)
$darkBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#0f172a'))
$mutedBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#64748b'))
$whiteBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
$tableBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
$alternateBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#f8fafc'))
$borderPen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#cbd5e1'), 1)
$relationPen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#94a3b8'), 1.2)

$graphics.DrawString('Dormitory Management - PostgreSQL ERD (33 tables)', $titleFont, $darkBrush, 55, 13)
$graphics.DrawString('PK = Primary Key | FK = Foreign Key | UK = Unique Key | Alembic head 20260921_0009', $subtitleFont, $mutedBrush, 55, 43)

foreach ($rel in $relationships) {
    if (-not $positions.ContainsKey($rel.Parent) -or -not $positions.ContainsKey($rel.Child)) {
        continue
    }
    $p = $positions[$rel.Parent]
    $c = $positions[$rel.Child]
    $y1 = [single]($p.Y + ($p.Height / 2))
    $y2 = [single]($c.Y + ($c.Height / 2))
    if ($p.X -lt $c.X) {
        $x1 = [single]($p.X + $p.Width)
        $x2 = [single]$c.X
        $bend = [single][Math]::Max(55, ($x2 - $x1) / 2)
        $graphics.DrawBezier($relationPen, $x1, $y1, $x1 + $bend, $y1, $x2 - $bend, $y2, $x2, $y2)
    } elseif ($p.X -gt $c.X) {
        $x1 = [single]$p.X
        $x2 = [single]($c.X + $c.Width)
        $bend = [single][Math]::Max(55, ($x1 - $x2) / 2)
        $graphics.DrawBezier($relationPen, $x1, $y1, $x1 - $bend, $y1, $x2 + $bend, $y2, $x2, $y2)
    } else {
        $x1 = [single]($p.X + $p.Width)
        $x2 = [single]($c.X + $c.Width)
        $outsideX = [single]($x1 + 55)
        $graphics.DrawBezier($relationPen, $x1, $y1, $outsideX, $y1, $outsideX, $y2, $x2, $y2)
    }
}

foreach ($moduleTitle in $moduleTitles) {
    $moduleBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($moduleColors[$moduleTitle.Module]))
    $graphics.DrawString($moduleTitle.Module, $moduleFont, $moduleBrush, $moduleTitle.X, $moduleTitle.Y)
    $moduleBrush.Dispose()
}

foreach ($tableName in $tables.Keys) {
    if (-not $positions.ContainsKey($tableName)) {
        continue
    }
    $pos = $positions[$tableName]
    $headerBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($moduleColors[$pos.Module]))
    $graphics.FillRectangle($tableBrush, $pos.X, $pos.Y, $pos.Width, $pos.Height)
    $graphics.DrawRectangle($borderPen, $pos.X, $pos.Y, $pos.Width, $pos.Height)
    $graphics.FillRectangle($headerBrush, $pos.X, $pos.Y, $pos.Width, $tableHeaderHeight)
    $graphics.DrawString($tableName, $headerFont, $whiteBrush, $pos.X + 10, $pos.Y + 7)
    $rowIndex = 0
    foreach ($field in $tables[$tableName]) {
        $rowY = $pos.Y + $tableHeaderHeight + ($rowIndex * $rowHeight)
        if (($rowIndex % 2) -eq 1) {
            $graphics.FillRectangle($alternateBrush, $pos.X + 1, $rowY, $pos.Width - 2, $rowHeight)
        }
        $keyBrush = if ($field.Keys -match 'PK') {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#b45309'))
        } elseif ($field.Keys -match 'FK') {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#7c3aed'))
        } else {
            [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#64748b'))
        }
        $graphics.DrawString($field.Keys, $keyFont, $keyBrush, $pos.X + 8, $rowY + 4)
        $graphics.DrawString($field.Name, $fieldFont, $darkBrush, $pos.X + 74, $rowY + 3)
        $typeSize = $graphics.MeasureString($field.Type, $fieldFont)
        $graphics.DrawString($field.Type, $fieldFont, $mutedBrush, $pos.X + $pos.Width - $typeSize.Width - 8, $rowY + 3)
        $keyBrush.Dispose()
        $rowIndex++
    }
    $headerBrush.Dispose()
}

$bitmap.Save((Join-Path (Get-Location) $OutputPng), [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()
$titleFont.Dispose()
$subtitleFont.Dispose()
$moduleFont.Dispose()
$headerFont.Dispose()
$fieldFont.Dispose()
$keyFont.Dispose()
$darkBrush.Dispose()
$mutedBrush.Dispose()
$whiteBrush.Dispose()
$tableBrush.Dispose()
$alternateBrush.Dispose()
$borderPen.Dispose()
$relationPen.Dispose()

Write-Output "Rendered $($tables.Count) tables and $($relationships.Count) relationships."
Write-Output "SVG: $OutputSvg"
Write-Output "PNG: $OutputPng"
````

## File: `scripts/seed.sh`

SHA-256: `b6bcf51603a00d2f5d4aaad54233d26e84f698f67c142415a81186a85bf19275`  
Dòng: 6

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root/src/backend"
python -m dormitory_infrastructure.identity.seed_cli
```

## File: `src/backend/alembic.ini`

SHA-256: `7edcdfa64a1291edadc29f11897c25550a478ff05b8a6f33c905d0d159e89c64`  
Dòng: 39

```ini
[alembic]
script_location = dormitory_infrastructure/persistence/migrations
prepend_sys_path = .
path_separator = os
sqlalchemy.url = postgresql+psycopg://dormitory:changeme@localhost:5432/dormitory

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## File: `src/backend/dormitory_api/__init__.py`

SHA-256: `0f5e0c9cbfeaa5724c507a81e8da80e1a3b75d55795f307ff5d6df99a2fbb1ec`  
Dòng: 1

```python
"""FastAPI delivery layer."""
```

## File: `src/backend/dormitory_api/authorization/__init__.py`

SHA-256: `358e9436f4de214d81dc85965ec7d21224f29c5e5ef1f69b3468403e22055ac7`  
Dòng: 3

```python
from dormitory_api.dependencies import admin_only, admin_or_staff, require_roles

__all__ = ["admin_only", "admin_or_staff", "require_roles"]
```

## File: `src/backend/dormitory_api/controllers/__init__.py`

SHA-256: `6de724a412084c70361ebca2810092e8a5be2f47e4b073a42e730a01c97b9ee2`  
Dòng: 17

```python
from .auth import router as auth_router
from .billing import router as billing_router
from .contracts import router as contracts_router
from .housing import router as housing_router
from .identity import router as identity_router
from .students import router as students_router
from .utilities import router as utilities_router

__all__ = [
    "auth_router",
    "billing_router",
    "contracts_router",
    "housing_router",
    "identity_router",
    "students_router",
    "utilities_router",
]
```

## File: `src/backend/dormitory_api/controllers/auth.py`

SHA-256: `5f9e72c518e8310cd172af8d72c6cf7482ae0ecb3ecf6074e417278fed6e8d74`  
Dòng: 162

```python
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import get_current_user
from dormitory_application.identity import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserRead,
)
from dormitory_infrastructure.identity import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthRepository, AuthUser
from dormitory_infrastructure.persistence.config import get_settings

router = APIRouter(prefix="/auth", tags=["Auth"])


def _user_read(user: AuthUser) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name,
        is_active=user.is_active,
    )


def _birth_date_for_age(age: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - age)
    except ValueError:
        return date(today.year - age, 2, 28)


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _issue_tokens(user: AuthUser, repository: AuthRepository) -> tuple[str, str]:
    settings = get_settings()
    refresh_token = create_refresh_token()
    repository.set_refresh_token(
        user.id,
        hash_refresh_token(refresh_token),
        datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days),
    )
    access_token = create_access_token(str(user.id), user.role.name, user.email)
    return access_token, refresh_token


def _token_response(user: AuthUser, access_token: str, refresh_token: str) -> TokenResponse:
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=get_settings().access_token_expire_minutes * 60,
        user=_user_read(user),
    )


def _invalid_credentials() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "errorCode": "AUTH_INVALID_CREDENTIALS",
            "message": "Email hoặc mật khẩu không đúng.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def _invalid_refresh_token() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "errorCode": "AUTH_INVALID_REFRESH_TOKEN",
            "message": "Refresh token không hợp lệ hoặc đã hết hạn.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Connection = Depends(get_db)) -> UserRead:
    repository = AuthRepository(db)
    try:
        user_id = repository.register_student(
            payload.email, payload.full_name.strip(), hash_password(payload.password),
            payload.student_code.upper(), _birth_date_for_age(payload.age),
        )
        if user_id is None:
            raise HTTPException(status_code=500, detail="Student role has not been seeded.")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "errorCode": "STUDENT_ALREADY_EXISTS",
                "message": "Email hoặc mã sinh viên đã được sử dụng.",
            },
        ) from exc
    return _user_read(repository.find_user(user_id=user_id))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Connection = Depends(get_db)) -> TokenResponse:
    repository = AuthRepository(db)
    user = repository.find_user(email=payload.email)
    succeeded = bool(
        user is not None
        and user.is_active
        and verify_password(payload.password, user.password_hash)
    )
    if not succeeded or user is None:
        raise _invalid_credentials()
    access_token, refresh_token = _issue_tokens(user, repository)
    db.commit()
    return _token_response(user, access_token, refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Connection = Depends(get_db)) -> TokenResponse:
    repository = AuthRepository(db)
    user = repository.find_user(
        refresh_hash=hash_refresh_token(payload.refresh_token)
    )
    now = datetime.now(UTC)
    if (
        user is None
        or not user.is_active
        or user.refresh_token_revoked_at is not None
        or user.refresh_token_expires_at is None
        or _as_utc(user.refresh_token_expires_at) <= now
    ):
        raise _invalid_refresh_token()
    access_token, refresh_token = _issue_tokens(user, repository)
    db.commit()
    return _token_response(user, access_token, refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)) -> None:
    AuthRepository(db).revoke_refresh_token(user.id, datetime.now(UTC))
    db.commit()
    return None


@router.get("/me", response_model=UserRead)
def me(user: AuthUser = Depends(get_current_user)) -> UserRead:
    return _user_read(user)
```

## File: `src/backend/dormitory_api/controllers/billing.py`

SHA-256: `517c5f69890da0d91411f66a5f47761ee758bf9e94e045a608a7722a4d921987`  
Dòng: 34

```python
from uuid import UUID

from fastapi import APIRouter, Depends

from dormitory_api.dependencies import admin_or_staff, get_billing_service, get_current_user
from dormitory_application.billing import BillGenerateRequest, BillRead, BillingService
from dormitory_infrastructure.persistence.repositories import AuthUser

router = APIRouter(tags=["Billing"])
read_access = get_current_user
generate_access = admin_or_staff


@router.get("/bills", response_model=list[BillRead], dependencies=[Depends(read_access)])
def list_bills(
    contract_id: UUID | None = None,
    user: AuthUser = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.list_bills(user.id, user.role.name, contract_id)


@router.post(
    "/bills/generate",
    response_model=BillRead,
    status_code=201,
    dependencies=[Depends(generate_access)],
)
def generate_bill(
    payload: BillGenerateRequest,
    user: AuthUser = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.generate(payload, user.id)
```

## File: `src/backend/dormitory_api/controllers/contracts.py`

SHA-256: `5ed30061343ba2c605c1218e3cae62a319355e6015604feb86320b2701e1b52f`  
Dòng: 153

```python
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from dormitory_application.contracts import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    ContractService,
    HousingApplicationCreate,
    HousingApplicationRead,
    HousingApplicationReject,
    TerminateContractRequest,
    TransferBedRequest,
)
from dormitory_infrastructure.persistence.repositories import AuthUser

from dormitory_api.dependencies import (
    admin_or_staff,
    get_contract_service,
    get_current_user,
)

router = APIRouter(tags=["Contracts"])


@router.post("/housing-applications", response_model=HousingApplicationRead, status_code=201)
def create_application(
    payload: HousingApplicationCreate,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    if user.role.name != "Student":
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail={"errorCode": "STUDENT_ONLY", "message": "Chỉ sinh viên được gửi đăng ký."},
        )
    return service.create_application(user.id, payload)


@router.get("/housing-applications", response_model=list[HousingApplicationRead])
def list_applications(
    status: str | None = None,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.list_applications(user.id, user.role.name, status)


@router.post(
    "/housing-applications/{application_id}/approve",
    response_model=HousingApplicationRead,
    dependencies=[Depends(admin_or_staff)],
)
def approve_application(
    application_id: UUID,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.approve_application(application_id, user.id)


@router.post(
    "/housing-applications/{application_id}/reject",
    response_model=HousingApplicationRead,
    dependencies=[Depends(admin_or_staff)],
)
def reject_application(
    application_id: UUID,
    payload: HousingApplicationReject,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.reject_application(application_id, user.id, payload.reason)


@router.post(
    "/contracts/{application_id}/assign-bed",
    response_model=ContractRead,
    status_code=201,
    dependencies=[Depends(admin_or_staff)],
)
def assign_bed(
    application_id: UUID,
    payload: AssignBedRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.assign_bed(application_id, payload)


@router.get("/contracts", response_model=list[ContractRead])
def list_contracts(
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.list_contracts(user.id, user.role.name)


@router.get("/contracts/me", response_model=ContractRead | None)
def my_contract(
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_my_contract(user.id)


@router.get("/contracts/{contract_id}", response_model=ContractRead)
def get_contract(
    contract_id: UUID,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_contract(contract_id, user.id, user.role.name)


@router.get(
    "/contracts/{contract_id}/assignment-history",
    response_model=list[BedAssignmentRead],
)
def assignment_history(
    contract_id: UUID,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.assignment_history(contract_id, user.id, user.role.name)


@router.post(
    "/contracts/{contract_id}/transfer",
    response_model=ContractRead,
    dependencies=[Depends(admin_or_staff)],
)
def transfer(
    contract_id: UUID,
    payload: TransferBedRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.transfer(contract_id, payload)


@router.post(
    "/contracts/{contract_id}/terminate",
    response_model=ContractRead,
    dependencies=[Depends(admin_or_staff)],
)
def terminate(
    contract_id: UUID,
    payload: TerminateContractRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.terminate(contract_id, payload.termination_date)
```

## File: `src/backend/dormitory_api/controllers/housing.py`

SHA-256: `113bbe59cb66cce7e5717a3fbdaf007944ef066b468c8b199c2160b40e4281f7`  
Dòng: 123

```python
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from dormitory_application.housing import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    HousingService,
    RoomCreate,
    RoomMatrixBuilding,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)

from dormitory_api.dependencies import (
    admin_only,
    admin_or_staff,
    get_current_user,
    get_housing_service,
)

router = APIRouter(tags=["Housing"])


@router.get("/buildings", response_model=list[BuildingRead], dependencies=[Depends(admin_or_staff)])
def list_buildings(service: HousingService = Depends(get_housing_service)):
    return service.list_buildings()


@router.get("/buildings/{item_id}", response_model=BuildingRead, dependencies=[Depends(admin_or_staff)])
def get_building(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    return service.get_building(item_id)


@router.post("/buildings", response_model=BuildingRead, status_code=201, dependencies=[Depends(admin_only)])
def create_building(payload: BuildingCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_building(payload)


@router.put("/buildings/{item_id}", response_model=BuildingRead, dependencies=[Depends(admin_only)])
def update_building(item_id: UUID, payload: BuildingUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_building(item_id, payload)


@router.delete("/buildings/{item_id}", status_code=204, dependencies=[Depends(admin_only)])
def delete_building(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_building(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/room-types", response_model=list[RoomTypeRead], dependencies=[Depends(get_current_user)])
def list_room_types(service: HousingService = Depends(get_housing_service)):
    return service.list_room_types()


@router.post("/room-types", response_model=RoomTypeRead, status_code=201, dependencies=[Depends(admin_only)])
def create_room_type(payload: RoomTypeCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_room_type(payload)


@router.put("/room-types/{item_id}", response_model=RoomTypeRead, dependencies=[Depends(admin_only)])
def update_room_type(item_id: UUID, payload: RoomTypeUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_room_type(item_id, payload)


@router.delete("/room-types/{item_id}", status_code=204, dependencies=[Depends(admin_only)])
def delete_room_type(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_room_type(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/rooms", response_model=list[RoomRead], dependencies=[Depends(admin_or_staff)])
def list_rooms(buildingId: UUID | None = None, service: HousingService = Depends(get_housing_service)):
    return service.list_rooms(buildingId)


@router.post("/rooms", response_model=RoomRead, status_code=201, dependencies=[Depends(admin_or_staff)])
def create_room(payload: RoomCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_room(payload)


@router.put("/rooms/{item_id}", response_model=RoomRead, dependencies=[Depends(admin_or_staff)])
def update_room(item_id: UUID, payload: RoomUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_room(item_id, payload)


@router.delete("/rooms/{item_id}", status_code=204, dependencies=[Depends(admin_or_staff)])
def delete_room(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_room(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/beds", response_model=list[BedRead], dependencies=[Depends(admin_or_staff)])
def list_beds(roomId: UUID | None = None, service: HousingService = Depends(get_housing_service)):
    return service.list_beds(roomId)


@router.post("/beds", response_model=BedRead, status_code=201, dependencies=[Depends(admin_or_staff)])
def create_bed(payload: BedCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_bed(payload)


@router.put("/beds/{item_id}", response_model=BedRead, dependencies=[Depends(admin_or_staff)])
def update_bed(item_id: UUID, payload: BedUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_bed(item_id, payload)


@router.delete("/beds/{item_id}", status_code=204, dependencies=[Depends(admin_or_staff)])
def delete_bed(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_bed(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/room-matrix", response_model=list[RoomMatrixBuilding], dependencies=[Depends(admin_or_staff)])
def room_matrix(service: HousingService = Depends(get_housing_service)):
    return service.room_matrix()
```

## File: `src/backend/dormitory_api/controllers/identity.py`

SHA-256: `430ce0a7c1c3ad28b7db93318f150e2924998bf9d6e58f7d1bbd085a5f5337a8`  
Dòng: 86

```python
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import admin_only, get_current_user
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import (
    ResetPasswordRequest,
    StudentProfileRead,
    StudentProfileUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthUser, IdentityRepository

router = APIRouter(tags=["Identity"])


@router.get("/users", response_model=list[UserRead], dependencies=[Depends(admin_only)])
def list_users(role: str | None = None, db: Connection = Depends(get_db)):
    return [UserRead(**item) for item in IdentityRepository(db).list_users(role)]


@router.post("/users", response_model=UserRead, status_code=201, dependencies=[Depends(admin_only)])
def create_user(payload: UserCreate, actor: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    repository = IdentityRepository(db)
    try:
        user_id = repository.create_user(
            payload.email.strip().lower(), payload.full_name.strip(),
            hash_password(payload.password), payload.role,
        )
        if user_id is None:
            raise NotFoundError("Role not found")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email đã được sử dụng.") from exc
    return UserRead(**repository.get_user(user_id))


@router.put("/users/{user_id}", response_model=UserRead, dependencies=[Depends(admin_only)])
def update_user(user_id: UUID, payload: UserUpdate, actor: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    repository = IdentityRepository(db)
    if not repository.update_user(
        user_id, payload.full_name.strip(), payload.role, payload.is_active, actor.id,
    ):
        raise NotFoundError("User or role not found")
    db.commit()
    return UserRead(**repository.get_user(user_id))


@router.post("/users/{user_id}/reset-password", status_code=204, dependencies=[Depends(admin_only)])
def reset_password(user_id: UUID, payload: ResetPasswordRequest, actor: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    if not IdentityRepository(db).reset_password(
        user_id, hash_password(payload.new_password), actor.id,
    ):
        raise NotFoundError("User not found")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/student-profile/me", response_model=StudentProfileRead)
def my_profile(user: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    item = IdentityRepository(db).get_profile(user.id)
    if item is None:
        raise NotFoundError("Student profile not found")
    return StudentProfileRead(**item)


@router.put("/student-profile/me", response_model=StudentProfileRead)
def update_my_profile(payload: StudentProfileUpdate, user: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    if user.role.name != "Student":
        raise NotFoundError("Student profile not found")
    repository = IdentityRepository(db)
    try:
        repository.upsert_profile(user.id, payload.model_dump())
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Mã sinh viên đã được sử dụng.") from exc
    return StudentProfileRead(**repository.get_profile(user.id))
```

## File: `src/backend/dormitory_api/controllers/students.py`

SHA-256: `08e94f62f4cc9bab54f306013478bbc71c75ed9b52b4f6fb609c49e94449ebfd`  
Dòng: 99

```python
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import admin_or_staff
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import StudentCreate, StudentPage, StudentRead
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthRepository, StudentRepository

router = APIRouter(prefix="/students", tags=["Students"])


def _birth_date_for_age(age: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - age)
    except ValueError:
        return date(today.year - age, 2, 28)


def _age(birth_date: date | None) -> int | None:
    if birth_date is None:
        return None
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def _student(item: dict[str, object]) -> StudentRead:
    return StudentRead(
        id=item["id"],
        student_code=item["student_code"],
        full_name=item["full_name"],
        age=_age(item["date_of_birth"]),
        email=item["email"],
        is_active=item["is_active"],
    )


@router.get(
    "",
    response_model=StudentPage,
    dependencies=[Depends(admin_or_staff)],
    summary="Lấy danh sách sinh viên có phân trang",
)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    db: Connection = Depends(get_db),
) -> StudentPage:
    repository = StudentRepository(db)
    return StudentPage(
        items=[_student(item) for item in repository.list_students(page_size, (page - 1) * page_size)],
        page=page,
        page_size=page_size,
        total=repository.count_students(),
    )


@router.get(
    "/{student_id}",
    response_model=StudentRead,
    dependencies=[Depends(admin_or_staff)],
    summary="Lấy chi tiết sinh viên",
)
def get_student(student_id: UUID, db: Connection = Depends(get_db)) -> StudentRead:
    item = StudentRepository(db).get_student(student_id)
    if item is None:
        raise NotFoundError("Student not found")
    return _student(item)


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_or_staff)],
    summary="Tạo tài khoản và hồ sơ sinh viên",
)
def create_student(payload: StudentCreate, db: Connection = Depends(get_db)) -> StudentRead:
    try:
        user_id = AuthRepository(db).register_student(
            payload.email, payload.full_name.strip(), hash_password(payload.password),
            payload.student_code.upper(), _birth_date_for_age(payload.age),
        )
        if user_id is None:
            raise NotFoundError("Student role not found")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email hoặc mã sinh viên đã được sử dụng.") from exc
    item = StudentRepository(db).get_student(user_id)
    return _student(item)
```

## File: `src/backend/dormitory_api/controllers/utilities.py`

SHA-256: `d6f84948cca8b340235d4263958c82d320f5a56be03e4edb7c8460dc2eec59f4`  
Dòng: 88

```python
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from dormitory_api.dependencies import admin_or_staff, get_current_user, get_utility_service
from dormitory_application.utilities import (
    MeterCreate,
    MeterRead,
    MeterReadingCreate,
    MeterReadingRead,
    UtilityRead,
    UtilityService,
    UtilityTariffCreate,
    UtilityTariffRead,
)
from dormitory_infrastructure.persistence.repositories import AuthUser

router = APIRouter(tags=["Utilities"])
read_access = get_current_user
manage_access = admin_or_staff


@router.get("/utilities", response_model=list[UtilityRead], dependencies=[Depends(read_access)])
def list_utilities(service: UtilityService = Depends(get_utility_service)):
    return service.list_utilities()


@router.get("/meters", response_model=list[MeterRead], dependencies=[Depends(read_access)])
def list_meters(room_id: UUID | None = None, service: UtilityService = Depends(get_utility_service)):
    return service.list_meters(room_id)


@router.post("/meters", response_model=MeterRead, status_code=201, dependencies=[Depends(manage_access)])
def create_meter(payload: MeterCreate, service: UtilityService = Depends(get_utility_service)):
    return service.create_meter(payload)


@router.get(
    "/utility-tariffs",
    response_model=list[UtilityTariffRead],
    dependencies=[Depends(read_access)],
)
def list_tariffs(
    utility_id: UUID | None = None, service: UtilityService = Depends(get_utility_service)
):
    return service.list_tariffs(utility_id)


@router.post(
    "/utility-tariffs",
    response_model=UtilityTariffRead,
    status_code=201,
    dependencies=[Depends(manage_access)],
)
def create_tariff(
    payload: UtilityTariffCreate,
    user: AuthUser = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.create_tariff(payload, user.id)


@router.get(
    "/meter-readings",
    response_model=list[MeterReadingRead],
    dependencies=[Depends(read_access)],
)
def list_readings(
    meter_id: UUID | None = None,
    period_start: date | None = None,
    service: UtilityService = Depends(get_utility_service),
):
    return service.list_readings(meter_id, period_start)


@router.post(
    "/meter-readings",
    response_model=MeterReadingRead,
    status_code=201,
    dependencies=[Depends(manage_access)],
)
def create_reading(
    payload: MeterReadingCreate,
    user: AuthUser = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.create_reading(payload, user.id)
```

## File: `src/backend/dormitory_api/dependencies.py`

SHA-256: `ee5d8095af7436a7f6b0e1fce2aacb998e6da318057cc6a113fc192f3af0499b`  
Dòng: 85

```python
from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.engine import Connection

from dormitory_application.housing import HousingService
from dormitory_application.contracts import ContractService
from dormitory_application.billing import BillingService
from dormitory_application.utilities import UtilityService
from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity import decode_access_token
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import (
    AuthRepository,
    AuthUser,
    StoredBillingRepository,
    StoredContractRepository,
    StoredHousingRepository,
    StoredUtilityRepository,
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_housing_service(db: Connection = Depends(get_db)) -> HousingService:
    return HousingService(StoredHousingRepository(db))


def get_contract_service(db: Connection = Depends(get_db)) -> ContractService:
    return ContractService(StoredContractRepository(db))


def get_utility_service(db: Connection = Depends(get_db)) -> UtilityService:
    return UtilityService(StoredUtilityRepository(db))


def get_billing_service(db: Connection = Depends(get_db)) -> BillingService:
    return BillingService(StoredBillingRepository(db))


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Connection = Depends(get_db),
) -> AuthUser:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"errorCode": "AUTH_INVALID_TOKEN", "message": "Phiên đăng nhập không hợp lệ."},
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise unauthorized
    except jwt.InvalidTokenError as exc:
        raise unauthorized from exc

    user = AuthRepository(db).find_user(user_id=UUID(user_id))
    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_roles(*roles: RoleName) -> Callable:
    allowed = {role.value for role in roles}

    def role_dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"errorCode": "AUTH_FORBIDDEN", "message": "Bạn không có quyền thực hiện thao tác này."},
            )
        return user

    return role_dependency


admin_only = require_roles(RoleName.ADMIN)
admin_or_staff = require_roles(RoleName.ADMIN, RoleName.STAFF)
```

## File: `src/backend/dormitory_api/main.py`

SHA-256: `4096b48d95c9d53b8b605f7a00713cf9ed4a115b0ad598d56bf53a11f8fd4721`  
Dòng: 91

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Connection

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
    {"name": "Identity", "description": "Người dùng, ba vai trò cố định và hồ sơ sinh viên."},
    {"name": "Students", "description": "CRUD sinh viên và phân trang theo Bài 2."},
    {"name": "Housing", "description": "Tòa nhà, loại phòng, phòng, giường và sơ đồ phòng."},
    {"name": "Contracts", "description": "Đơn đăng ký, hợp đồng và lịch sử phân giường."},
    {"name": "Utilities", "description": "Công tơ, biểu giá và ghi chỉ số điện nước thủ công."},
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
def readiness(db: Connection = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT public.fn_db_ready()"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "errorCode": "DATABASE_NOT_READY",
                "message": "PostgreSQL chưa sẵn sàng.",
            },
        )
    return {"status": "ready", "database": "ok"}
```

## File: `src/backend/dormitory_api/middleware/__init__.py`

SHA-256: `06d1378b86c101057a9f5bc846c05a361f90e6e7556ec6b3f74f987a87e229b7`  
Dòng: 3

```python
from .errors import register_error_handlers

__all__ = ["register_error_handlers"]
```

## File: `src/backend/dormitory_api/middleware/errors.py`

SHA-256: `e112f1c96575444c65614021b2ecaa2611310235d9a1b5ea9b6c38ae970cc94a`  
Dòng: 146

```python
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
```

## File: `src/backend/dormitory_application/__init__.py`

SHA-256: `1e5dd1421477f093d8463885f0d69577644c6f9960ff6dc1e21347964848e69c`  
Dòng: 1

```python
"""Application use cases."""
```

## File: `src/backend/dormitory_application/ai/__init__.py`

SHA-256: `23b2c10820b9df37d4b6ff94ca6bd18d600a45a925887f4776326f07608779c6`  
Dòng: 1

```python
"""AI use cases (week 6)."""
```

## File: `src/backend/dormitory_application/billing/__init__.py`

SHA-256: `f974655f9f83429f4dc74fd68d06f84d39abf1ae9edbb7dc31c54bd21adce340`  
Dòng: 5

```python
"""Billing use cases (week 3)."""
from .schemas import BillGenerateRequest, BillItemRead, BillRead
from .service import BillingService

__all__ = ["BillingService", "BillGenerateRequest", "BillItemRead", "BillRead"]
```

## File: `src/backend/dormitory_application/billing/schemas.py`

SHA-256: `d60d4dec2a03e6ba5436847c4baad35817818a060075b3cad361d3bd33eda314`  
Dòng: 53

```python
from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class BillGenerateRequest(BaseModel):
    contract_id: UUID
    period_start: date
    period_end: date
    issued_date: date
    due_date: date
    idempotency_key: str = Field(min_length=8, max_length=100)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.period_end < self.period_start:
            raise ValueError("Ngày kết thúc kỳ phải từ ngày bắt đầu trở đi.")
        if self.due_date < self.issued_date:
            raise ValueError("Hạn thanh toán phải từ ngày phát hành trở đi.")
        return self


class BillItemRead(BaseModel):
    id: UUID
    item_type: str
    reference_type: str | None
    reference_id: UUID | None
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    calculation_snapshot: dict | None


class BillRead(BaseModel):
    id: UUID
    bill_no: str
    contract_id: UUID
    student_id: UUID
    period_start: date
    period_end: date
    issued_date: date
    due_date: date
    status: str
    subtotal: Decimal
    adjustment_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_amount: Decimal
    idempotency_key: str
    items: list[BillItemRead]
```

## File: `src/backend/dormitory_application/billing/service.py`

SHA-256: `a784d79786599027e18530f3fe110896f1d652ab1afd0477677f5c9ff48ecaab`  
Dòng: 14

```python
from uuid import UUID

from .schemas import BillGenerateRequest


class BillingService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_bills(self, user_id: UUID, role: str, contract_id: UUID | None = None):
        return self.repository.list_bills(user_id, role, contract_id)

    def generate(self, data: BillGenerateRequest, user_id: UUID):
        return self.repository.generate(data, user_id)
```

## File: `src/backend/dormitory_application/common/__init__.py`

SHA-256: `101c9b93bcd6b030b24d7cba1a4a2fb5feeb8e41f08185ebbe8b260eeb5938d0`  
Dòng: 3

```python
from .errors import BusinessRuleError, ConflictError, NotFoundError

__all__ = ["BusinessRuleError", "ConflictError", "NotFoundError"]
```

## File: `src/backend/dormitory_application/common/errors.py`

SHA-256: `cfcc606e750b370b576f749bee99ed12e483d4a8b86dcf48f2627d4ad75e91a1`  
Dòng: 13

```python
class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class BusinessRuleError(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 409) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code
```

## File: `src/backend/dormitory_application/contracts/__init__.py`

SHA-256: `98f2fb04dd53ac5ef90c630d949e84402d9408a69112f14bedb676296a94db72`  
Dòng: 24

```python
"""Contract use cases (week 2)."""
from .schemas import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    HousingApplicationCreate,
    HousingApplicationRead,
    HousingApplicationReject,
    TerminateContractRequest,
    TransferBedRequest,
)
from .service import ContractService

__all__ = [
    "AssignBedRequest",
    "BedAssignmentRead",
    "ContractRead",
    "ContractService",
    "HousingApplicationCreate",
    "HousingApplicationRead",
    "HousingApplicationReject",
    "TerminateContractRequest",
    "TransferBedRequest",
]
```

## File: `src/backend/dormitory_application/contracts/schemas.py`

SHA-256: `5146af3b6d12a499941ca2678c9e08cb9053ac7e43c5a55c396c831e0ecd34f7`  
Dòng: 71

```python
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class HousingApplicationCreate(BaseModel):
    term_code: str = Field(min_length=1, max_length=30)
    preferred_room_type_id: UUID


class HousingApplicationReject(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class HousingApplicationRead(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    term_code: str
    preferred_room_type_id: UUID
    preferred_room_type_name: str
    status: str
    rejection_reason: str | None
    created_at: datetime


class AssignBedRequest(BaseModel):
    bed_id: UUID
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_period(self):
        if self.end_date <= self.start_date:
            raise ValueError("Ngày kết thúc phải sau ngày bắt đầu.")
        return self


class TransferBedRequest(BaseModel):
    bed_id: UUID
    transfer_date: date


class TerminateContractRequest(BaseModel):
    termination_date: date


class BedAssignmentRead(BaseModel):
    id: UUID
    bed_id: UUID
    building_code: str
    room_code: str
    bed_code: str
    start_date: date
    end_date: date | None
    status: str


class ContractRead(BaseModel):
    id: UUID
    contract_no: str
    student_id: UUID
    student_name: str
    application_id: UUID
    start_date: date
    end_date: date
    status: str
    base_rate: Decimal
    current_assignment: BedAssignmentRead | None
```

## File: `src/backend/dormitory_application/contracts/service.py`

SHA-256: `80a52b1fc6b3c898b64ae4d636121a25c003526600d8bd2a5890daf977841bba`  
Dòng: 63

```python
from datetime import date
from uuid import UUID

from .schemas import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    HousingApplicationCreate,
    HousingApplicationRead,
    TransferBedRequest,
)


class ContractService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create_application(
        self, student_id: UUID, data: HousingApplicationCreate
    ) -> HousingApplicationRead:
        return self.repository.create_application(student_id, data)

    def list_applications(
        self, user_id: UUID, role: str, status: str | None
    ) -> list[HousingApplicationRead]:
        return self.repository.list_applications(user_id, role, status)

    def approve_application(
        self, application_id: UUID, reviewer_id: UUID
    ) -> HousingApplicationRead:
        return self.repository.review_application(
            application_id, reviewer_id, "Approved", None
        )

    def reject_application(
        self, application_id: UUID, reviewer_id: UUID, reason: str
    ) -> HousingApplicationRead:
        return self.repository.review_application(
            application_id, reviewer_id, "Rejected", reason.strip()
        )

    def assign_bed(self, application_id: UUID, data: AssignBedRequest) -> ContractRead:
        return self.repository.assign_bed(application_id, data)

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return self.repository.list_contracts(user_id, role)

    def get_contract(self, contract_id: UUID, user_id: UUID, role: str) -> ContractRead:
        return self.repository.get_contract(contract_id, user_id, role)

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        return self.repository.get_my_contract(student_id)

    def assignment_history(
        self, contract_id: UUID, user_id: UUID, role: str
    ) -> list[BedAssignmentRead]:
        return self.repository.assignment_history(contract_id, user_id, role)

    def transfer(self, contract_id: UUID, data: TransferBedRequest) -> ContractRead:
        return self.repository.transfer(contract_id, data)

    def terminate(self, contract_id: UUID, termination_date: date) -> ContractRead:
        return self.repository.terminate(contract_id, termination_date)
```

## File: `src/backend/dormitory_application/housing/__init__.py`

SHA-256: `1b2bba900ef012080881bc2ad4fe87f35ffc387ddabe74927529fb6e3704125d`  
Dòng: 35

```python
from .schemas import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    RoomCreate,
    RoomMatrixBuilding,
    RoomBulkGenderUpdate,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)
from .service import HousingService

__all__ = [
    "BedCreate",
    "BedRead",
    "BedUpdate",
    "BuildingCreate",
    "BuildingRead",
    "BuildingUpdate",
    "HousingService",
    "RoomCreate",
    "RoomMatrixBuilding",
    "RoomBulkGenderUpdate",
    "RoomRead",
    "RoomTypeCreate",
    "RoomTypeRead",
    "RoomTypeUpdate",
    "RoomUpdate",
]
```

## File: `src/backend/dormitory_application/housing/interfaces.py`

SHA-256: `54777a5ac70db65aa72cc97eb8d9eb8fc4f250c60dccb9c2ac8602317570d887`  
Dòng: 40

```python
from typing import Protocol
from uuid import UUID

from .schemas import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    RoomCreate,
    RoomMatrixBuilding,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)


class HousingRepository(Protocol):
    def list_buildings(self) -> list[BuildingRead]: ...
    def get_building(self, item_id: UUID) -> BuildingRead | None: ...
    def create_building(self, data: BuildingCreate) -> BuildingRead: ...
    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead | None: ...
    def delete_building(self, item_id: UUID) -> bool: ...
    def list_room_types(self) -> list[RoomTypeRead]: ...
    def create_room_type(self, data: RoomTypeCreate) -> RoomTypeRead: ...
    def update_room_type(self, item_id: UUID, data: RoomTypeUpdate) -> RoomTypeRead | None: ...
    def delete_room_type(self, item_id: UUID) -> bool: ...
    def list_rooms(self, building_id: UUID | None = None, staff_id: UUID | None = None) -> list[RoomRead]: ...
    def create_room(self, data: RoomCreate) -> RoomRead: ...
    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead | None: ...
    def delete_room(self, item_id: UUID) -> bool: ...
    def list_beds(self, room_id: UUID | None = None, staff_id: UUID | None = None) -> list[BedRead]: ...
    def create_bed(self, data: BedCreate) -> BedRead: ...
    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead | None: ...
    def delete_bed(self, item_id: UUID) -> bool: ...
    def room_matrix(self, staff_id: UUID | None = None) -> list[RoomMatrixBuilding]: ...
    def bulk_update_gender(self, data, actor_id: UUID, is_admin: bool) -> list[RoomRead]: ...
```

## File: `src/backend/dormitory_application/housing/schemas.py`

SHA-256: `d809550340812f970b6796c4565deda5b39b50f5b81227c08fbf7031e9faf306`  
Dòng: 124

```python
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BuildingBase(BaseModel):
    code: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=120)
    address: str = Field(default="", max_length=250)
    floors: int = Field(ge=1, le=100)
    is_active: bool = True


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class RoomTypeBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    default_monthly_rate: Decimal = Field(ge=0)
    default_capacity: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool = True


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(RoomTypeBase):
    pass


class RoomTypeRead(RoomTypeBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class RoomBase(BaseModel):
    building_id: UUID
    room_type_id: UUID
    code: str = Field(min_length=1, max_length=20)
    floor: int = Field(ge=1, le=100)
    gender_policy: str = Field(default="Unassigned", pattern="^(Male|Female|Mixed|Unassigned)$")
    managed_by_staff_id: UUID | None = None
    status: str = Field(default="Available", pattern="^(Available|Maintenance|Inactive)$")
    is_active: bool = True
    note: str | None = Field(default=None, max_length=500)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomRead(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    building_code: str
    room_type_name: str


class BedBase(BaseModel):
    room_id: UUID
    code: str = Field(min_length=1, max_length=20)
    is_active: bool = True
    note: str | None = Field(default=None, max_length=300)


class BedCreate(BedBase):
    pass


class BedUpdate(BedBase):
    pass


class BedRead(BedBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: str


class RoomMatrixBed(BaseModel):
    id: UUID
    code: str
    status: str


class RoomMatrixRoom(BaseModel):
    id: UUID
    code: str
    floor: int
    room_type: str
    gender_policy: str
    managed_by_staff_id: UUID | None
    beds: list[RoomMatrixBed]


class RoomMatrixBuilding(BaseModel):
    id: UUID
    code: str
    name: str
    rooms: list[RoomMatrixRoom]


class RoomBulkGenderUpdate(BaseModel):
    gender_policy: str = Field(pattern="^(Male|Female|Mixed|Unassigned)$")
    building_id: UUID | None = None
    floor: int | None = Field(default=None, ge=1)
    room_ids: list[UUID] = Field(default_factory=list)
```

## File: `src/backend/dormitory_application/housing/service.py`

SHA-256: `02c908e29656b7883ad17d33e042885a7b562b9af1d9885c02bda6ac516da9fa`  
Dòng: 101

```python
from uuid import UUID

from dormitory_application.common import NotFoundError

from .interfaces import HousingRepository
from .schemas import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    RoomCreate,
    RoomMatrixBuilding,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)


class HousingService:
    def __init__(self, repository: HousingRepository) -> None:
        self.repository = repository

    def list_buildings(self) -> list[BuildingRead]:
        return self.repository.list_buildings()

    def get_building(self, item_id: UUID) -> BuildingRead:
        item = self.repository.get_building(item_id)
        if item is None:
            raise NotFoundError("Building not found")
        return item

    def create_building(self, data: BuildingCreate) -> BuildingRead:
        return self.repository.create_building(data)

    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead:
        item = self.repository.update_building(item_id, data)
        if item is None:
            raise NotFoundError("Building not found")
        return item

    def delete_building(self, item_id: UUID) -> None:
        if not self.repository.delete_building(item_id):
            raise NotFoundError("Building not found")

    def list_room_types(self) -> list[RoomTypeRead]:
        return self.repository.list_room_types()

    def create_room_type(self, data: RoomTypeCreate) -> RoomTypeRead:
        return self.repository.create_room_type(data)

    def update_room_type(self, item_id: UUID, data: RoomTypeUpdate) -> RoomTypeRead:
        item = self.repository.update_room_type(item_id, data)
        if item is None:
            raise NotFoundError("Room type not found")
        return item

    def delete_room_type(self, item_id: UUID) -> None:
        if not self.repository.delete_room_type(item_id):
            raise NotFoundError("Room type not found")

    def list_rooms(self, building_id: UUID | None = None, staff_id: UUID | None = None) -> list[RoomRead]:
        return self.repository.list_rooms(building_id, staff_id)

    def create_room(self, data: RoomCreate) -> RoomRead:
        return self.repository.create_room(data)

    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead:
        item = self.repository.update_room(item_id, data)
        if item is None:
            raise NotFoundError("Room not found")
        return item

    def delete_room(self, item_id: UUID) -> None:
        if not self.repository.delete_room(item_id):
            raise NotFoundError("Room not found")

    def list_beds(self, room_id: UUID | None = None, staff_id: UUID | None = None) -> list[BedRead]:
        return self.repository.list_beds(room_id, staff_id)

    def create_bed(self, data: BedCreate) -> BedRead:
        return self.repository.create_bed(data)

    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead:
        item = self.repository.update_bed(item_id, data)
        if item is None:
            raise NotFoundError("Bed not found")
        return item

    def delete_bed(self, item_id: UUID) -> None:
        if not self.repository.delete_bed(item_id):
            raise NotFoundError("Bed not found")

    def room_matrix(self, staff_id: UUID | None = None) -> list[RoomMatrixBuilding]:
        return self.repository.room_matrix(staff_id)

    def bulk_update_gender(self, data, actor_id: UUID, is_admin: bool) -> list[RoomRead]:
        return self.repository.bulk_update_gender(data, actor_id, is_admin)
```

## File: `src/backend/dormitory_application/identity/__init__.py`

SHA-256: `b6e0103612c7d9135e84de36bf1b85f6422d2595f496e042cffa4d5609b3a4c9`  
Dòng: 22

```python
from .schemas import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    StudentCreate,
    StudentPage,
    StudentProfileRead,
    StudentProfileUpdate,
    StudentRead,
    TokenResponse,
    UserCreate,
    UserRead,
    UserUpdate,
)

__all__ = [
    "LoginRequest", "RefreshTokenRequest", "RegisterRequest",
    "ResetPasswordRequest", "StudentProfileRead", "StudentProfileUpdate",
    "StudentCreate", "StudentPage", "StudentRead",
    "TokenResponse", "UserCreate", "UserRead", "UserUpdate",
]
```

## File: `src/backend/dormitory_application/identity/schemas.py`

SHA-256: `0d81ba73bd71a165341d1667bf0311e69bb5bea122100cffdec04629c5c6380a`  
Dòng: 109

```python
from datetime import date
import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailValidatedModel(BaseModel):
    @field_validator("email", check_fields=False)
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError("Email không đúng định dạng.")
        return normalized


class LoginRequest(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool = True


class UserCreate(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    role: str


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    role: str
    is_active: bool


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)


class StudentProfileUpdate(BaseModel):
    student_code: str = Field(min_length=1, max_length=30)
    faculty: str = Field(default="", max_length=150)
    cohort: str = Field(default="", max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, pattern="^(Male|Female|Other)$")
    phone: str = Field(default="", max_length=30)
    address: str = Field(default="", max_length=300)
    identity_number: str | None = Field(default=None, max_length=30)
    emergency_contact_name: str = Field(default="", max_length=120)
    emergency_contact_phone: str = Field(default="", max_length=30)


class StudentProfileRead(StudentProfileUpdate):
    user_id: UUID
    email: str
    full_name: str


class RegisterRequest(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    student_code: str = Field(min_length=8, max_length=8, pattern=r"^\S{8}$")
    age: int = Field(ge=18, le=60)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=32, max_length=512)


class StudentCreate(RegisterRequest):
    pass


class StudentRead(BaseModel):
    id: UUID
    student_code: str
    full_name: str
    age: int | None
    email: str
    is_active: bool


class StudentPage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[StudentRead]
    page: int
    page_size: int = Field(serialization_alias="pageSize")
    total: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead
```

## File: `src/backend/dormitory_application/reports/__init__.py`

SHA-256: `016c193863945a50dcae54538b79d82adb75c5e6e44ba62c4eaf60a8c6c14e19`  
Dòng: 1

```python
"""Reporting use cases (week 6)."""
```

## File: `src/backend/dormitory_application/utilities/__init__.py`

SHA-256: `bf3adbd2203f2c4e7e2c8a142df61aacd5fbd73bb5633602b4df64f4e5f8bb3c`  
Dòng: 26

```python
"""Utility use cases (week 3)."""
from .schemas import (
    MeterCreate,
    MeterRead,
    MeterReadingCreate,
    MeterReadingRead,
    TariffTierInput,
    TariffTierRead,
    UtilityRead,
    UtilityTariffCreate,
    UtilityTariffRead,
)
from .service import UtilityService

__all__ = [
    "MeterCreate",
    "MeterRead",
    "MeterReadingCreate",
    "MeterReadingRead",
    "TariffTierInput",
    "TariffTierRead",
    "UtilityRead",
    "UtilityTariffCreate",
    "UtilityTariffRead",
    "UtilityService",
]
```

## File: `src/backend/dormitory_application/utilities/schemas.py`

SHA-256: `bc42ec6b3870f0175828eeae7e0fbbde27480a0f97c30b9959eaf679894f1ae8`  
Dòng: 122

```python
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from dormitory_domain.billing import TariffTier, validate_tariff_tiers


class UtilityRead(BaseModel):
    id: UUID
    code: str
    name: str
    unit: str
    rounding_scale: int
    is_active: bool


class MeterCreate(BaseModel):
    utility_id: UUID
    room_id: UUID
    meter_code: str = Field(min_length=1, max_length=50)
    serial_number: str | None = Field(default=None, max_length=100)
    installed_at: date | None = None
    initial_reading: Decimal = Field(default=Decimal("0"), ge=0)
    note: str | None = Field(default=None, max_length=500)


class MeterRead(BaseModel):
    id: UUID
    utility_id: UUID
    utility_code: str
    utility_name: str
    room_id: UUID
    room_label: str
    meter_code: str
    serial_number: str | None
    initial_reading: Decimal
    is_active: bool


class TariffTierInput(BaseModel):
    tier_order: int = Field(ge=1)
    from_quantity: Decimal = Field(ge=0)
    to_quantity: Decimal | None = Field(default=None, gt=0)
    unit_price: Decimal = Field(ge=0)


class UtilityTariffCreate(BaseModel):
    utility_id: UUID
    name: str = Field(min_length=1, max_length=120)
    effective_from: date
    effective_to: date | None = None
    calculation_type: str = Field(default="Tiered", pattern="^(Flat|Tiered)$")
    tiers: list[TariffTierInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_period_and_tiers(self):
        if self.effective_to is not None and self.effective_to < self.effective_from:
            raise ValueError("Ngày kết thúc biểu giá phải sau ngày bắt đầu.")
        validate_tariff_tiers(
            [
                TariffTier(
                    tier_order=item.tier_order,
                    from_quantity=item.from_quantity,
                    to_quantity=item.to_quantity,
                    unit_price=item.unit_price,
                )
                for item in self.tiers
            ],
            self.calculation_type,
        )
        return self


class TariffTierRead(TariffTierInput):
    id: UUID


class UtilityTariffRead(BaseModel):
    id: UUID
    utility_id: UUID
    utility_code: str
    utility_name: str
    name: str
    effective_from: date
    effective_to: date | None
    calculation_type: str
    is_active: bool
    tiers: list[TariffTierRead]


class MeterReadingCreate(BaseModel):
    meter_id: UUID
    period_start: date
    period_end: date
    previous_reading: Decimal = Field(ge=0)
    current_reading: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def validate_reading(self):
        if self.period_end < self.period_start:
            raise ValueError("Ngày kết thúc kỳ phải từ ngày bắt đầu trở đi.")
        if self.current_reading < self.previous_reading:
            raise ValueError("Chỉ số hiện tại không được nhỏ hơn chỉ số trước.")
        return self


class MeterReadingRead(BaseModel):
    id: UUID
    meter_id: UUID
    meter_code: str
    utility_code: str
    period_start: date
    period_end: date
    previous_reading: Decimal
    current_reading: Decimal
    consumption: Decimal
    calculated_amount: Decimal
    tariff_id: UUID
    tariff_snapshot: dict
    recorded_at: datetime
```

## File: `src/backend/dormitory_application/utilities/service.py`

SHA-256: `a5d36bc37c9d225bd19590ede467d5e6be42f9623820676a6ed707821de75830`  
Dòng: 30

```python
from datetime import date
from uuid import UUID

from .schemas import MeterCreate, MeterReadingCreate, UtilityTariffCreate


class UtilityService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_utilities(self):
        return self.repository.list_utilities()

    def list_meters(self, room_id: UUID | None = None):
        return self.repository.list_meters(room_id)

    def create_meter(self, data: MeterCreate):
        return self.repository.create_meter(data)

    def list_tariffs(self, utility_id: UUID | None = None):
        return self.repository.list_tariffs(utility_id)

    def create_tariff(self, data: UtilityTariffCreate, user_id: UUID):
        return self.repository.create_tariff(data, user_id)

    def create_reading(self, data: MeterReadingCreate, user_id: UUID):
        return self.repository.create_reading(data, user_id)

    def list_readings(self, meter_id: UUID | None = None, period_start: date | None = None):
        return self.repository.list_readings(meter_id, period_start)
```

## File: `src/backend/dormitory_application/violations/__init__.py`

SHA-256: `877f52c64deecb020745709674ca603a39ebfb169a88ecf44c163b70b00d94c3`  
Dòng: 1

```python
"""Violation use cases (week 5)."""
```

## File: `src/backend/dormitory_domain/__init__.py`

SHA-256: `8b7080c2f7df917f287e9cd57c15762b0f8aced86814c669d6c48c5083c8c3d3`  
Dòng: 1

```python
"""Domain model and business rules."""
```

## File: `src/backend/dormitory_domain/billing/__init__.py`

SHA-256: `4fddab483a96ca6da1d5b8cefc52f99db8013d8e947ce76b6a40e585f0acc83a`  
Dòng: 16

```python
"""Billing domain package (implemented from week 3)."""
from .calculator import (
    BillingCalculation,
    TariffTier,
    TierCharge,
    calculate_utility_charge,
    validate_tariff_tiers,
)

__all__ = [
    "BillingCalculation",
    "TariffTier",
    "TierCharge",
    "calculate_utility_charge",
    "validate_tariff_tiers",
]
```

## File: `src/backend/dormitory_domain/billing/calculator.py`

SHA-256: `cdf4814a3abbad88bf0436de84a22289fe9fbd6dd7590aabab74fa6d0b4a716e`  
Dòng: 114

```python
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


MONEY = Decimal("0.01")
QUANTITY = Decimal("0.001")


@dataclass(frozen=True)
class TariffTier:
    tier_order: int
    from_quantity: Decimal
    to_quantity: Decimal | None
    unit_price: Decimal


@dataclass(frozen=True)
class TierCharge:
    tier_order: int
    from_quantity: Decimal
    to_quantity: Decimal | None
    billed_quantity: Decimal
    unit_price: Decimal
    amount: Decimal


@dataclass(frozen=True)
class BillingCalculation:
    consumption: Decimal
    total_amount: Decimal
    breakdown: tuple[TierCharge, ...]


def validate_tariff_tiers(tiers: list[TariffTier], calculation_type: str) -> None:
    if not tiers:
        raise ValueError("Biểu giá phải có ít nhất một bậc.")
    ordered = sorted(tiers, key=lambda item: item.tier_order)
    if [item.tier_order for item in ordered] != list(range(1, len(ordered) + 1)):
        raise ValueError("Thứ tự bậc giá phải liên tục từ 1.")
    if ordered[0].from_quantity != Decimal("0"):
        raise ValueError("Bậc giá đầu tiên phải bắt đầu từ 0.")
    if calculation_type == "Flat" and len(ordered) != 1:
        raise ValueError("Biểu giá đồng giá chỉ được có một bậc.")

    expected_from = Decimal("0")
    for index, tier in enumerate(ordered):
        if tier.from_quantity != expected_from:
            raise ValueError("Các bậc giá phải liên tục, không được hở hoặc chồng lấn.")
        if tier.unit_price < 0:
            raise ValueError("Đơn giá không được âm.")
        if tier.to_quantity is None:
            if index != len(ordered) - 1:
                raise ValueError("Chỉ bậc cuối cùng được để trống giới hạn trên.")
        else:
            if tier.to_quantity <= tier.from_quantity:
                raise ValueError("Giới hạn trên phải lớn hơn giới hạn dưới.")
            expected_from = tier.to_quantity

    if ordered[-1].to_quantity is not None:
        raise ValueError("Bậc giá cuối cùng phải không giới hạn.")


def calculate_utility_charge(
    consumption: Decimal,
    tiers: list[TariffTier],
    calculation_type: str = "Tiered",
) -> BillingCalculation:
    consumption = Decimal(consumption).quantize(QUANTITY)
    if consumption < 0:
        raise ValueError("Sản lượng tiêu thụ không được âm.")
    if calculation_type not in {"Flat", "Tiered"}:
        raise ValueError("Loại biểu giá không hợp lệ.")
    validate_tariff_tiers(tiers, calculation_type)
    ordered = sorted(tiers, key=lambda item: item.tier_order)

    if calculation_type == "Flat":
        amount = (consumption * ordered[0].unit_price).quantize(MONEY, ROUND_HALF_UP)
        charge = TierCharge(
            tier_order=1,
            from_quantity=Decimal("0"),
            to_quantity=None,
            billed_quantity=consumption,
            unit_price=ordered[0].unit_price,
            amount=amount,
        )
        return BillingCalculation(consumption, amount, (charge,))

    breakdown: list[TierCharge] = []
    total = Decimal("0")
    for tier in ordered:
        if consumption <= tier.from_quantity:
            billed_quantity = Decimal("0")
        else:
            upper = consumption if tier.to_quantity is None else min(consumption, tier.to_quantity)
            billed_quantity = max(Decimal("0"), upper - tier.from_quantity).quantize(QUANTITY)
        if billed_quantity == 0:
            continue
        amount = (billed_quantity * tier.unit_price).quantize(MONEY, ROUND_HALF_UP)
        total += amount
        breakdown.append(
            TierCharge(
                tier_order=tier.tier_order,
                from_quantity=tier.from_quantity,
                to_quantity=tier.to_quantity,
                billed_quantity=billed_quantity,
                unit_price=tier.unit_price,
                amount=amount,
            )
        )
    return BillingCalculation(
        consumption=consumption,
        total_amount=total.quantize(MONEY, ROUND_HALF_UP),
        breakdown=tuple(breakdown),
    )
```

## File: `src/backend/dormitory_domain/common/__init__.py`

SHA-256: `3c4ad35d82313d4a0c8c99da9f148a47cb79ab46f0ff5fbc2c8132e3613df4d2`  
Dòng: 9

```python
from .enums import BedAssignmentStatus, BedStatus, ContractStatus, HousingApplicationStatus, RoleName

__all__ = [
    "BedAssignmentStatus",
    "BedStatus",
    "ContractStatus",
    "HousingApplicationStatus",
    "RoleName",
]
```

## File: `src/backend/dormitory_domain/common/enums.py`

SHA-256: `99cba198d74d4a021997c22ee90e5350bb5b5e3b6d2a23d535cea0957b320d67`  
Dòng: 29

```python
from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "Admin"
    STAFF = "Staff"
    STUDENT = "Student"


class BedStatus(StrEnum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"


class HousingApplicationStatus(StrEnum):
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class ContractStatus(StrEnum):
    ACTIVE = "Active"
    TERMINATED = "Terminated"


class BedAssignmentStatus(StrEnum):
    ACTIVE = "Active"
    ENDED = "Ended"
```

## File: `src/backend/dormitory_domain/contracts/__init__.py`

SHA-256: `7909df939c3c5e5055baa78ca738f70bd0b4ebe9b9f6da5a154a8323121ba299`  
Dòng: 1

```python
"""Contract domain package (implemented from week 2)."""
```

## File: `src/backend/dormitory_domain/housing/__init__.py`

SHA-256: `825343991a95e88fbfbc199819e239fdf7ddaa7e0556ecc66b60d33249803c40`  
Dòng: 3

```python
from .entities import Bed, Building, Room, RoomType

__all__ = ["Bed", "Building", "Room", "RoomType"]
```

## File: `src/backend/dormitory_domain/housing/entities.py`

SHA-256: `eadef1d08d122b39dba82293c0ca42df7bff201bfbc04ded925712cc157be600`  
Dòng: 75

```python
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from dormitory_domain.common import BedStatus


@dataclass(slots=True)
class Building:
    code: str
    name: str
    address: str
    floors: int
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        if not self.code or not self.name:
            raise ValueError("Building code and name are required")
        if self.floors < 1:
            raise ValueError("Building must have at least one floor")


@dataclass(slots=True)
class RoomType:
    name: str
    default_monthly_rate: Decimal
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Room type name is required")
        if self.default_monthly_rate < 0:
            raise ValueError("Monthly rate cannot be negative")


@dataclass(slots=True)
class Room:
    building_id: UUID
    room_type_id: UUID
    code: str
    floor: int
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        if not self.code:
            raise ValueError("Room code is required")
        if self.floor < 1:
            raise ValueError("Room floor must be positive")


@dataclass(slots=True)
class Bed:
    room_id: UUID
    code: str
    is_active: bool = True
    is_occupied: bool = False
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        if not self.code:
            raise ValueError("Bed code is required")

    @property
    def status(self) -> BedStatus:
        if not self.is_active:
            return BedStatus.MAINTENANCE
        return BedStatus.OCCUPIED if self.is_occupied else BedStatus.AVAILABLE
```

## File: `src/backend/dormitory_domain/utilities/__init__.py`

SHA-256: `3b2e6421d72c5a75f120fbcf601d15059c29e5b2500dc69145427db55de45598`  
Dòng: 1

```python
"""Utilities domain package (implemented from week 3)."""
```

## File: `src/backend/dormitory_domain/violations/__init__.py`

SHA-256: `c6899f413cb771f74ee4adc02b73a06bb649ca218b1f1331170107d198eaa243`  
Dòng: 1

```python
"""Violation domain package (implemented from week 5)."""
```

## File: `src/backend/dormitory_infrastructure/__init__.py`

SHA-256: `3c6f0562b0095f453e65e5178b7ddbab813680c531e650684ce791acdd5a3f90`  
Dòng: 1

```python
"""Persistence, identity and external service adapters."""
```

## File: `src/backend/dormitory_infrastructure/ai/__init__.py`

SHA-256: `8b9d949800908cdab4bdfe88298ee145759e58753573ff4519f579274a1e30bf`  
Dòng: 1

```python
"""LLM provider adapter (week 6)."""
```

## File: `src/backend/dormitory_infrastructure/identity/__init__.py`

SHA-256: `c4d7ea899b73d28dbf275aa3f06a4f8290a081718c3b591475bc9fb02aa4671f`  
Dòng: 17

```python
from .security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "decode_access_token",
    "hash_password",
    "hash_refresh_token",
    "verify_password",
]
```

## File: `src/backend/dormitory_infrastructure/identity/security.py`

SHA-256: `f20da3ea4c871a10b44dba1df865ba130f12e29625b4f32e38d6144eb716eef1`  
Dòng: 54

```python
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from dormitory_infrastructure.persistence.config import get_settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str, role: str, email: str) -> str:
    settings = get_settings()
    expires = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "email": email,
        "role": role,
        "jti": str(uuid4()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": datetime.now(UTC),
        "exp": expires,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def create_refresh_token() -> str:
    return token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
```

## File: `src/backend/dormitory_infrastructure/identity/seed_cli.py`

SHA-256: `dd936d270ff1730d8235c116010cf765bee7039720a373630d11f55e3794bc7f`  
Dòng: 12

```python
from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import engine


def main() -> None:
    with engine.connect() as db:
        seed_identity(db)
    print("Seeded Admin, Staff and Student demo accounts.")


if __name__ == "__main__":
    main()
```

## File: `src/backend/dormitory_infrastructure/identity/seeder.py`

SHA-256: `83175b17adae94d92dffabd6aff60f5a90a940500ab5e5b724167a2076293716`  
Dòng: 54

```python
"""Seed demo accounts and utility catalog through PostgreSQL functions."""
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity.security import hash_password


DEMO_USERS = (
    ("admin@dormitory.local", "Quản trị viên", RoleName.ADMIN, "Admin@123"),
    ("staff@dormitory.local", "Cán bộ ký túc xá", RoleName.STAFF, "Staff@123"),
    ("student@dormitory.local", "Sinh viên demo", RoleName.STUDENT, "Student@123"),
)

UTILITY_CATALOG = (
    ("ELECTRICITY", "Tiền điện", "kWh", 0),
    ("WATER", "Tiền nước", "m3", 0),
)


def seed_identity(db: Connection) -> None:
    for role_name in RoleName:
        db.execute(
            text("SELECT public.fn_seed_role(:id, :name)"),
            {"id": uuid4(), "name": role_name.value},
        )

    student_id = None
    for email, full_name, role_name, password in DEMO_USERS:
        user_id = db.scalar(
            text("SELECT public.fn_seed_user(:id, :email, :full_name, :password_hash, :role_name)"),
            {
                "id": uuid4(), "email": email, "full_name": full_name,
                "password_hash": hash_password(password), "role_name": role_name.value,
            },
        )
        if role_name == RoleName.STUDENT:
            student_id = user_id

    db.execute(
        text("SELECT public.fn_seed_student_profile(:user_id, :student_code)"),
        {"user_id": student_id, "student_code": "SV-DEMO-001"},
    )
    for code, name, unit, rounding_scale in UTILITY_CATALOG:
        db.execute(
            text("SELECT public.fn_seed_utility(:id, :code, :name, :unit, :rounding_scale)"),
            {
                "id": uuid4(), "code": code, "name": name,
                "unit": unit, "rounding_scale": rounding_scale,
            },
        )
    db.commit()
```

## File: `src/backend/dormitory_infrastructure/persistence/__init__.py`

SHA-256: `9344c5bc7598d7ceb8ea59f13d5320c115db951f9bba454b1c8c88d42881dd22`  
Dòng: 3

```python
from .database import engine, get_db

__all__ = ["engine", "get_db"]
```

## File: `src/backend/dormitory_infrastructure/persistence/config.py`

SHA-256: `069626ad7b75fec85b1d51747c04aace03f01c5d7a5a3bff5f7fcc3577d164e1`  
Dòng: 28

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://dormitory:changeme@localhost:5432/dormitory"
    secret_key: str = "development-only-change-me-at-least-32-bytes"
    jwt_issuer: str = "dormitory-api"
    jwt_audience: str = "dormitory-client"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    cors_origins: str = ""

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## File: `src/backend/dormitory_infrastructure/persistence/database.py`

SHA-256: `316ba275efb4cd6e2538e136ed09aaa877906602dba66601b160d672ee370cca`  
Dòng: 15

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from .config import get_settings


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)


def get_db() -> Generator[Connection, None, None]:
    with engine.connect() as connection:
        yield connection
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/env.py`

SHA-256: `6b16d3763f8033e05c4cff18b978ae97d3dee4cfd1a8e8e6a1476079f9b2a8fb`  
Dòng: 47

```python
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from dormitory_infrastructure.persistence.config import get_settings

config = context.config
config.set_main_option(
    "sqlalchemy.url",
    config.attributes.get("database_url", get_settings().database_url),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260912_0001_initial.py`

SHA-256: `e99565302813bffafa332ed794f4068cb7c5185567bafb9070f5f8c5d17a034b`  
Dòng: 89

```python
"""Initial identity and housing schema.

Revision ID: 20260912_0001
Revises: None
Create Date: 2026-09-12
"""

from alembic import op
import sqlalchemy as sa

revision = "20260912_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "buildings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=250), nullable=False),
        sa.Column("floors", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "room_types",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("default_monthly_rate", sa.Numeric(14, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "rooms",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("building_id", sa.Uuid(), nullable=False),
        sa.Column("room_type_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.ForeignKeyConstraint(["room_type_id"], ["room_types.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("building_id", "code", name="uq_rooms_building_code"),
    )
    op.create_table(
        "beds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("room_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "code", name="uq_beds_room_code"),
    )


def downgrade() -> None:
    op.drop_table("beds")
    op.drop_table("rooms")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("room_types")
    op.drop_table("buildings")
    op.drop_table("roles")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260919_0002_contracts.py`

SHA-256: `ca114af95369b7fec44b6501e76e593423ec0f7acb8cb08d149e7ff008b92db4`  
Dòng: 114

```python
"""Add housing applications, contracts and bed assignments.

Revision ID: 20260919_0002
Revises: 20260912_0001
Create Date: 2026-09-19
"""

from alembic import op
import sqlalchemy as sa

revision = "20260919_0002"
down_revision = "20260912_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "housing_applications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("term_code", sa.String(length=30), nullable=False),
        sa.Column("preferred_room_type_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("rejection_reason", sa.String(length=500), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["preferred_room_type_id"], ["room_types.id"]),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_housing_applications_status"),
        "housing_applications",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_housing_applications_student_id"),
        "housing_applications",
        ["student_id"],
        unique=False,
    )
    op.create_table(
        "contracts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_no", sa.String(length=50), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("application_id", sa.Uuid(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("base_rate", sa.Numeric(14, 2), nullable=False),
        sa.Column("terminated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["application_id"], ["housing_applications.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("application_id"),
        sa.UniqueConstraint("contract_no"),
    )
    op.create_index(op.f("ix_contracts_status"), "contracts", ["status"], unique=False)
    op.create_index(
        op.f("ix_contracts_student_id"), "contracts", ["student_id"], unique=False
    )
    op.create_table(
        "bed_assignments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_id", sa.Uuid(), nullable=False),
        sa.Column("bed_id", sa.Uuid(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["bed_id"], ["beds.id"]),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bed_assignments_bed_id"), "bed_assignments", ["bed_id"], unique=False
    )
    op.create_index(
        op.f("ix_bed_assignments_contract_id"),
        "bed_assignments",
        ["contract_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_bed_assignments_status"), "bed_assignments", ["status"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_bed_assignments_status"), table_name="bed_assignments")
    op.drop_index(op.f("ix_bed_assignments_contract_id"), table_name="bed_assignments")
    op.drop_index(op.f("ix_bed_assignments_bed_id"), table_name="bed_assignments")
    op.drop_table("bed_assignments")
    op.drop_index(op.f("ix_contracts_student_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_status"), table_name="contracts")
    op.drop_table("contracts")
    op.drop_index(
        op.f("ix_housing_applications_student_id"),
        table_name="housing_applications",
    )
    op.drop_index(
        op.f("ix_housing_applications_status"),
        table_name="housing_applications",
    )
    op.drop_table("housing_applications")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0003_identity_permissions_profiles_audit.py`

SHA-256: `282193d1d08d33463e695dff48b322c562d868e887133b97822fbb39eeb781dc`  
Dòng: 91

```python
"""Add permissions, student profiles and audit history.

Revision ID: 20260921_0003
Revises: 20260919_0002
"""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0003"
down_revision = "20260919_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("module", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_permissions_code", "permissions", ["code"], unique=True)
    op.create_index("ix_permissions_module", "permissions", ["module"])
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("permission_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"]),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    op.create_table(
        "student_profiles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("student_code", sa.String(30), nullable=False),
        sa.Column("faculty", sa.String(150), server_default="", nullable=False),
        sa.Column("cohort", sa.String(30), server_default="", nullable=False),
        sa.Column("date_of_birth", sa.Date()),
        sa.Column("phone", sa.String(30), server_default="", nullable=False),
        sa.Column("address", sa.String(300), server_default="", nullable=False),
        sa.Column("emergency_contact_name", sa.String(120), server_default="", nullable=False),
        sa.Column("emergency_contact_phone", sa.String(30), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("student_code"),
    )
    op.create_index("ix_student_profiles_student_code", "student_profiles", ["student_code"], unique=True)
    op.create_table(
        "login_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid()),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("succeeded", sa.Boolean(), nullable=False),
        sa.Column("ip_address", sa.String(64), server_default="", nullable=False),
        sa.Column("user_agent", sa.String(500), server_default="", nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("user_id", "email", "succeeded", "occurred_at"):
        op.create_index(f"ix_login_events_{column}", "login_events", [column])
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid()),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False),
        sa.Column("before_data", sa.JSON()),
        sa.Column("after_data", sa.JSON()),
        sa.Column("correlation_id", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("actor_user_id", "action", "entity_type", "entity_id", "correlation_id", "created_at"):
        op.create_index(f"ix_audit_logs_{column}", "audit_logs", [column])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("login_events")
    op.drop_table("student_profiles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0004_housing_scope_contract_events.py`

SHA-256: `6908f9ec6ec1de7a1ff6f8d6a0d08e40b75df239dd0e5703ce2f001253403d36`  
Dòng: 126

```python
"""Extend core tables and add gender-aware housing workflow."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0004"
down_revision = "20260921_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = sa.text("CURRENT_TIMESTAMP")
    for name, column in (
        ("roles", sa.Column("display_name", sa.String(100))),
        ("roles", sa.Column("description", sa.String(300))),
        ("roles", sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False)),
        ("roles", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("roles", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("permissions", sa.Column("description", sa.String(300))),
        ("permissions", sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False)),
        ("users", sa.Column("last_password_changed_at", sa.DateTime(timezone=True))),
        ("users", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("users", sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("users", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("users", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("student_profiles", sa.Column("gender", sa.String(20))),
        ("student_profiles", sa.Column("identity_number", sa.String(30))),
        ("buildings", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("buildings", sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("buildings", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("buildings", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("room_types", sa.Column("default_capacity", sa.Integer())),
        ("room_types", sa.Column("description", sa.String(500))),
        ("room_types", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("room_types", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("gender_policy", sa.String(20), server_default="Unassigned", nullable=False)),
        ("rooms", sa.Column("managed_by_staff_id", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("rooms", sa.Column("status", sa.String(20), server_default="Available", nullable=False)),
        ("rooms", sa.Column("note", sa.String(500))),
        ("rooms", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("beds", sa.Column("note", sa.String(300))),
        ("beds", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("beds", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("housing_applications", sa.Column("expected_start_date", sa.Date())),
        ("housing_applications", sa.Column("expected_end_date", sa.Date())),
        ("housing_applications", sa.Column("note", sa.String(1000))),
        ("housing_applications", sa.Column("cancelled_at", sa.DateTime(timezone=True))),
        ("contracts", sa.Column("issued_at", sa.DateTime(timezone=True))),
        ("contracts", sa.Column("issued_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("contracts", sa.Column("termination_reason", sa.String(500))),
        ("contracts", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("contracts", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("bed_assignments", sa.Column("assigned_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("bed_assignments", sa.Column("ended_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("bed_assignments", sa.Column("end_reason", sa.String(500))),
        ("bed_assignments", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
    ):
        op.add_column(name, column)
    op.create_index("ix_rooms_managed_by_staff_id", "rooms", ["managed_by_staff_id"])
    op.create_check_constraint("ck_rooms_gender_policy", "rooms", "gender_policy IN ('Male','Female','Mixed','Unassigned')")
    op.create_check_constraint("ck_rooms_status", "rooms", "status IN ('Available','Maintenance','Inactive')")
    op.create_check_constraint("ck_applications_expected_period", "housing_applications", "expected_end_date IS NULL OR expected_start_date IS NULL OR expected_end_date >= expected_start_date")
    op.create_check_constraint("ck_contracts_period", "contracts", "end_date >= start_date")
    op.create_check_constraint("ck_contracts_base_rate", "contracts", "base_rate >= 0")
    op.create_check_constraint("ck_assignments_period", "bed_assignments", "end_date IS NULL OR end_date >= start_date")
    op.create_index("uq_active_assignment_contract", "bed_assignments", ["contract_id"], unique=True, postgresql_where=sa.text("status = 'Active'"))
    op.create_table(
        "room_transfer_requests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("current_bed_id", sa.Uuid(), sa.ForeignKey("beds.id"), nullable=False),
        sa.Column("preferred_room_type_id", sa.Uuid(), sa.ForeignKey("room_types.id")),
        sa.Column("preferred_building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("requested_bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("reason", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="Submitted"),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)),
        sa.Column("assigned_bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )
    op.create_index("ix_transfer_contract", "room_transfer_requests", ["contract_id"])
    op.create_index("ix_transfer_student", "room_transfer_requests", ["student_id"])
    op.create_index("uq_submitted_transfer_contract", "room_transfer_requests", ["contract_id"], unique=True, postgresql_where=sa.text("status = 'Submitted'"))
    op.create_table(
        "contract_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("event_type", sa.String(40), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("old_status", sa.String(20)),
        sa.Column("new_status", sa.String(20), nullable=False),
        sa.Column("reason", sa.String(500)),
        sa.Column("event_data", sa.JSON()),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )
    op.create_index("ix_contract_events_contract", "contract_events", ["contract_id", "created_at"])


def downgrade() -> None:
    op.drop_table("contract_events")
    op.drop_table("room_transfer_requests")
    op.drop_index("uq_active_assignment_contract", table_name="bed_assignments")
    columns = {
        "bed_assignments": ["assigned_by", "ended_by", "end_reason", "created_at"],
        "contracts": ["issued_at", "issued_by", "termination_reason", "created_at", "updated_at"],
        "housing_applications": ["expected_start_date", "expected_end_date", "note", "cancelled_at"],
        "beds": ["note", "created_at", "updated_at"],
        "rooms": ["gender_policy", "managed_by_staff_id", "status", "note", "created_at", "updated_at", "updated_by"],
        "room_types": ["default_capacity", "description", "created_at", "updated_at"],
        "buildings": ["created_at", "created_by", "updated_at", "updated_by"],
        "student_profiles": ["gender", "identity_number"],
        "users": ["last_password_changed_at", "created_at", "created_by", "updated_at", "updated_by"],
        "permissions": ["description", "is_active"],
        "roles": ["display_name", "description", "is_active", "created_at", "updated_at"],
    }
    for table, names in columns.items():
        for name in names:
            op.drop_column(table, name)
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0005_utilities_files.py`

SHA-256: `7fc49b32d02b923d791d37dc7aad944a3b142a46787580cdf2d4a302dce363fb`  
Dòng: 109

```python
"""Add utilities, metering, tariff and file metadata tables."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0005"
down_revision = "20260921_0004"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("stored_files",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("storage_provider", sa.String(30), nullable=False),
        sa.Column("storage_key", sa.String(500), nullable=False, unique=True),
        sa.Column("original_name", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(150), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum_sha256", sa.String(64)),
        sa.Column("uploaded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("size_bytes > 0", name="ck_stored_files_size"),
    )
    op.create_table("utilities",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("code", sa.String(30), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("unit", sa.String(30), nullable=False),
        sa.Column("rounding_scale", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("rounding_scale >= 0", name="ck_utilities_rounding"),
    )
    op.create_table("meters",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("utility_id", sa.Uuid(), sa.ForeignKey("utilities.id"), nullable=False),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("meter_code", sa.String(50), nullable=False, unique=True),
        sa.Column("serial_number", sa.String(100)), sa.Column("installed_at", sa.Date()),
        sa.Column("initial_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("retired_at", sa.Date()), sa.Column("note", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("initial_reading >= 0", name="ck_meters_initial"),
    )
    op.create_index("ix_meters_room_id", "meters", ["room_id"])
    op.create_table("utility_tariffs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("utility_id", sa.Uuid(), sa.ForeignKey("utilities.id"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False), sa.Column("effective_to", sa.Date()),
        sa.Column("calculation_type", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_tariffs_period"),
        sa.CheckConstraint("calculation_type IN ('Flat','Tiered')", name="ck_tariffs_type"),
    )
    op.create_index("ix_tariffs_utility", "utility_tariffs", ["utility_id", "effective_from"])
    op.create_table("tariff_tiers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("tariff_id", sa.Uuid(), sa.ForeignKey("utility_tariffs.id"), nullable=False),
        sa.Column("tier_order", sa.Integer(), nullable=False),
        sa.Column("from_quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("to_quantity", sa.Numeric(14, 3)),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False),
        sa.UniqueConstraint("tariff_id", "tier_order", name="uq_tariff_tiers_order"),
        sa.CheckConstraint("tier_order > 0 AND from_quantity >= 0 AND unit_price >= 0", name="ck_tariff_tiers_positive"),
        sa.CheckConstraint("to_quantity IS NULL OR to_quantity > from_quantity", name="ck_tariff_tiers_range"),
    )
    op.create_table("utility_import_batches",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False), sa.Column("valid_rows", sa.Integer(), nullable=False),
        sa.Column("invalid_rows", sa.Integer(), nullable=False), sa.Column("preview_rows", sa.JSON()),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("total_rows >= 0 AND valid_rows >= 0 AND invalid_rows >= 0", name="ck_import_counts"),
    )
    op.create_table("meter_readings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("meter_id", sa.Uuid(), sa.ForeignKey("meters.id"), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False), sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("previous_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("current_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("consumption", sa.Numeric(14, 3), nullable=False),
        sa.Column("tariff_id", sa.Uuid(), sa.ForeignKey("utility_tariffs.id"), nullable=False),
        sa.Column("tariff_snapshot", sa.JSON(), nullable=False),
        sa.Column("calculated_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("import_batch_id", sa.Uuid(), sa.ForeignKey("utility_import_batches.id")),
        sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.UniqueConstraint("meter_id", "period_start", "period_end", name="uq_meter_readings_period"),
        sa.CheckConstraint("period_end >= period_start", name="ck_readings_period"),
        sa.CheckConstraint("previous_reading >= 0 AND current_reading >= previous_reading AND consumption = current_reading - previous_reading AND calculated_amount >= 0", name="ck_readings_values"),
    )
    op.create_index("ix_meter_readings_meter", "meter_readings", ["meter_id", "period_end"])


def downgrade() -> None:
    for table in ("meter_readings", "utility_import_batches", "tariff_tiers", "utility_tariffs", "meters", "utilities", "stored_files"):
        op.drop_table(table)
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0006_billing_payments.py`

SHA-256: `07c3787f49fc9c5c7183a0a7da45e79e714cb3901878cef7c126b65a0b0c099d`  
Dòng: 62

```python
"""Add billing and payments with integrated receipt snapshots."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0006"
down_revision = "20260921_0005"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("bills",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_no", sa.String(50), nullable=False, unique=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False), sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("issued_date", sa.Date(), nullable=False), sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("subtotal", sa.Numeric(14, 2), nullable=False), sa.Column("adjustment_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(14, 2), nullable=False), sa.Column("paid_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("balance_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("idempotency_key", sa.String(100), nullable=False, unique=True),
        sa.Column("issued_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("voided_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("voided_at", sa.DateTime(timezone=True)), sa.Column("void_reason", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("period_end >= period_start AND due_date >= issued_date", name="ck_bills_dates"),
        sa.CheckConstraint("subtotal >= 0 AND total_amount >= 0 AND paid_amount >= 0 AND paid_amount <= total_amount AND balance_amount = total_amount - paid_amount", name="ck_bills_amounts"),
    )
    op.create_index("ix_bills_contract_period", "bills", ["contract_id", "period_start", "period_end"])
    op.create_index("ix_bills_student_status_due", "bills", ["student_id", "status", "due_date"])
    op.create_index("uq_nonvoid_bill_period", "bills", ["contract_id", "period_start", "period_end"], unique=True, postgresql_where=sa.text("status <> 'Void'"))
    op.create_table("bill_items",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_id", sa.Uuid(), sa.ForeignKey("bills.id"), nullable=False),
        sa.Column("item_type", sa.String(30), nullable=False), sa.Column("reference_type", sa.String(50)), sa.Column("reference_id", sa.Uuid()),
        sa.Column("description", sa.String(300), nullable=False), sa.Column("quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False), sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("calculation_snapshot", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("quantity >= 0", name="ck_bill_items_quantity"),
    )
    op.create_index("ix_bill_items_bill", "bill_items", ["bill_id"])
    op.create_index("uq_bill_item_reference", "bill_items", ["bill_id", "reference_type", "reference_id"], unique=True, postgresql_where=sa.text("reference_id IS NOT NULL"))
    op.create_table("payments",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_id", sa.Uuid(), sa.ForeignKey("bills.id"), nullable=False),
        sa.Column("payment_no", sa.String(50), nullable=False, unique=True), sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("method", sa.String(30), nullable=False), sa.Column("status", sa.String(20), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False), sa.Column("proof_file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("transaction_reference", sa.String(100), unique=True), sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)), sa.Column("receipt_no", sa.String(50), unique=True),
        sa.Column("receipt_issued_at", sa.DateTime(timezone=True)), sa.Column("receipt_issued_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("receipt_snapshot", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("amount > 0", name="ck_payments_amount"),
        sa.CheckConstraint("status = 'Confirmed' OR (receipt_no IS NULL AND receipt_issued_at IS NULL AND receipt_issued_by IS NULL AND receipt_snapshot IS NULL)", name="ck_payment_receipt_confirmed"),
    )
    op.create_index("ix_payments_bill_status", "payments", ["bill_id", "status", "paid_at"])


def downgrade() -> None:
    op.drop_table("payments"); op.drop_table("bill_items"); op.drop_table("bills")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0007_violations_maintenance.py`

SHA-256: `d70f70eb522edada0a89d6ee8458a90c6677b291d97fcca1864c34fb789ddbad`  
Dòng: 82

```python
"""Add violations and maintenance workflows."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0007"
down_revision = "20260921_0006"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("violation_types",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("code", sa.String(30), unique=True, nullable=False),
        sa.Column("name", sa.String(150), nullable=False), sa.Column("description", sa.String(1000)),
        sa.Column("default_fine_amount", sa.Numeric(14, 2), nullable=False), sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("default_fine_amount >= 0", name="ck_violation_types_fine"),
    )
    op.create_table("violations",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("violation_no", sa.String(50), unique=True, nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id")),
        sa.Column("violation_type_id", sa.Uuid(), sa.ForeignKey("violation_types.id"), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False), sa.Column("location", sa.String(200)),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("fine_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(20), nullable=False), sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)), sa.Column("resolution_note", sa.String(1000)),
        sa.Column("bill_item_id", sa.Uuid(), sa.ForeignKey("bill_items.id"), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("fine_amount >= 0", name="ck_violations_fine"),
    )
    op.create_index("ix_violations_student_status", "violations", ["student_id", "status", "occurred_at"])
    op.create_table("violation_evidences",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("violation_id", sa.Uuid(), sa.ForeignKey("violations.id"), nullable=False),
        sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id"), nullable=False), sa.Column("description", sa.String(300)),
        sa.Column("uploaded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
    )
    op.create_index("ix_violation_evidences_violation", "violation_evidences", ["violation_id"])
    op.create_table("maintenance_requests",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("request_no", sa.String(50), unique=True, nullable=False),
        sa.Column("requester_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")), sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")),
        sa.Column("bed_id", sa.Uuid(), sa.ForeignKey("beds.id")), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("status", sa.String(30), nullable=False), sa.Column("assigned_to", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("deadline", sa.DateTime(timezone=True)), sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("completion_note", sa.String(1000)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("building_id IS NOT NULL OR room_id IS NOT NULL OR bed_id IS NOT NULL", name="ck_maintenance_location"),
    )
    op.create_index("ix_maintenance_requester", "maintenance_requests", ["requester_id", "status", "created_at"])
    op.create_index("ix_maintenance_assignee", "maintenance_requests", ["assigned_to", "status", "created_at"])
    op.create_table("maintenance_events",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("request_id", sa.Uuid(), sa.ForeignKey("maintenance_requests.id"), nullable=False),
        sa.Column("event_type", sa.String(30), nullable=False), sa.Column("old_status", sa.String(30)), sa.Column("new_status", sa.String(30)),
        sa.Column("comment", sa.String(2000)), sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
    )
    op.create_index("ix_maintenance_events_request", "maintenance_events", ["request_id", "created_at"])
    op.create_table("maintenance_plans",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("code", sa.String(50), unique=True, nullable=False),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")), sa.Column("bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("frequency_type", sa.String(20), nullable=False),
        sa.Column("frequency_interval", sa.Integer(), nullable=False), sa.Column("next_due_date", sa.Date(), nullable=False),
        sa.Column("assigned_to", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("frequency_interval > 0", name="ck_maintenance_plan_interval"),
    )


def downgrade() -> None:
    for table in ("maintenance_plans", "maintenance_events", "maintenance_requests", "violation_evidences", "violations", "violation_types"):
        op.drop_table(table)
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0008_notifications.py`

SHA-256: `7f972463d06aee25ef544f0b84ddd9136eb8f5a955eba27d42a1d6353e871e94`  
Dòng: 46

```python
"""Add notifications, targeting and read tracking."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0008"
down_revision = "20260921_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = sa.text("CURRENT_TIMESTAMP")
    op.create_table("notifications",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False), sa.Column("status", sa.String(20), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False), sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)), sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("published_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.CheckConstraint("expires_at IS NULL OR published_at IS NULL OR expires_at > published_at", name="ck_notifications_period"),
    )
    op.create_index("ix_notifications_status_time", "notifications", ["status", "published_at", "expires_at"])
    op.create_table("notification_targets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("notification_id", sa.Uuid(), sa.ForeignKey("notifications.id"), nullable=False),
        sa.Column("target_type", sa.String(20), nullable=False),
        sa.Column("role_id", sa.Uuid(), sa.ForeignKey("roles.id")), sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.CheckConstraint("""(target_type = 'All' AND role_id IS NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Role' AND role_id IS NOT NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Building' AND role_id IS NULL AND building_id IS NOT NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Room' AND role_id IS NULL AND building_id IS NULL AND room_id IS NOT NULL AND user_id IS NULL)
            OR (target_type = 'User' AND role_id IS NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NOT NULL)""", name="ck_notification_target_exactly_one"),
    )
    op.create_index("ix_notification_targets_notification", "notification_targets", ["notification_id"])
    op.create_table("notification_reads",
        sa.Column("notification_id", sa.Uuid(), sa.ForeignKey("notifications.id"), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("read_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("notification_reads"); op.drop_table("notification_targets"); op.drop_table("notifications")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260921_0009_schema_hardening.py`

SHA-256: `01be6614966d638ee709659b5fa3dcc308303aa4a8b96debcb648cc01ba23699`  
Dòng: 35

```python
"""Remove out-of-scope history tables and harden core indexes."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0009"
down_revision = "20260921_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("login_events")
    op.create_index("ix_rooms_scope", "rooms", ["managed_by_staff_id", "building_id", "floor"])
    op.create_index("ix_contracts_student_status_end", "contracts", ["student_id", "status", "end_date"])
    op.create_index("ix_assignments_bed_status_period", "bed_assignments", ["bed_id", "status", "start_date", "end_date"])


def downgrade() -> None:
    op.drop_index("ix_assignments_bed_status_period", table_name="bed_assignments")
    op.drop_index("ix_contracts_student_status_end", table_name="contracts")
    op.drop_index("ix_rooms_scope", table_name="rooms")
    op.create_table("login_events",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("email", sa.String(254), nullable=False), sa.Column("succeeded", sa.Boolean(), nullable=False),
        sa.Column("ip_address", sa.String(64), nullable=False), sa.Column("user_agent", sa.String(500), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_table("audit_logs",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("actor_user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False), sa.Column("before_data", sa.JSON()), sa.Column("after_data", sa.JSON()),
        sa.Column("correlation_id", sa.String(100)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260927_0010_refresh_tokens.py`

SHA-256: `acb48062c96d4801b84d2745b96506ca4a53cd86b50a46010884a2b3556fd7bc`  
Dòng: 28

```python
"""Add rotating refresh-token state to users without creating a new table."""

from alembic import op
import sqlalchemy as sa

revision = "20260927_0010"
down_revision = "20260921_0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("refresh_token_hash", sa.String(64)))
    op.add_column("users", sa.Column("refresh_token_expires_at", sa.DateTime(timezone=True)))
    op.add_column("users", sa.Column("refresh_token_revoked_at", sa.DateTime(timezone=True)))
    op.create_index(
        "ix_users_refresh_token_hash",
        "users",
        ["refresh_token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_users_refresh_token_hash", table_name="users")
    op.drop_column("users", "refresh_token_revoked_at")
    op.drop_column("users", "refresh_token_expires_at")
    op.drop_column("users", "refresh_token_hash")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0011_identity_list_function.py`

SHA-256: `578ede31c731362e81f45c23495f5eb2df015777d6886255bf0402a70ede576f`  
Dòng: 23

```python
"""Install the PostgreSQL function used by the account-list API."""

from importlib.resources import files

from alembic import op

revision = "20260928_0011"
down_revision = "20260927_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statement = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity.sql")
        .read_text(encoding="utf-8")
    )
    op.execute(statement)


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_users(text)")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0012_identity_operations.py`

SHA-256: `5c50d7438735ad56f14a89ebf3eb21feb8ae6cb6a6d5006145b4ff4743c5f62c`  
Dòng: 28

```python
"""Move account reads and writes into PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0012"
down_revision = "20260928_0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity_operations.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_reset_user_password(uuid, text, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_update_user(uuid, text, text, boolean, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_create_user(uuid, text, text, text, text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_user(uuid)")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0013_auth_functions.py`

SHA-256: `227d78c058bdb4ea74f9821d16fc9ddd886f9285e0b77139c35b74bfdecd285e`  
Dòng: 28

```python
"""Use PostgreSQL functions for authentication data access."""

from importlib.resources import files

from alembic import op

revision = "20260928_0013"
down_revision = "20260928_0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "auth.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_revoke_refresh_token(uuid, timestamptz)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_set_refresh_token(uuid, text, timestamptz)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_register_student(uuid, text, text, text, text, date)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_auth_user(uuid, text, text)")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0014_student_reads.py`

SHA-256: `179dcf170e37e95b9ba2db5e1811e2bfd7b4cc80f285012f3f5cfcd9d42a9f64`  
Dòng: 27

```python
"""Read student lists and details through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0014"
down_revision = "20260928_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "students.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_student(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_students(integer, integer)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_count_students()")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0015_identity_profiles.py`

SHA-256: `72d04ae9823c9201aaa4759bd9794d5967d9a4435b0c04eb5dc11e60d36247ea`  
Dòng: 30

```python
"""Use PostgreSQL functions for permissions and student profiles."""

from importlib.resources import files

from alembic import op

revision = "20260928_0015"
down_revision = "20260928_0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity_profiles.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_upsert_student_profile("
        "uuid, text, text, text, date, text, text, text, text, text, text)"
    )
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_student_profile(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_permissions()")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0016_housing_reads.py`

SHA-256: `bda893be865c0d1e8b9509d51c8a76ebd528819c1d39afd68ab0754f199a4aa3`  
Dòng: 30

```python
"""Read housing inventory and room matrix through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0016"
down_revision = "20260928_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "housing_reads.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_room_matrix(uuid)", "fn_get_bed(uuid)", "fn_list_beds(uuid, uuid)",
        "fn_get_room(uuid)", "fn_list_rooms(uuid, uuid)", "fn_get_room_type(uuid)",
        "fn_list_room_types()", "fn_get_building(uuid)", "fn_list_buildings()",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0017_housing_writes.py`

SHA-256: `108c6263d062d5794d0c3dd36b62c05c02bf1b80d8d5f42bb669c8a7af9f031a`  
Dòng: 30

```python
"""Write housing inventory through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0017"
down_revision = "20260928_0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "housing_writes.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_bulk_update_room_gender("
        "uuid[], uuid, integer, text, uuid, boolean)"
    )
    op.execute("DROP FUNCTION IF EXISTS public.fn_deactivate_housing(text, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_save_housing(text, uuid, jsonb, boolean)")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0018_contract_reads.py`

SHA-256: `cc09532bb9bd91994d67a2bea43463ac58e2948f5a1ffdc34d8c2f30add4877e`  
Dòng: 30

```python
"""Read housing applications and contracts through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0018"
down_revision = "20260928_0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "contract_reads.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_assignment_history(uuid)", "fn_get_contract(uuid)",
        "fn_list_contracts(uuid, text)", "fn_get_application(uuid)",
        "fn_list_applications(uuid, text, text)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260928_0019_contract_writes.py`

SHA-256: `4a51c8ee512c6afa83628c5b67a489aedcddc8587e9dccb89ad2326d36fdebda`  
Dòng: 33

```python
"""Write housing application and contract transactions in PostgreSQL."""

from importlib.resources import files

from alembic import op

revision = "20260928_0019"
down_revision = "20260928_0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "contract_writes.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_terminate_contract(uuid, date)",
        "fn_transfer_bed(uuid, uuid, uuid, date)",
        "fn_assign_bed(uuid, uuid, uuid, text, uuid, date, date)",
        "fn_check_bed_available(uuid, date, date)",
        "fn_review_application(uuid, uuid, text, text)",
        "fn_create_application(uuid, uuid, text, uuid)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20260929_0020_simplify_to_17_tables.py`

SHA-256: `bddcbeabc323a59ac766e6015c3bf343fa3a043702d99b752253dad3973ee88e`  
Dòng: 69

```python
"""Keep the 17 tables used by the educational API.

The removed tables contain features outside the selected course scope. Back up
the database before applying this migration if it contains non-demo data.
"""

from importlib.resources import files

from alembic import op


revision = "20260929_0020"
down_revision = "20260928_0019"
branch_labels = None
depends_on = None


def _install_sql(filename: str) -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", filename)
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        if statement.strip():
            op.execute(statement.strip())


def upgrade() -> None:
    # PostgreSQL cannot change the result columns of these functions in place.
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_user(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_users(text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_auth_user(uuid, text, text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_permissions()")

    _install_sql("identity.sql")
    _install_sql("identity_operations.sql")
    _install_sql("auth.sql")

    op.drop_table("role_permissions")
    op.drop_table("permissions")

    op.drop_table("notification_reads")
    op.drop_table("notification_targets")
    op.drop_table("notifications")

    op.drop_table("maintenance_events")
    op.drop_table("maintenance_plans")
    op.drop_table("maintenance_requests")

    op.drop_table("violation_evidences")
    op.drop_table("violations")
    op.drop_table("violation_types")

    op.drop_table("payments")
    op.drop_table("contract_events")
    op.drop_table("room_transfer_requests")

    op.drop_column("meter_readings", "import_batch_id")
    op.drop_column("meter_readings", "source")
    op.drop_table("utility_import_batches")
    op.drop_table("stored_files")


def downgrade() -> None:
    raise RuntimeError(
        "Migration 0020 removes out-of-scope data; restore a pre-upgrade backup to downgrade."
    )
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20261004_0021_utility_billing_functions.py`

SHA-256: `c3da19011a81f3ae32268b97a29476e8770ed4ada02d88087e15ad270e604cb7`  
Dòng: 33

```python
"""Move utility and billing persistence into PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20261004_0021"
down_revision = "20260929_0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_dir = files("dormitory_infrastructure.persistence").joinpath("sql")
    for filename in ("utility_functions.sql", "billing_functions.sql"):
        for statement in sql_dir.joinpath(filename).read_text(encoding="utf-8").split("-- NEXT STATEMENT"):
            if statement.strip():
                op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_generate_bill(uuid, text, uuid, date, date, date, date, text, uuid)",
        "fn_bill_items(uuid)", "fn_list_bills(uuid, text, uuid)", "fn_get_bill(uuid)",
        "fn_create_reading(uuid, uuid, date, date, numeric, numeric, numeric, uuid, json, numeric, uuid)",
        "fn_reading_context(uuid, date, date)", "fn_get_reading(uuid)",
        "fn_list_readings(uuid, date)", "fn_find_tariff(uuid, date)",
        "fn_create_tariff(uuid, uuid, text, date, date, text, uuid, jsonb)",
        "fn_tariff_tiers(uuid)", "fn_get_tariff(uuid)", "fn_list_tariffs(uuid)",
        "fn_create_meter(uuid, uuid, uuid, text, text, date, numeric, text)",
        "fn_get_meter(uuid)", "fn_list_meters(uuid)", "fn_list_utilities()",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
```

## File: `src/backend/dormitory_infrastructure/persistence/migrations/versions/20261004_0022_seed_functions.py`

SHA-256: `0f8a8800defc1d2cc973bed824544ee689c3d4b30e466eecbb14a20aa216169b`  
Dòng: 33

```python
"""Seed and readiness database operations through stored functions."""

from importlib.resources import files

from alembic import op

revision = "20261004_0022"
down_revision = "20261004_0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "seed_functions.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        if statement.strip():
            op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_db_ready()",
        "fn_seed_utility(uuid, text, text, text, integer)",
        "fn_seed_student_profile(uuid, text)",
        "fn_seed_user(uuid, text, text, text, text)",
        "fn_seed_role(uuid, text)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
```

## File: `src/backend/dormitory_infrastructure/persistence/models.py`

SHA-256: `a3d0a206f05326c72b402a7a02fa0f3523135f73f4e52eafb37cdbc7234f4fa9`  
Dòng: 1

```python
# ORM mappings were removed. Persistence uses parameterized SQL and PostgreSQL functions.
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/__init__.py`

SHA-256: `ef8a06db90e45a92dea48997f94cf777c4c3d137d7c8d6c1ab51f3d65e4b3729`  
Dòng: 26

```python
"""Stored-function repository implementations.

Application code imports repositories from this package. SQLAlchemy is used only
for connections, parameters and transactions; business reads/writes are delegated
to PostgreSQL functions installed from ``persistence/sql`` by Alembic.
"""

from .auth import AuthRepository, AuthUser, RoleRef
from .billing import StoredBillingRepository
from .contracts import StoredContractRepository
from .housing import StoredHousingRepository
from .identity import IdentityRepository
from .students import StudentRepository
from .utilities import StoredUtilityRepository

__all__ = [
    "AuthRepository",
    "AuthUser",
    "IdentityRepository",
    "RoleRef",
    "StoredBillingRepository",
    "StoredContractRepository",
    "StoredHousingRepository",
    "StoredUtilityRepository",
    "StudentRepository",
]
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/auth.py`

SHA-256: `2bb0b1f57c4b0bd05913d98af00c9de521450da1dbb5f7038c39fe485ebd9edc`  
Dòng: 80

```python
"""Authentication repository: calls PostgreSQL ``fn_*`` functions only."""

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection


@dataclass(frozen=True)
class RoleRef:
    name: str


@dataclass(frozen=True)
class AuthUser:
    id: UUID
    email: str
    full_name: str
    password_hash: str
    is_active: bool
    role: RoleRef
    refresh_token_expires_at: datetime | None
    refresh_token_revoked_at: datetime | None


class AuthRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def find_user(
        self, *, user_id: UUID | None = None, email: str | None = None,
        refresh_hash: str | None = None,
    ) -> AuthUser | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_auth_user(:user_id, :email, :refresh_hash)"),
            {"user_id": user_id, "email": email, "refresh_hash": refresh_hash},
        ).mappings().first()
        if row is None:
            return None
        return AuthUser(
            id=row["user_id"], email=row["email"], full_name=row["full_name"],
            password_hash=row["password_hash"], is_active=row["is_active"],
            role=RoleRef(row["role_name"]),
            refresh_token_expires_at=row["refresh_token_expires_at"],
            refresh_token_revoked_at=row["refresh_token_revoked_at"],
        )

    def register_student(
        self, email: str, full_name: str, password_hash: str,
        student_code: str, date_of_birth: date,
    ) -> UUID | None:
        user_id = uuid4()
        created = self.db.scalar(
            text(
                "SELECT public.fn_register_student(:user_id, :email, :full_name, "
                ":password_hash, :student_code, :date_of_birth)"
            ),
            {
                "user_id": user_id, "email": email, "full_name": full_name,
                "password_hash": password_hash, "student_code": student_code,
                "date_of_birth": date_of_birth,
            },
        )
        return user_id if created else None

    def set_refresh_token(
        self, user_id: UUID, token_hash: str, expires_at: datetime,
    ) -> None:
        self.db.scalar(
            text("SELECT public.fn_set_refresh_token(:user_id, :token_hash, :expires_at)"),
            {"user_id": user_id, "token_hash": token_hash, "expires_at": expires_at},
        )

    def revoke_refresh_token(self, user_id: UUID, revoked_at: datetime) -> None:
        self.db.scalar(
            text("SELECT public.fn_revoke_refresh_token(:user_id, :revoked_at)"),
            {"user_id": user_id, "revoked_at": revoked_at},
        )
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/billing.py`

SHA-256: `d93bdf84a18ffe7ab78c774f94d9916270a20b8e0db85890db84450a9f07f647`  
Dòng: 64

```python
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from dormitory_application.billing import BillGenerateRequest, BillItemRead, BillRead
from dormitory_application.common import BusinessRuleError, NotFoundError


class StoredBillingRepository:
    """Billing persistence through PostgreSQL stored functions; no table SQL."""

    def __init__(self, db: Connection) -> None:
        self.db = db

    def _bill(self, row) -> BillRead:
        items = self.db.execute(
            text("SELECT * FROM public.fn_bill_items(:id)"),
            {"id": row["id"]},
        ).mappings().all()
        return BillRead(**dict(row), items=[BillItemRead(**dict(item)) for item in items])

    def _get_bill(self, bill_id: UUID):
        return self.db.execute(
            text("SELECT * FROM public.fn_get_bill(:id)"),
            {"id": bill_id},
        ).mappings().one()

    def list_bills(self, user_id: UUID, role: str, contract_id: UUID | None = None) -> list[BillRead]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_bills(:user_id, :role, :contract_id)"),
            {"role": role, "user_id": user_id, "contract_id": contract_id},
        ).mappings().all()
        return [self._bill(row) for row in rows]

    def generate(self, data: BillGenerateRequest, user_id: UUID) -> BillRead:
        try:
            result = self.db.scalar(
                text("SELECT public.fn_generate_bill(:id, :no, :contract_id, :start, "
                     ":end, :issued, :due, :key, :user_id)"),
                {"id": uuid4(), "no": f"HD-{data.period_end:%Y%m}-{uuid4().hex[:8].upper()}",
                 "contract_id": data.contract_id, "start": data.period_start,
                 "end": data.period_end, "issued": data.issued_date,
                 "due": data.due_date, "key": data.idempotency_key,
                 "user_id": user_id},
            )
            if result == "CONTRACT_NOT_FOUND":
                raise NotFoundError("Contract not found")
            errors = {
                "IDEMPOTENCY_KEY_REUSED": ("Khóa chống trùng đã được dùng cho yêu cầu khác.", 409),
                "BILL_PERIOD_OUTSIDE_CONTRACT": ("Kỳ hóa đơn nằm ngoài thời hạn hợp đồng.", 422),
                "BILL_PERIOD_ALREADY_EXISTS": ("Hợp đồng đã có hóa đơn trong kỳ này.", 409),
                "BILL_ROOM_NOT_FOUND": ("Không tìm thấy phòng của hợp đồng trong kỳ hóa đơn.", 409),
            }
            if result in errors:
                message, status = errors[result]
                raise BusinessRuleError(result, message, status)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError("BILL_DATA_CONFLICT",
                                    "Hóa đơn cho hợp đồng và kỳ này đã tồn tại.") from exc
        return self._bill(self._get_bill(UUID(result)))
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/contract_reads.py`

SHA-256: `82782b542113b2a2721d9ef304ee64c62d9d242223e31c395a39427482e2b7a0`  
Dòng: 77

```python
"""Read-side stored-function calls used by the contract repository."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_application.contracts import (
    BedAssignmentRead, ContractRead, HousingApplicationRead,
)


class StoredContractReads:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _rows(self, query: str, **params):
        return self.db.execute(text(query), params).mappings()

    def get_application(self, application_id: UUID) -> HousingApplicationRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_get_application(:application_id)",
            application_id=application_id,
        ).first()
        return HousingApplicationRead.model_validate(dict(row)) if row else None

    def list_applications(
        self, user_id: UUID, role: str, status: str | None,
    ) -> list[HousingApplicationRead]:
        return [HousingApplicationRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_applications(:user_id, :role, :status)",
            user_id=user_id, role=role, status=status,
        )]

    @staticmethod
    def _contract(row) -> ContractRead:
        assignment = None
        if row["assignment_id"] is not None:
            assignment = BedAssignmentRead(
                id=row["assignment_id"], bed_id=row["bed_id"],
                building_code=row["building_code"], room_code=row["room_code"],
                bed_code=row["bed_code"], start_date=row["assignment_start_date"],
                end_date=row["assignment_end_date"], status=row["assignment_status"],
            )
        return ContractRead(
            id=row["id"], contract_no=row["contract_no"],
            student_id=row["student_id"], student_name=row["student_name"],
            application_id=row["application_id"], start_date=row["start_date"],
            end_date=row["end_date"], status=row["status"],
            base_rate=row["base_rate"], current_assignment=assignment,
        )

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return [self._contract(row) for row in self._rows(
            "SELECT * FROM public.fn_list_contracts(:user_id, :role)",
            user_id=user_id, role=role,
        )]

    def get_contract(self, contract_id: UUID) -> ContractRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_get_contract(:contract_id)",
            contract_id=contract_id,
        ).first()
        return self._contract(row) if row else None

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_list_contracts(:student_id, 'Student') LIMIT 1",
            student_id=student_id,
        ).first()
        return self._contract(row) if row else None

    def assignment_history(self, contract_id: UUID) -> list[BedAssignmentRead]:
        return [BedAssignmentRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_assignment_history(:contract_id)",
            contract_id=contract_id,
        )]
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/contract_writes.py`

SHA-256: `2587def4ceda31f3c0641b64b0c8a936ba87c53e7c1fe05bdc3d12fd208cfbd9`  
Dòng: 94

```python
"""Write-side stored-function calls and transaction result mapping."""

from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.contracts import AssignBedRequest, HousingApplicationCreate, TransferBedRequest


_ERRORS = {
    "APPLICATION_ALREADY_EXISTS": ("Bạn đã có đăng ký đang xử lý cho học kỳ này.", 409),
    "APPLICATION_INVALID_STATE": ("Chỉ đăng ký đang chờ mới có thể được duyệt hoặc từ chối.", 409),
    "REJECTION_REASON_REQUIRED": ("Phải nhập lý do từ chối.", 422),
    "APPLICATION_NOT_APPROVED": ("Đăng ký phải được duyệt trước khi phân giường.", 409),
    "CONTRACT_ALREADY_EXISTS": ("Đăng ký này đã có hợp đồng.", 409),
    "BED_NOT_AVAILABLE": ("Giường đang bảo trì hoặc phòng đã ngừng hoạt động.", 409),
    "BED_ASSIGNMENT_CONFLICT": ("Giường đã được phân trong khoảng thời gian này.", 409),
    "CONTRACT_NOT_ACTIVE": ("Hợp đồng không còn hiệu lực.", 409),
    "ACTIVE_ASSIGNMENT_NOT_FOUND": ("Không tìm thấy giường hiện tại.", 409),
    "TRANSFER_DATE_INVALID": ("Ngày chuyển giường không hợp lệ.", 422),
    "SAME_BED_TRANSFER": ("Giường mới phải khác giường hiện tại.", 409),
    "TERMINATION_DATE_INVALID": ("Ngày chấm dứt không hợp lệ.", 422),
}


class StoredContractWrites:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _execute(self, sql: str, params: dict) -> None:
        try:
            result = self.db.execute(text(sql), params).scalar_one()
            if result != "OK":
                self.db.rollback()
                if result in ("NOT_FOUND", "APPLICATION_NOT_FOUND"):
                    raise NotFoundError("Housing application not found")
                if result == "BED_NOT_FOUND":
                    raise NotFoundError("Bed not found")
                if result == "CONTRACT_NOT_FOUND":
                    raise NotFoundError("Contract not found")
                message, status = _ERRORS[result]
                raise BusinessRuleError(result, message, status)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "CONTRACT_DATA_CONFLICT", "Dữ liệu hợp đồng hoặc phân giường bị trùng."
            ) from exc

    def create_application(self, student_id: UUID, data: HousingApplicationCreate) -> UUID:
        item_id = uuid4()
        self._execute(
            "SELECT public.fn_create_application(:id, :student_id, :term_code, :room_type_id)",
            {"id": item_id, "student_id": student_id, "term_code": data.term_code,
             "room_type_id": data.preferred_room_type_id},
        )
        return item_id

    def review_application(
        self, application_id: UUID, reviewer_id: UUID, target_status: str, reason: str | None
    ) -> None:
        self._execute(
            "SELECT public.fn_review_application(:id, :reviewer_id, :status, :reason)",
            {"id": application_id, "reviewer_id": reviewer_id,
             "status": target_status, "reason": reason},
        )

    def assign_bed(self, application_id: UUID, data: AssignBedRequest) -> UUID:
        contract_id = uuid4()
        self._execute(
            "SELECT public.fn_assign_bed(:application_id, :contract_id, :assignment_id, "
            ":contract_no, :bed_id, :start_date, :end_date)",
            {"application_id": application_id, "contract_id": contract_id,
             "assignment_id": uuid4(), "contract_no": f"HD-{data.start_date:%Y%m%d}-{uuid4().hex[:8].upper()}",
             "bed_id": data.bed_id, "start_date": data.start_date, "end_date": data.end_date},
        )
        return contract_id

    def transfer(self, contract_id: UUID, data: TransferBedRequest) -> None:
        self._execute(
            "SELECT public.fn_transfer_bed(:contract_id, :assignment_id, :bed_id, :transfer_date)",
            {"contract_id": contract_id, "assignment_id": uuid4(),
             "bed_id": data.bed_id, "transfer_date": data.transfer_date},
        )

    def terminate(self, contract_id: UUID, termination_date: date) -> None:
        self._execute(
            "SELECT public.fn_terminate_contract(:contract_id, :termination_date)",
            {"contract_id": contract_id, "termination_date": termination_date},
        )
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/contracts.py`

SHA-256: `9ba905beb74ce61b65cd4e43e6fbd05421e11bfdf11f37128619ae6af5b3638a`  
Dòng: 77

```python
"""Contract repository backed only by PostgreSQL functions."""

from datetime import date
from uuid import UUID

from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.contracts import (
    AssignBedRequest, BedAssignmentRead, ContractRead, HousingApplicationCreate,
    HousingApplicationRead, TransferBedRequest,
)

from .contract_reads import StoredContractReads
from .contract_writes import StoredContractWrites


class StoredContractRepository:
    def __init__(self, db: Connection) -> None:
        self.reads = StoredContractReads(db)
        self.writes = StoredContractWrites(db)

    def create_application(
        self, student_id: UUID, data: HousingApplicationCreate
    ) -> HousingApplicationRead:
        item_id = self.writes.create_application(student_id, data)
        return self.reads.get_application(item_id)

    def list_applications(
        self, user_id: UUID, role: str, status: str | None
    ) -> list[HousingApplicationRead]:
        return self.reads.list_applications(user_id, role, status)

    def review_application(
        self, application_id: UUID, reviewer_id: UUID,
        target_status: str, reason: str | None,
    ) -> HousingApplicationRead:
        self.writes.review_application(application_id, reviewer_id, target_status, reason)
        return self.reads.get_application(application_id)

    def assign_bed(self, application_id: UUID, data: AssignBedRequest) -> ContractRead:
        contract_id = self.writes.assign_bed(application_id, data)
        return self._load_contract(contract_id)

    def _load_contract(self, contract_id: UUID) -> ContractRead:
        item = self.reads.get_contract(contract_id)
        if item is None:
            raise NotFoundError("Contract not found")
        return item

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return self.reads.list_contracts(user_id, role)

    def get_contract(self, contract_id: UUID, user_id: UUID, role: str) -> ContractRead:
        item = self._load_contract(contract_id)
        if role == "Student" and item.student_id != user_id:
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ có thể xem hợp đồng của mình.", 403)
        return item

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        return self.reads.get_my_contract(student_id)

    def assignment_history(
        self, contract_id: UUID, user_id: UUID, role: str,
    ) -> list[BedAssignmentRead]:
        contract = self._load_contract(contract_id)
        if role == "Student" and contract.student_id != user_id:
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ có thể xem lịch sử của mình.", 403)
        return self.reads.assignment_history(contract_id)

    def transfer(self, contract_id: UUID, data: TransferBedRequest) -> ContractRead:
        self.writes.transfer(contract_id, data)
        return self._load_contract(contract_id)

    def terminate(self, contract_id: UUID, termination_date: date) -> ContractRead:
        self.writes.terminate(contract_id, termination_date)
        return self._load_contract(contract_id)
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/housing.py`

SHA-256: `13c91fe42b334885a23cc7ff23df1e605b0f78b2ea2c1cafbf07c01757b4b61c`  
Dòng: 124

```python
"""Housing repository backed only by PostgreSQL functions."""

from uuid import UUID, uuid4

from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError
from dormitory_application.housing.schemas import (
    BedCreate, BedRead, BedUpdate, BuildingCreate, BuildingRead, BuildingUpdate,
    RoomBulkGenderUpdate, RoomCreate, RoomMatrixBuilding, RoomRead,
    RoomTypeCreate, RoomTypeRead, RoomTypeUpdate, RoomUpdate,
)

from .housing_reads import StoredHousingReads
from .housing_writes import StoredHousingWrites


class StoredHousingRepository:
    def __init__(self, db: Connection) -> None:
        self.reads = StoredHousingReads(db)
        self.writes = StoredHousingWrites(db)

    def list_buildings(self) -> list[BuildingRead]:
        return self.reads.list_buildings()

    def get_building(self, item_id: UUID) -> BuildingRead | None:
        return self.reads.get_building(item_id)

    def create_building(self, data: BuildingCreate) -> BuildingRead:
        item_id = uuid4()
        self.writes.save("building", item_id, data, True)
        return self.reads.get_building(item_id)

    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead | None:
        return self.reads.get_building(item_id) if self.writes.save(
            "building", item_id, data, False
        ) else None

    def delete_building(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("building", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Tòa nhà đang có sinh viên nội trú.")
        return result == 1

    def list_room_types(self) -> list[RoomTypeRead]:
        return self.reads.list_room_types()

    def create_room_type(self, data: RoomTypeCreate) -> RoomTypeRead:
        item_id = uuid4()
        self.writes.save("room_type", item_id, data, True)
        return self.reads.get_room_type(item_id)

    def update_room_type(self, item_id: UUID, data: RoomTypeUpdate) -> RoomTypeRead | None:
        return self.reads.get_room_type(item_id) if self.writes.save(
            "room_type", item_id, data, False
        ) else None

    def delete_room_type(self, item_id: UUID) -> bool:
        return self.writes.deactivate("room_type", item_id) == 1

    def list_rooms(
        self, building_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[RoomRead]:
        return self.reads.list_rooms(building_id, staff_id)

    def create_room(self, data: RoomCreate) -> RoomRead:
        item_id = uuid4()
        self.writes.save("room", item_id, data, True)
        return self.reads.get_room(item_id)

    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead | None:
        return self.reads.get_room(item_id) if self.writes.save(
            "room", item_id, data, False
        ) else None

    def delete_room(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("room", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Phòng đang có sinh viên nội trú.")
        return result == 1

    def list_beds(
        self, room_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[BedRead]:
        return self.reads.list_beds(room_id, staff_id)

    def create_bed(self, data: BedCreate) -> BedRead:
        item_id = uuid4()
        self.writes.save("bed", item_id, data, True)
        return self.reads.get_bed(item_id)

    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead | None:
        return self.reads.get_bed(item_id) if self.writes.save(
            "bed", item_id, data, False
        ) else None

    def delete_bed(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("bed", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Giường đang được phân cho sinh viên.")
        return result == 1

    def room_matrix(self, staff_id: UUID | None = None) -> list[RoomMatrixBuilding]:
        return self.reads.room_matrix(staff_id)

    def bulk_update_gender(
        self, data: RoomBulkGenderUpdate, actor_id: UUID, is_admin: bool
    ) -> list[RoomRead]:
        result = self.writes.bulk_update_gender(
            data.room_ids, data.building_id, data.floor, data.gender_policy,
            actor_id, is_admin,
        )
        if result == -1:
            raise BusinessRuleError("ROOM_SCOPE_REQUIRED", "Phải chọn tòa, tầng hoặc danh sách phòng.", 422)
        if result == -2:
            raise BusinessRuleError("ROOM_SCOPE_EMPTY", "Không tìm thấy phòng phù hợp.", 404)
        if result == -3:
            raise BusinessRuleError("ROOM_SCOPE_FORBIDDEN", "Staff chỉ được cấu hình phòng mình phụ trách.", 403)
        if result == -4:
            raise BusinessRuleError(
                "ROOM_OCCUPIED_GENDER_LOCKED",
                "Không thể đổi phân khu giới tính khi phòng còn người ở.",
            )
        return self.reads.list_rooms(staff_id=None if is_admin else actor_id)
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/housing_reads.py`

SHA-256: `d5d22945384d697c98ff74fa943351369623b419dfeb57b1a7ac000896d26319`  
Dòng: 98

```python
"""Read-side stored-function calls used by the housing repository."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_application.housing.schemas import (
    BedRead, BuildingRead, RoomMatrixBed, RoomMatrixBuilding,
    RoomMatrixRoom, RoomRead, RoomTypeRead,
)


class StoredHousingReads:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _rows(self, query: str, **params):
        return self.db.execute(text(query), params).mappings()

    def list_buildings(self) -> list[BuildingRead]:
        return [BuildingRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_buildings()"
        )]

    def get_building(self, item_id: UUID) -> BuildingRead | None:
        row = self._rows("SELECT * FROM public.fn_get_building(:item_id)", item_id=item_id).first()
        return BuildingRead.model_validate(dict(row)) if row else None

    def list_room_types(self) -> list[RoomTypeRead]:
        return [RoomTypeRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_room_types()"
        )]

    def get_room_type(self, item_id: UUID) -> RoomTypeRead | None:
        row = self._rows("SELECT * FROM public.fn_get_room_type(:item_id)", item_id=item_id).first()
        return RoomTypeRead.model_validate(dict(row)) if row else None

    def list_rooms(
        self, building_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[RoomRead]:
        return [RoomRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_rooms(:building_id, :staff_id)",
            building_id=building_id, staff_id=staff_id,
        )]

    def get_room(self, item_id: UUID) -> RoomRead | None:
        row = self._rows("SELECT * FROM public.fn_get_room(:item_id)", item_id=item_id).first()
        return RoomRead.model_validate(dict(row)) if row else None

    def list_beds(
        self, room_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[BedRead]:
        return [BedRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_beds(:room_id, :staff_id)",
            room_id=room_id, staff_id=staff_id,
        )]

    def get_bed(self, item_id: UUID) -> BedRead | None:
        row = self._rows("SELECT * FROM public.fn_get_bed(:item_id)", item_id=item_id).first()
        return BedRead.model_validate(dict(row)) if row else None

    def room_matrix(self, staff_id: UUID | None = None) -> list[RoomMatrixBuilding]:
        buildings: dict[UUID, dict] = {}
        rooms: dict[UUID, dict] = {}
        for row in self._rows(
            "SELECT * FROM public.fn_room_matrix(:staff_id)", staff_id=staff_id,
        ):
            building = buildings.setdefault(
                row["building_id"],
                {
                    "id": row["building_id"], "code": row["building_code"],
                    "name": row["building_name"], "rooms": [],
                },
            )
            if row["room_id"] is None:
                continue
            room = rooms.get(row["room_id"])
            if room is None:
                room = {
                    "id": row["room_id"], "code": row["room_code"],
                    "floor": row["floor"], "room_type": row["room_type"],
                    "gender_policy": row["gender_policy"],
                    "managed_by_staff_id": row["managed_by_staff_id"], "beds": [],
                }
                rooms[row["room_id"]] = room
                building["rooms"].append(room)
            if row["bed_id"] is not None:
                room["beds"].append(RoomMatrixBed(
                    id=row["bed_id"], code=row["bed_code"], status=row["bed_status"],
                ))
        return [
            RoomMatrixBuilding(
                id=building["id"], code=building["code"], name=building["name"],
                rooms=[RoomMatrixRoom(**room) for room in building["rooms"]],
            )
            for building in buildings.values()
        ]
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/housing_writes.py`

SHA-256: `06a23e71ae307f57199675cc9822de2eba7feaa495846d8e012cbb1eeffdc493`  
Dòng: 70

```python
"""Write-side stored-function calls used by the housing repository."""

import json
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_application.common import ConflictError


class StoredHousingWrites:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def save(self, entity: str, item_id: UUID, data: BaseModel, create: bool) -> bool:
        try:
            saved = self.db.scalar(
                text(
                    "SELECT public.fn_save_housing("
                    ":entity, :item_id, CAST(:data AS jsonb), :create)"
                ),
                {
                    "entity": entity, "item_id": item_id,
                    "data": json.dumps(data.model_dump(mode="json"), ensure_ascii=False),
                    "create": create,
                },
            )
            if saved:
                self.db.commit()
            else:
                self.db.rollback()
            return bool(saved)
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Duplicate code/name or referenced record is invalid") from exc

    def deactivate(self, entity: str, item_id: UUID) -> int:
        result = int(self.db.scalar(
            text("SELECT public.fn_deactivate_housing(:entity, :item_id)"),
            {"entity": entity, "item_id": item_id},
        ))
        if result == 1:
            self.db.commit()
        else:
            self.db.rollback()
        return result

    def bulk_update_gender(
        self, room_ids: list[UUID], building_id: UUID | None, floor: int | None,
        gender_policy: str, actor_id: UUID, is_admin: bool,
    ) -> int:
        result = int(self.db.scalar(
            text(
                "SELECT public.fn_bulk_update_room_gender("
                ":room_ids, :building_id, :floor, :gender_policy, :actor_id, :is_admin)"
            ),
            {
                "room_ids": room_ids, "building_id": building_id, "floor": floor,
                "gender_policy": gender_policy, "actor_id": actor_id,
                "is_admin": is_admin,
            },
        ))
        if result > 0:
            self.db.commit()
        else:
            self.db.rollback()
        return result
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/identity.py`

SHA-256: `3f111e156690a55b440e2b73510eaed9c388437a2ae394f86ada5a0e0aedf713`  
Dòng: 86

```python
"""Account/profile repository: calls PostgreSQL ``fn_*`` functions only."""

from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection


class IdentityRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    @staticmethod
    def _user(row) -> dict[str, object]:
        return {
            "id": row["user_id"], "email": row["email"],
            "full_name": row["full_name"], "role": row["role_name"],
            "is_active": row["is_active"],
        }

    def list_users(self, role: str | None = None) -> list[dict[str, object]]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_users(:role)"), {"role": role}
        ).mappings()
        return [self._user(row) for row in rows]

    def get_user(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_user(:user_id)"), {"user_id": user_id}
        ).mappings().first()
        return self._user(row) if row else None

    def create_user(
        self, email: str, full_name: str, password_hash: str, role_name: str
    ) -> UUID | None:
        user_id = uuid4()
        created = self.db.scalar(
            text(
                "SELECT public.fn_create_user(:user_id, :email, :full_name, "
                ":password_hash, :role_name)"
            ),
            {
                "user_id": user_id, "email": email, "full_name": full_name,
                "password_hash": password_hash, "role_name": role_name,
            },
        )
        return user_id if created else None

    def update_user(
        self, user_id: UUID, full_name: str, role_name: str,
        is_active: bool, actor_id: UUID,
    ) -> bool:
        return bool(self.db.scalar(
            text(
                "SELECT public.fn_update_user(:user_id, :full_name, :role_name, "
                ":is_active, :actor_id)"
            ),
            {
                "user_id": user_id, "full_name": full_name, "role_name": role_name,
                "is_active": is_active, "actor_id": actor_id,
            },
        ))

    def reset_password(self, user_id: UUID, password_hash: str, actor_id: UUID) -> bool:
        return bool(self.db.scalar(
            text("SELECT public.fn_reset_user_password(:user_id, :password_hash, :actor_id)"),
            {"user_id": user_id, "password_hash": password_hash, "actor_id": actor_id},
        ))

    def get_profile(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_student_profile(:user_id)"),
            {"user_id": user_id},
        ).mappings().first()
        return dict(row) if row else None

    def upsert_profile(self, user_id: UUID, values: dict[str, object]) -> None:
        self.db.scalar(
            text(
                "SELECT public.fn_upsert_student_profile("
                ":user_id, :student_code, :faculty, :cohort, :date_of_birth, "
                ":gender, :phone, :address, :identity_number, "
                ":emergency_contact_name, :emergency_contact_phone)"
            ),
            {"user_id": user_id, **values},
        )
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/students.py`

SHA-256: `1a999536626bf7f23612961ea7266e6583f53ac52b8eed6e6d18c1c6fa7d1206`  
Dòng: 39

```python
"""Student repository: calls PostgreSQL ``fn_*`` functions only."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection


class StudentRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    @staticmethod
    def _row(row) -> dict[str, object]:
        return {
            "id": row["user_id"],
            "student_code": row["student_code"],
            "full_name": row["full_name"],
            "date_of_birth": row["date_of_birth"],
            "email": row["email"],
            "is_active": row["is_active"],
        }

    def count_students(self) -> int:
        return int(self.db.scalar(text("SELECT public.fn_count_students()")) or 0)

    def list_students(self, limit: int, offset: int) -> list[dict[str, object]]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_students(:limit, :offset)"),
            {"limit": limit, "offset": offset},
        ).mappings()
        return [self._row(row) for row in rows]

    def get_student(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_student(:user_id)"),
            {"user_id": user_id},
        ).mappings().first()
        return self._row(row) if row is not None else None
```

## File: `src/backend/dormitory_infrastructure/persistence/repositories/utilities.py`

SHA-256: `ad54558b55e2b74105bda25ba876c7defe283acc116929d5d45338a12bdbbf01`  
Dòng: 235

```python
"""Metering and tariff access through PostgreSQL stored functions."""

import json
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.utilities import (
    MeterCreate, MeterRead, MeterReadingCreate, MeterReadingRead,
    TariffTierRead, UtilityRead, UtilityTariffCreate, UtilityTariffRead,
)
from dormitory_domain.billing import TariffTier, calculate_utility_charge


class StoredUtilityRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _commit(self) -> None:
        self.db.commit()

    def _row(self, sql: str, **params):
        return self.db.execute(text(sql), params).mappings().first()

    def _rows(self, sql: str, **params):
        return self.db.execute(text(sql), params).mappings().all()

    def list_utilities(self) -> list[UtilityRead]:
        rows = self._rows("SELECT * FROM public.fn_list_utilities()")
        return [UtilityRead.model_validate(dict(row)) for row in rows]

    def _meter(self, meter_id: UUID) -> MeterRead | None:
        row = self._row("SELECT * FROM public.fn_get_meter(:meter_id)", meter_id=meter_id)
        return MeterRead.model_validate(dict(row)) if row else None

    def list_meters(self, room_id: UUID | None = None) -> list[MeterRead]:
        rows = self._rows("SELECT * FROM public.fn_list_meters(:room_id)", room_id=room_id)
        return [MeterRead.model_validate(dict(row)) for row in rows]

    def create_meter(self, data: MeterCreate) -> MeterRead:
        meter_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_meter(:id, :utility_id, :room_id, "
                     ":meter_code, :serial_number, :installed_at, :initial_reading, :note)"),
                {
                    "id": meter_id, "utility_id": data.utility_id, "room_id": data.room_id,
                    "meter_code": data.meter_code.strip().upper(),
                    "serial_number": data.serial_number.strip() if data.serial_number else None,
                    "installed_at": data.installed_at,
                    "initial_reading": data.initial_reading, "note": data.note,
                },
            )
            if result != "OK":
                if result in {"UTILITY_NOT_FOUND", "ROOM_NOT_FOUND"}:
                    raise NotFoundError("Utility not found" if result == "UTILITY_NOT_FOUND" else "Room not found")
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._meter(meter_id)

    def _tiers(self, tariff_id: UUID) -> list[TariffTierRead]:
        rows = self._rows("SELECT * FROM public.fn_tariff_tiers(:tariff_id)", tariff_id=tariff_id)
        return [TariffTierRead.model_validate(dict(row)) for row in rows]

    def _tariff(self, row) -> UtilityTariffRead:
        return UtilityTariffRead(
            id=row["id"], utility_id=row["utility_id"],
            utility_code=row["utility_code"], utility_name=row["utility_name"],
            name=row["name"], effective_from=row["effective_from"],
            effective_to=row["effective_to"], calculation_type=row["calculation_type"],
            is_active=row["is_active"], tiers=self._tiers(row["id"]),
        )

    def _tariff_row(self, tariff_id: UUID):
        return self._row("SELECT * FROM public.fn_get_tariff(:tariff_id)", tariff_id=tariff_id)

    def list_tariffs(self, utility_id: UUID | None = None) -> list[UtilityTariffRead]:
        rows = self._rows("SELECT * FROM public.fn_list_tariffs(:utility_id)", utility_id=utility_id)
        return [self._tariff(row) for row in rows]

    def create_tariff(self, data: UtilityTariffCreate, user_id: UUID) -> UtilityTariffRead:
        tariff_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_tariff(:id, :utility_id, :name, "
                     ":effective_from, :effective_to, :calculation_type, :created_by, "
                     "CAST(:tiers AS jsonb))"),
                {
                    "id": tariff_id, "utility_id": data.utility_id,
                    "name": data.name.strip(), "effective_from": data.effective_from,
                    "effective_to": data.effective_to,
                    "calculation_type": data.calculation_type, "created_by": user_id,
                    "tiers": json.dumps([
                        {"id": str(uuid4()), **{
                            key: str(value) if isinstance(value, Decimal) else value
                            for key, value in tier.model_dump().items()
                        }} for tier in data.tiers
                    ]),
                },
            )
            if result == "UTILITY_NOT_FOUND":
                raise NotFoundError("Utility not found")
            if result == "TARIFF_PERIOD_OVERLAP":
                raise BusinessRuleError(
                    result, "Khoảng hiệu lực của biểu giá bị trùng với biểu giá đang hoạt động."
                )
            if result != "OK":
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._tariff(self._tariff_row(tariff_id))

    def _find_tariff(self, utility_id: UUID, period_end: date):
        row = self._row("SELECT * FROM public.fn_find_tariff(:utility_id, :period_end)",
                        utility_id=utility_id, period_end=period_end)
        if row is None:
            raise BusinessRuleError(
                "TARIFF_NOT_FOUND",
                "Không có biểu giá hiệu lực tại ngày kết thúc kỳ ghi chỉ số.",
            )
        return row

    def _reading(self, reading_id: UUID) -> MeterReadingRead:
        row = self._row("SELECT * FROM public.fn_get_reading(:reading_id)",
                        reading_id=reading_id)
        return MeterReadingRead.model_validate(dict(row))

    def create_reading(self, data: MeterReadingCreate, user_id: UUID) -> MeterReadingRead:
        meter = self._row(
            "SELECT * FROM public.fn_reading_context(:meter_id, :period_start, :period_end)",
            meter_id=data.meter_id, period_start=data.period_start, period_end=data.period_end,
        )
        if meter is None or not meter["is_active"]:
            raise NotFoundError("Meter not found")
        if meter["duplicate_id"]:
            raise BusinessRuleError(
                "METER_READING_ALREADY_EXISTS", "Công tơ đã có chỉ số trong kỳ này."
            )
        expected_previous = (meter["previous_reading"] if meter["previous_reading"] is not None
                             else meter["initial_reading"])
        if data.previous_reading != expected_previous:
            raise BusinessRuleError(
                "PREVIOUS_READING_MISMATCH",
                f"Chỉ số đầu kỳ phải bằng {expected_previous}.", 422,
            )
        tariff = self._find_tariff(meter["utility_id"], data.period_end)
        tier_models = self._tiers(tariff["id"])
        tiers = [
            TariffTier(t.tier_order, t.from_quantity, t.to_quantity, t.unit_price)
            for t in tier_models
        ]
        consumption = data.current_reading - data.previous_reading
        calculation = calculate_utility_charge(consumption, tiers, tariff["calculation_type"])
        snapshot = {
            "tariff_id": str(tariff["id"]),
            "name": tariff["name"],
            "calculation_type": tariff["calculation_type"],
            "effective_from": tariff["effective_from"].isoformat(),
            "effective_to": tariff["effective_to"].isoformat() if tariff["effective_to"] else None,
            "tiers": [
                {
                    "tier_order": tier.tier_order,
                    "from_quantity": str(tier.from_quantity),
                    "to_quantity": str(tier.to_quantity) if tier.to_quantity is not None else None,
                    "unit_price": str(tier.unit_price),
                }
                for tier in tiers
            ],
            "breakdown": [
                {
                    "tier_order": charge.tier_order,
                    "billed_quantity": str(charge.billed_quantity),
                    "unit_price": str(charge.unit_price),
                    "amount": str(charge.amount),
                }
                for charge in calculation.breakdown
            ],
        }
        reading_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_reading(:id, :meter_id, :period_start, "
                     ":period_end, :previous_reading, :current_reading, :consumption, "
                     ":tariff_id, CAST(:tariff_snapshot AS json), :calculated_amount, "
                     ":recorded_by)"),
                {
                    "id": reading_id, "meter_id": data.meter_id,
                    "period_start": data.period_start, "period_end": data.period_end,
                    "previous_reading": data.previous_reading,
                    "current_reading": data.current_reading,
                    "consumption": calculation.consumption,
                    "tariff_id": tariff["id"],
                    "tariff_snapshot": json.dumps(snapshot, ensure_ascii=False),
                    "calculated_amount": calculation.total_amount,
                    "recorded_by": user_id,
                },
            )
            if result == "METER_NOT_FOUND":
                raise NotFoundError("Meter not found")
            if result == "METER_READING_ALREADY_EXISTS":
                raise BusinessRuleError(result, "Công tơ đã có chỉ số trong kỳ này.")
            if result == "PREVIOUS_READING_MISMATCH":
                raise BusinessRuleError(result, "Chỉ số đầu kỳ không khớp.", 422)
            if result == "TARIFF_NOT_FOUND":
                raise BusinessRuleError(result, "Không có biểu giá hiệu lực tại ngày kết thúc kỳ ghi chỉ số.")
            if result != "OK":
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._reading(reading_id)

    def list_readings(
        self, meter_id: UUID | None = None, period_start: date | None = None
    ) -> list[MeterReadingRead]:
        rows = self._rows("SELECT * FROM public.fn_list_readings(:meter_id, :period_start)",
                          meter_id=meter_id, period_start=period_start)
        return [MeterReadingRead.model_validate(dict(row)) for row in rows]
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/auth.sql`

SHA-256: `4c5e0808fe4391505f5c2a2a0ef29236f118316201951fb21d994d53a4d17016`  
Dòng: 101

```sql
CREATE OR REPLACE FUNCTION public.fn_auth_user(
    p_user_id uuid DEFAULT NULL,
    p_email text DEFAULT NULL,
    p_refresh_hash text DEFAULT NULL
)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    password_hash text,
    is_active boolean,
    role_name text,
    refresh_token_expires_at timestamptz,
    refresh_token_revoked_at timestamptz
)
LANGUAGE sql
STABLE
AS $function$
    SELECT
        u.id,
        u.email::text,
        u.full_name::text,
        u.password_hash::text,
        u.is_active,
        r.name::text,
        u.refresh_token_expires_at,
        u.refresh_token_revoked_at
    FROM users AS u
    JOIN roles AS r ON r.id = u.role_id
    WHERE (p_user_id IS NOT NULL AND u.id = p_user_id)
       OR (p_email IS NOT NULL AND u.email = p_email)
       OR (p_refresh_hash IS NOT NULL AND u.refresh_token_hash = p_refresh_hash);
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_register_student(
    p_user_id uuid,
    p_email text,
    p_full_name text,
    p_password_hash text,
    p_student_code text,
    p_date_of_birth date
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = 'Student';
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_user_id, p_email, p_full_name, p_password_hash, v_role_id, true);
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, phone, address,
        emergency_contact_name, emergency_contact_phone, date_of_birth
    ) VALUES (
        p_user_id, p_student_code, '', '', '', '', '', '', p_date_of_birth
    );
    RETURN true;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_set_refresh_token(
    p_user_id uuid,
    p_token_hash text,
    p_expires_at timestamptz
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE users
    SET refresh_token_hash = p_token_hash,
        refresh_token_expires_at = p_expires_at,
        refresh_token_revoked_at = NULL
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_revoke_refresh_token(
    p_user_id uuid,
    p_revoked_at timestamptz
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE users
    SET refresh_token_revoked_at = p_revoked_at,
        refresh_token_hash = NULL,
        refresh_token_expires_at = NULL
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/billing_functions.sql`

SHA-256: `a74672b4e38a3d0aaa10157519ed6d1c895deb37a258fdd3a11596aece2a628b`  
Dòng: 113

```sql
CREATE OR REPLACE FUNCTION public.fn_get_bill(p_id uuid)
RETURNS SETOF bills LANGUAGE sql STABLE AS $function$
    SELECT * FROM bills WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_bills(p_user_id uuid, p_role text,
                                                p_contract_id uuid)
RETURNS SETOF bills LANGUAGE sql STABLE AS $function$
    SELECT * FROM bills
    WHERE (p_role <> 'Student' OR student_id = p_user_id)
      AND (p_contract_id IS NULL OR contract_id = p_contract_id)
    ORDER BY issued_date DESC, bill_no DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_bill_items(p_bill_id uuid)
RETURNS SETOF bill_items LANGUAGE sql STABLE AS $function$
    SELECT * FROM bill_items WHERE bill_id = p_bill_id ORDER BY created_at, item_type;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_generate_bill(
    p_id uuid, p_bill_no text, p_contract_id uuid, p_period_start date,
    p_period_end date, p_issued_date date, p_due_date date,
    p_idempotency_key text, p_user_id uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE
    v_existing bills%ROWTYPE;
    v_contract contracts%ROWTYPE;
    v_room_ids uuid[];
    v_reading record;
    v_subtotal numeric(14, 2);
    v_unit_price numeric(14, 2);
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(p_idempotency_key, 0));
    SELECT * INTO v_existing FROM bills WHERE idempotency_key = p_idempotency_key;
    IF FOUND THEN
        IF v_existing.contract_id <> p_contract_id
           OR v_existing.period_start <> p_period_start
           OR v_existing.period_end <> p_period_end THEN
            RETURN 'IDEMPOTENCY_KEY_REUSED';
        END IF;
        RETURN v_existing.id::text;
    END IF;

    SELECT * INTO v_contract FROM contracts WHERE id = p_contract_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'CONTRACT_NOT_FOUND'; END IF;
    IF p_period_end < v_contract.start_date OR p_period_start > v_contract.end_date THEN
        RETURN 'BILL_PERIOD_OUTSIDE_CONTRACT';
    END IF;
    IF EXISTS (SELECT 1 FROM bills WHERE contract_id = p_contract_id
               AND period_start = p_period_start AND period_end = p_period_end
               AND status <> 'Void') THEN
        RETURN 'BILL_PERIOD_ALREADY_EXISTS';
    END IF;
    SELECT array_agg(DISTINCT r.id) INTO v_room_ids
    FROM rooms r JOIN beds b ON b.room_id = r.id
    JOIN bed_assignments ba ON ba.bed_id = b.id
    WHERE ba.contract_id = p_contract_id AND ba.start_date <= p_period_end
      AND (ba.end_date IS NULL OR ba.end_date >= p_period_start);
    IF v_room_ids IS NULL THEN RETURN 'BILL_ROOM_NOT_FOUND'; END IF;

    INSERT INTO bills (id, bill_no, contract_id, student_id, period_start,
                       period_end, issued_date, due_date, status, subtotal,
                       adjustment_amount, total_amount, paid_amount,
                       balance_amount, idempotency_key, issued_by)
    VALUES (p_id, p_bill_no, p_contract_id, v_contract.student_id, p_period_start,
            p_period_end, p_issued_date, p_due_date, 'Issued', 0, 0, 0, 0, 0,
            p_idempotency_key, p_user_id);

    INSERT INTO bill_items (id, bill_id, item_type, reference_type, reference_id,
                            description, quantity, unit_price, amount, calculation_snapshot)
    VALUES (gen_random_uuid(), p_id, 'Housing', 'Contract', p_contract_id,
            format('Phí phòng kỳ %s - %s', to_char(p_period_start, 'DD/MM/YYYY'),
                   to_char(p_period_end, 'DD/MM/YYYY')),
            1, v_contract.base_rate, v_contract.base_rate,
            jsonb_build_object('contract_no', v_contract.contract_no,
                               'base_rate', v_contract.base_rate::text)::json);
    v_subtotal := v_contract.base_rate;

    FOR v_reading IN
        SELECT mr.id, mr.consumption, mr.calculated_amount, mr.previous_reading,
               mr.current_reading, mr.tariff_snapshot, m.meter_code,
               u.code AS utility_code, u.name AS utility_name
        FROM meter_readings mr JOIN meters m ON m.id = mr.meter_id
        JOIN utilities u ON u.id = m.utility_id
        WHERE m.room_id = ANY(v_room_ids) AND mr.period_start = p_period_start
          AND mr.period_end = p_period_end
        ORDER BY u.code, m.meter_code
    LOOP
        v_unit_price := CASE WHEN v_reading.consumption = 0 THEN 0
                        ELSE round(v_reading.calculated_amount / v_reading.consumption, 2)
                        END;
        INSERT INTO bill_items (id, bill_id, item_type, reference_type, reference_id,
                                description, quantity, unit_price, amount,
                                calculation_snapshot)
        VALUES (gen_random_uuid(), p_id, initcap(v_reading.utility_code),
                'MeterReading', v_reading.id,
                v_reading.utility_name || ' - công tơ ' || v_reading.meter_code,
                v_reading.consumption, v_unit_price, v_reading.calculated_amount,
                jsonb_build_object('meter_code', v_reading.meter_code,
                    'previous_reading', v_reading.previous_reading::text,
                    'current_reading', v_reading.current_reading::text,
                    'tariff', v_reading.tariff_snapshot)::json);
        v_subtotal := v_subtotal + v_reading.calculated_amount;
    END LOOP;
    UPDATE bills SET subtotal = v_subtotal, total_amount = v_subtotal,
                     balance_amount = v_subtotal, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
    RETURN p_id::text;
END;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/contract_reads.sql`

SHA-256: `4a340bd99da79215ba406f45680bae12d458d426ca37235df1c863e06a6ae88f`  
Dòng: 99

```sql
CREATE OR REPLACE FUNCTION public.fn_list_applications(
    p_user_id uuid, p_role text, p_status text DEFAULT NULL
)
RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    preferred_room_type_id uuid, preferred_room_type_name text,
    status text, rejection_reason text, created_at timestamptz
)
LANGUAGE sql STABLE
AS $function$
    SELECT a.id, a.student_id, u.full_name::text, a.term_code::text,
           a.preferred_room_type_id, rt.name::text, a.status::text,
           a.rejection_reason::text, a.created_at
    FROM housing_applications AS a
    JOIN users AS u ON u.id = a.student_id
    JOIN room_types AS rt ON rt.id = a.preferred_room_type_id
    WHERE (p_role <> 'Student' OR a.student_id = p_user_id)
      AND (p_status IS NULL OR a.status = p_status)
    ORDER BY a.created_at DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_application(p_id uuid)
RETURNS TABLE (
    id uuid, student_id uuid, student_name text, term_code text,
    preferred_room_type_id uuid, preferred_room_type_name text,
    status text, rejection_reason text, created_at timestamptz
)
LANGUAGE sql STABLE
AS $function$
    SELECT a.id, a.student_id, u.full_name::text, a.term_code::text,
           a.preferred_room_type_id, rt.name::text, a.status::text,
           a.rejection_reason::text, a.created_at
    FROM housing_applications AS a
    JOIN users AS u ON u.id = a.student_id
    JOIN room_types AS rt ON rt.id = a.preferred_room_type_id
    WHERE a.id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_contracts(p_user_id uuid, p_role text)
RETURNS TABLE (
    id uuid, contract_no text, student_id uuid, student_name text,
    application_id uuid, start_date date, end_date date, status text,
    base_rate numeric, assignment_id uuid, bed_id uuid,
    building_code text, room_code text, bed_code text,
    assignment_start_date date, assignment_end_date date, assignment_status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT c.id, c.contract_no::text, c.student_id, u.full_name::text,
           c.application_id, c.start_date, c.end_date, c.status::text,
           c.base_rate, a.id, a.bed_id, b.code::text, r.code::text,
           bed.code::text, a.start_date, a.end_date, a.status::text
    FROM contracts AS c
    JOIN users AS u ON u.id = c.student_id
    LEFT JOIN LATERAL (
        SELECT * FROM bed_assignments
        WHERE contract_id = c.id AND status = 'Active'
        ORDER BY start_date DESC LIMIT 1
    ) AS a ON true
    LEFT JOIN beds AS bed ON bed.id = a.bed_id
    LEFT JOIN rooms AS r ON r.id = bed.room_id
    LEFT JOIN buildings AS b ON b.id = r.building_id
    WHERE p_role <> 'Student' OR c.student_id = p_user_id
    ORDER BY c.start_date DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_contract(p_id uuid)
RETURNS TABLE (
    id uuid, contract_no text, student_id uuid, student_name text,
    application_id uuid, start_date date, end_date date, status text,
    base_rate numeric, assignment_id uuid, bed_id uuid,
    building_code text, room_code text, bed_code text,
    assignment_start_date date, assignment_end_date date, assignment_status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_contracts(NULL, 'Admin') WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_assignment_history(p_contract_id uuid)
RETURNS TABLE (
    id uuid, bed_id uuid, building_code text, room_code text,
    bed_code text, start_date date, end_date date, status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT a.id, a.bed_id, b.code::text, r.code::text, bed.code::text,
           a.start_date, a.end_date, a.status::text
    FROM bed_assignments AS a
    JOIN beds AS bed ON bed.id = a.bed_id
    JOIN rooms AS r ON r.id = bed.room_id
    JOIN buildings AS b ON b.id = r.building_id
    WHERE a.contract_id = p_contract_id
    ORDER BY a.start_date;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/contract_writes.sql`

SHA-256: `340214251b7a48ae6d31a6a5af9de8bf8026a81d88a389c09b94527dae8e5049`  
Dòng: 185

```sql
CREATE OR REPLACE FUNCTION public.fn_create_application(
    p_id uuid, p_student_id uuid, p_term_code text, p_room_type_id uuid
)
RETURNS text
LANGUAGE plpgsql
AS $function$
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended(p_student_id::text, 0));
    IF EXISTS (
        SELECT 1 FROM housing_applications
        WHERE student_id = p_student_id
          AND term_code = upper(trim(p_term_code))
          AND status IN ('Submitted', 'Approved')
    ) THEN RETURN 'APPLICATION_ALREADY_EXISTS'; END IF;
    INSERT INTO housing_applications (
        id, student_id, term_code, preferred_room_type_id, status
    ) VALUES (
        p_id, p_student_id, upper(trim(p_term_code)), p_room_type_id, 'Submitted'
    );
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_review_application(
    p_application_id uuid, p_reviewer_id uuid, p_status text, p_reason text
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_status text;
BEGIN
    SELECT status INTO v_status FROM housing_applications
    WHERE id = p_application_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'NOT_FOUND'; END IF;
    IF v_status <> 'Submitted' THEN RETURN 'APPLICATION_INVALID_STATE'; END IF;
    IF p_status = 'Rejected' AND (p_reason IS NULL OR trim(p_reason) = '') THEN
        RETURN 'REJECTION_REASON_REQUIRED';
    END IF;
    UPDATE housing_applications SET
        status = p_status, rejection_reason = p_reason,
        reviewed_by_user_id = p_reviewer_id, reviewed_at = CURRENT_TIMESTAMP
    WHERE id = p_application_id;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_check_bed_available(
    p_bed_id uuid, p_start_date date, p_end_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_bed_active boolean;
    v_room_active boolean;
BEGIN
    SELECT bed.is_active, room.is_active INTO v_bed_active, v_room_active
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    WHERE bed.id = p_bed_id
    FOR UPDATE OF bed;
    IF NOT FOUND THEN RETURN 'BED_NOT_FOUND'; END IF;
    IF NOT v_bed_active OR NOT v_room_active THEN RETURN 'BED_NOT_AVAILABLE'; END IF;
    IF EXISTS (
        SELECT 1 FROM bed_assignments
        WHERE bed_id = p_bed_id AND start_date <= p_end_date
          AND (end_date IS NULL OR end_date >= p_start_date)
    ) THEN RETURN 'BED_ASSIGNMENT_CONFLICT'; END IF;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_assign_bed(
    p_application_id uuid, p_contract_id uuid, p_assignment_id uuid,
    p_contract_no text, p_bed_id uuid, p_start_date date, p_end_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_student_id uuid;
    v_status text;
    v_bed_status text;
    v_base_rate numeric;
BEGIN
    SELECT student_id, status INTO v_student_id, v_status
    FROM housing_applications WHERE id = p_application_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'APPLICATION_NOT_FOUND'; END IF;
    IF v_status <> 'Approved' THEN RETURN 'APPLICATION_NOT_APPROVED'; END IF;
    IF EXISTS (SELECT 1 FROM contracts WHERE application_id = p_application_id) THEN
        RETURN 'CONTRACT_ALREADY_EXISTS';
    END IF;
    v_bed_status := public.fn_check_bed_available(p_bed_id, p_start_date, p_end_date);
    IF v_bed_status <> 'OK' THEN RETURN v_bed_status; END IF;
    SELECT rt.default_monthly_rate INTO v_base_rate
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    JOIN room_types AS rt ON rt.id = room.room_type_id
    WHERE bed.id = p_bed_id;
    INSERT INTO contracts (
        id, contract_no, student_id, application_id, start_date,
        end_date, status, base_rate
    ) VALUES (
        p_contract_id, p_contract_no, v_student_id, p_application_id,
        p_start_date, p_end_date, 'Active', v_base_rate
    );
    INSERT INTO bed_assignments (id, contract_id, bed_id, start_date, status)
    VALUES (p_assignment_id, p_contract_id, p_bed_id, p_start_date, 'Active');
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_transfer_bed(
    p_contract_id uuid, p_new_assignment_id uuid, p_bed_id uuid, p_transfer_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_contract_status text;
    v_contract_end date;
    v_current_id uuid;
    v_current_bed_id uuid;
    v_current_start date;
    v_bed_status text;
BEGIN
    SELECT status, end_date INTO v_contract_status, v_contract_end
    FROM contracts WHERE id = p_contract_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'CONTRACT_NOT_FOUND'; END IF;
    IF v_contract_status <> 'Active' THEN RETURN 'CONTRACT_NOT_ACTIVE'; END IF;
    SELECT id, bed_id, start_date INTO v_current_id, v_current_bed_id, v_current_start
    FROM bed_assignments
    WHERE contract_id = p_contract_id AND status = 'Active' FOR UPDATE;
    IF NOT FOUND THEN RETURN 'ACTIVE_ASSIGNMENT_NOT_FOUND'; END IF;
    IF p_transfer_date <= v_current_start OR p_transfer_date > v_contract_end THEN
        RETURN 'TRANSFER_DATE_INVALID';
    END IF;
    IF v_current_bed_id = p_bed_id THEN RETURN 'SAME_BED_TRANSFER'; END IF;
    v_bed_status := public.fn_check_bed_available(p_bed_id, p_transfer_date, v_contract_end);
    IF v_bed_status <> 'OK' THEN RETURN v_bed_status; END IF;
    UPDATE bed_assignments SET status = 'Ended', end_date = p_transfer_date
    WHERE id = v_current_id;
    INSERT INTO bed_assignments (id, contract_id, bed_id, start_date, status)
    VALUES (p_new_assignment_id, p_contract_id, p_bed_id, p_transfer_date, 'Active');
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_terminate_contract(
    p_contract_id uuid, p_termination_date date
)
RETURNS text
LANGUAGE plpgsql
AS $function$
DECLARE
    v_contract_status text;
    v_contract_end date;
    v_assignment_id uuid;
    v_assignment_start date;
BEGIN
    SELECT status, end_date INTO v_contract_status, v_contract_end
    FROM contracts WHERE id = p_contract_id FOR UPDATE;
    IF NOT FOUND THEN RETURN 'CONTRACT_NOT_FOUND'; END IF;
    IF v_contract_status <> 'Active' THEN RETURN 'CONTRACT_NOT_ACTIVE'; END IF;
    SELECT id, start_date INTO v_assignment_id, v_assignment_start
    FROM bed_assignments
    WHERE contract_id = p_contract_id AND status = 'Active' FOR UPDATE;
    IF NOT FOUND THEN RETURN 'ACTIVE_ASSIGNMENT_NOT_FOUND'; END IF;
    IF p_termination_date < v_assignment_start OR p_termination_date > v_contract_end THEN
        RETURN 'TERMINATION_DATE_INVALID';
    END IF;
    UPDATE bed_assignments SET status = 'Ended', end_date = p_termination_date
    WHERE id = v_assignment_id;
    UPDATE contracts SET status = 'Terminated', terminated_at = CURRENT_TIMESTAMP,
                         updated_at = CURRENT_TIMESTAMP
    WHERE id = p_contract_id;
    RETURN 'OK';
END;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/housing_reads.sql`

SHA-256: `4b0e97652f854cb9b421c2f55119139a03acef96fdb0fcbd461fef88d78ddeca`  
Dòng: 117

```sql
CREATE OR REPLACE FUNCTION public.fn_list_buildings()
RETURNS SETOF buildings
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM buildings ORDER BY code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_building(p_id uuid)
RETURNS SETOF buildings
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM buildings WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_room_types()
RETURNS SETOF room_types
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM room_types ORDER BY name;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_room_type(p_id uuid)
RETURNS SETOF room_types
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM room_types WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_rooms(p_building_id uuid DEFAULT NULL, p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text, room_type_id uuid,
    room_type_name text, code text, floor integer, gender_policy text,
    managed_by_staff_id uuid, status text, is_active boolean, note text
)
LANGUAGE sql STABLE
AS $function$
    SELECT r.id, r.building_id, b.code::text, r.room_type_id,
           rt.name::text, r.code::text, r.floor, r.gender_policy::text,
           r.managed_by_staff_id, r.status::text, r.is_active, r.note::text
    FROM rooms AS r
    JOIN buildings AS b ON b.id = r.building_id
    JOIN room_types AS rt ON rt.id = r.room_type_id
    WHERE (p_building_id IS NULL OR r.building_id = p_building_id)
      AND (p_staff_id IS NULL OR r.managed_by_staff_id = p_staff_id)
    ORDER BY r.floor, r.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_room(p_id uuid)
RETURNS TABLE (
    id uuid, building_id uuid, building_code text, room_type_id uuid,
    room_type_name text, code text, floor integer, gender_policy text,
    managed_by_staff_id uuid, status text, is_active boolean, note text
)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_rooms(NULL, NULL) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_beds(p_room_id uuid DEFAULT NULL, p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (id uuid, room_id uuid, code text, is_active boolean, note text, status text)
LANGUAGE sql STABLE
AS $function$
    SELECT bed.id, bed.room_id, bed.code::text, bed.is_active, bed.note::text,
           CASE WHEN NOT bed.is_active THEN 'Maintenance'
                WHEN EXISTS (
                    SELECT 1 FROM bed_assignments AS a
                    WHERE a.bed_id = bed.id AND a.status = 'Active'
                ) THEN 'Occupied'
                ELSE 'Available' END::text
    FROM beds AS bed
    JOIN rooms AS room ON room.id = bed.room_id
    WHERE (p_room_id IS NULL OR bed.room_id = p_room_id)
      AND (p_staff_id IS NULL OR room.managed_by_staff_id = p_staff_id)
    ORDER BY bed.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_bed(p_id uuid)
RETURNS TABLE (id uuid, room_id uuid, code text, is_active boolean, note text, status text)
LANGUAGE sql STABLE
AS $function$
    SELECT * FROM public.fn_list_beds(NULL, NULL) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_room_matrix(p_staff_id uuid DEFAULT NULL)
RETURNS TABLE (
    building_id uuid, building_code text, building_name text,
    room_id uuid, room_code text, floor integer, room_type text,
    gender_policy text, managed_by_staff_id uuid,
    bed_id uuid, bed_code text, bed_status text
)
LANGUAGE sql STABLE
AS $function$
    SELECT building.id, building.code::text, building.name::text,
           room.id, room.code::text, room.floor, rt.name::text,
           room.gender_policy::text, room.managed_by_staff_id,
           bed.id, bed.code::text,
           CASE WHEN NOT bed.is_active THEN 'Maintenance'
                WHEN EXISTS (
                    SELECT 1 FROM bed_assignments AS a
                    WHERE a.bed_id = bed.id AND a.status = 'Active'
                ) THEN 'Occupied'
                ELSE 'Available' END::text
    FROM buildings AS building
    LEFT JOIN rooms AS room ON room.building_id = building.id
    LEFT JOIN room_types AS rt ON rt.id = room.room_type_id
    LEFT JOIN beds AS bed ON bed.room_id = room.id
    WHERE p_staff_id IS NULL OR room.managed_by_staff_id = p_staff_id
    ORDER BY building.code, room.floor, room.code, bed.code;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/housing_writes.sql`

SHA-256: `ad964072bf27e97b463eaf9dfc807e066df051ea87e52e5a91474277b49f8f06`  
Dòng: 185

```sql
CREATE OR REPLACE FUNCTION public.fn_save_housing(
    p_entity text, p_id uuid, p_data jsonb, p_create boolean
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    CASE p_entity
        WHEN 'building' THEN
            IF p_create THEN
                INSERT INTO buildings (id, code, name, address, floors, is_active)
                VALUES (
                    p_id, upper(trim(p_data->>'code')), p_data->>'name',
                    p_data->>'address', (p_data->>'floors')::integer,
                    (p_data->>'is_active')::boolean
                );
                RETURN true;
            END IF;
            UPDATE buildings SET
                code = upper(trim(p_data->>'code')),
                name = p_data->>'name', address = p_data->>'address',
                floors = (p_data->>'floors')::integer,
                is_active = (p_data->>'is_active')::boolean,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'room_type' THEN
            IF p_create THEN
                INSERT INTO room_types (
                    id, name, default_monthly_rate, default_capacity,
                    description, is_active
                ) VALUES (
                    p_id, trim(p_data->>'name'),
                    (p_data->>'default_monthly_rate')::numeric,
                    (p_data->>'default_capacity')::integer,
                    p_data->>'description', (p_data->>'is_active')::boolean
                );
                RETURN true;
            END IF;
            UPDATE room_types SET
                name = trim(p_data->>'name'),
                default_monthly_rate = (p_data->>'default_monthly_rate')::numeric,
                default_capacity = (p_data->>'default_capacity')::integer,
                description = p_data->>'description',
                is_active = (p_data->>'is_active')::boolean,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'room' THEN
            IF p_create THEN
                INSERT INTO rooms (
                    id, building_id, room_type_id, code, floor, gender_policy,
                    managed_by_staff_id, status, is_active, note
                ) VALUES (
                    p_id, (p_data->>'building_id')::uuid,
                    (p_data->>'room_type_id')::uuid, upper(trim(p_data->>'code')),
                    (p_data->>'floor')::integer, p_data->>'gender_policy',
                    (p_data->>'managed_by_staff_id')::uuid, p_data->>'status',
                    (p_data->>'is_active')::boolean, p_data->>'note'
                );
                RETURN true;
            END IF;
            UPDATE rooms SET
                building_id = (p_data->>'building_id')::uuid,
                room_type_id = (p_data->>'room_type_id')::uuid,
                code = upper(trim(p_data->>'code')),
                floor = (p_data->>'floor')::integer,
                gender_policy = p_data->>'gender_policy',
                managed_by_staff_id = (p_data->>'managed_by_staff_id')::uuid,
                status = p_data->>'status',
                is_active = (p_data->>'is_active')::boolean,
                note = p_data->>'note', updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        WHEN 'bed' THEN
            IF p_create THEN
                INSERT INTO beds (id, room_id, code, is_active, note)
                VALUES (
                    p_id, (p_data->>'room_id')::uuid,
                    upper(trim(p_data->>'code')),
                    (p_data->>'is_active')::boolean, p_data->>'note'
                );
                RETURN true;
            END IF;
            UPDATE beds SET
                room_id = (p_data->>'room_id')::uuid,
                code = upper(trim(p_data->>'code')),
                is_active = (p_data->>'is_active')::boolean,
                note = p_data->>'note', updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            RETURN FOUND;
        ELSE
            RAISE EXCEPTION 'Unknown housing entity';
    END CASE;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_deactivate_housing(p_entity text, p_id uuid)
RETURNS integer
LANGUAGE plpgsql
AS $function$
BEGIN
    CASE p_entity
        WHEN 'building' THEN
            PERFORM 1 FROM buildings WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments AS a
                JOIN beds AS bed ON bed.id = a.bed_id
                JOIN rooms AS room ON room.id = bed.room_id
                WHERE room.building_id = p_id AND a.status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE buildings SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        WHEN 'room_type' THEN
            UPDATE room_types SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
            IF NOT FOUND THEN RETURN 0; END IF;
        WHEN 'room' THEN
            PERFORM 1 FROM rooms WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments AS a
                JOIN beds AS bed ON bed.id = a.bed_id
                WHERE bed.room_id = p_id AND a.status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE rooms SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        WHEN 'bed' THEN
            PERFORM 1 FROM beds WHERE id = p_id FOR UPDATE;
            IF NOT FOUND THEN RETURN 0; END IF;
            IF EXISTS (
                SELECT 1 FROM bed_assignments
                WHERE bed_id = p_id AND status = 'Active'
            ) THEN RETURN -1; END IF;
            UPDATE beds SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = p_id;
        ELSE
            RAISE EXCEPTION 'Unknown housing entity';
    END CASE;
    RETURN 1;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_bulk_update_room_gender(
    p_room_ids uuid[], p_building_id uuid, p_floor integer,
    p_gender_policy text, p_actor_id uuid, p_is_admin boolean
)
RETURNS integer
LANGUAGE plpgsql
AS $function$
DECLARE
    v_room_ids uuid[] := ARRAY[]::uuid[];
    v_room_id uuid;
BEGIN
    IF cardinality(p_room_ids) = 0 AND p_building_id IS NULL THEN
        RETURN -1;
    END IF;
    FOR v_room_id IN
        SELECT id FROM rooms
        WHERE (cardinality(p_room_ids) > 0 AND id = ANY(p_room_ids))
           OR (cardinality(p_room_ids) = 0 AND building_id = p_building_id
               AND (p_floor IS NULL OR floor = p_floor))
        FOR UPDATE
    LOOP
        v_room_ids := array_append(v_room_ids, v_room_id);
    END LOOP;
    IF cardinality(v_room_ids) = 0 THEN RETURN -2; END IF;
    IF NOT p_is_admin AND EXISTS (
        SELECT 1 FROM rooms
        WHERE id = ANY(v_room_ids) AND managed_by_staff_id IS DISTINCT FROM p_actor_id
    ) THEN RETURN -3; END IF;
    IF EXISTS (
        SELECT 1 FROM bed_assignments AS a
        JOIN beds AS bed ON bed.id = a.bed_id
        WHERE bed.room_id = ANY(v_room_ids) AND a.status = 'Active'
    ) THEN RETURN -4; END IF;
    UPDATE rooms SET gender_policy = p_gender_policy,
                     updated_by = p_actor_id, updated_at = CURRENT_TIMESTAMP
    WHERE id = ANY(v_room_ids);
    RETURN cardinality(v_room_ids);
END;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/identity.sql`

SHA-256: `60354a501810b492c07e34db00a7a737f403491ebbc19c75f3f3aa119cbdea2f`  
Dòng: 24

```sql
-- Public result contract for GET /api/v1/users.
-- The API may continue calling this function while the SELECT body is optimized.
CREATE OR REPLACE FUNCTION public.fn_list_users(p_role text DEFAULT NULL)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    role_name text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT
        u.id,
        u.email::text,
        u.full_name::text,
        r.name::text,
        u.is_active
    FROM users AS u
    JOIN roles AS r ON r.id = u.role_id
    WHERE p_role IS NULL OR r.name = p_role
    ORDER BY u.full_name;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/identity_operations.sql`

SHA-256: `ce74273e923c09bbfaf02902d6f006b60f6641f70d49c3ac3bee6c528d398142`  
Dòng: 89

```sql
-- Each statement is installed separately by Alembic.
CREATE OR REPLACE FUNCTION public.fn_get_user(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    role_name text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT users.user_id, users.email, users.full_name, users.role_name,
           users.is_active
    FROM public.fn_list_users(NULL) AS users
    WHERE users.user_id = p_user_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_user(
    p_user_id uuid,
    p_email text,
    p_full_name text,
    p_password_hash text,
    p_role_name text
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_user_id, p_email, p_full_name, p_password_hash, v_role_id, true);
    RETURN true;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_update_user(
    p_user_id uuid,
    p_full_name text,
    p_role_name text,
    p_is_active boolean,
    p_actor_id uuid
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
DECLARE
    v_role_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RETURN false;
    END IF;
    UPDATE users
    SET full_name = p_full_name,
        role_id = v_role_id,
        is_active = p_is_active,
        updated_by = p_actor_id,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_reset_user_password(
    p_user_id uuid,
    p_password_hash text,
    p_actor_id uuid
)
RETURNS boolean
LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE users
    SET password_hash = p_password_hash,
        updated_by = p_actor_id,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_user_id;
    RETURN FOUND;
END;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/identity_profiles.sql`

SHA-256: `dcd8b470a39956e9723576e7018043ae149191402194b3315f0473d9130c6a8d`  
Dòng: 68

```sql
CREATE OR REPLACE FUNCTION public.fn_get_student_profile(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    email text,
    full_name text,
    student_code text,
    faculty text,
    cohort text,
    date_of_birth date,
    gender text,
    phone text,
    address text,
    identity_number text,
    emergency_contact_name text,
    emergency_contact_phone text
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, u.email::text, u.full_name::text,
           sp.student_code::text, sp.faculty::text, sp.cohort::text,
           sp.date_of_birth, sp.gender::text, sp.phone::text,
           sp.address::text, sp.identity_number::text,
           sp.emergency_contact_name::text, sp.emergency_contact_phone::text
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    WHERE sp.user_id = p_user_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_upsert_student_profile(
    p_user_id uuid,
    p_student_code text,
    p_faculty text,
    p_cohort text,
    p_date_of_birth date,
    p_gender text,
    p_phone text,
    p_address text,
    p_identity_number text,
    p_emergency_contact_name text,
    p_emergency_contact_phone text
)
RETURNS void
LANGUAGE sql
AS $function$
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, date_of_birth, gender,
        phone, address, identity_number, emergency_contact_name,
        emergency_contact_phone
    ) VALUES (
        p_user_id, p_student_code, p_faculty, p_cohort, p_date_of_birth,
        p_gender, p_phone, p_address, p_identity_number,
        p_emergency_contact_name, p_emergency_contact_phone
    )
    ON CONFLICT (user_id) DO UPDATE SET
        student_code = EXCLUDED.student_code,
        faculty = EXCLUDED.faculty,
        cohort = EXCLUDED.cohort,
        date_of_birth = EXCLUDED.date_of_birth,
        gender = EXCLUDED.gender,
        phone = EXCLUDED.phone,
        address = EXCLUDED.address,
        identity_number = EXCLUDED.identity_number,
        emergency_contact_name = EXCLUDED.emergency_contact_name,
        emergency_contact_phone = EXCLUDED.emergency_contact_phone,
        updated_at = CURRENT_TIMESTAMP;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/seed_functions.sql`

SHA-256: `fb5b4c1df44ca18efe3afb1c4ccef934dc1922964d8f29a6cf5fa57483138607`  
Dòng: 55

```sql
CREATE OR REPLACE FUNCTION public.fn_seed_role(p_id uuid, p_name text)
RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO roles (id, name, is_active)
    VALUES (p_id, p_name, true)
    ON CONFLICT (name) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_user(
    p_id uuid, p_email text, p_full_name text, p_password_hash text, p_role_name text
) RETURNS uuid LANGUAGE plpgsql AS $function$
DECLARE v_role_id uuid; v_user_id uuid;
BEGIN
    SELECT id INTO v_role_id FROM roles WHERE name = p_role_name;
    IF v_role_id IS NULL THEN
        RAISE EXCEPTION 'Unknown seeded role: %', p_role_name;
    END IF;
    INSERT INTO users (id, email, full_name, password_hash, role_id, is_active)
    VALUES (p_id, p_email, p_full_name, p_password_hash, v_role_id, true)
    ON CONFLICT (email) DO NOTHING;
    SELECT id INTO v_user_id FROM users WHERE email = p_email;
    RETURN v_user_id;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_student_profile(p_user_id uuid, p_student_code text)
RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO student_profiles (
        user_id, student_code, faculty, cohort, phone, address,
        emergency_contact_name, emergency_contact_phone
    ) VALUES (p_user_id, p_student_code, '', '', '', '', '', '')
    ON CONFLICT (user_id) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_seed_utility(
    p_id uuid, p_code text, p_name text, p_unit text, p_rounding_scale integer
) RETURNS void LANGUAGE plpgsql AS $function$
BEGIN
    INSERT INTO utilities (id, code, name, unit, rounding_scale, is_active)
    VALUES (p_id, p_code, p_name, p_unit, p_rounding_scale, true)
    ON CONFLICT (code) DO NOTHING;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_db_ready()
RETURNS integer LANGUAGE sql STABLE AS $function$
    SELECT 1;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/students.sql`

SHA-256: `1b530cc9cdfa5e7b2a49722d8807bb4413cc8e7b67ebfa50e405b489c2179213`  
Dòng: 48

```sql
CREATE OR REPLACE FUNCTION public.fn_count_students()
RETURNS bigint
LANGUAGE sql
STABLE
AS $function$
    SELECT count(*) FROM student_profiles;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_students(p_limit integer, p_offset integer)
RETURNS TABLE (
    user_id uuid,
    student_code text,
    full_name text,
    date_of_birth date,
    email text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, sp.student_code::text, u.full_name::text,
           sp.date_of_birth, u.email::text, u.is_active
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    ORDER BY u.full_name, sp.student_code
    LIMIT p_limit OFFSET p_offset;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_student(p_user_id uuid)
RETURNS TABLE (
    user_id uuid,
    student_code text,
    full_name text,
    date_of_birth date,
    email text,
    is_active boolean
)
LANGUAGE sql
STABLE
AS $function$
    SELECT sp.user_id, sp.student_code::text, u.full_name::text,
           sp.date_of_birth, u.email::text, u.is_active
    FROM student_profiles AS sp
    JOIN users AS u ON u.id = sp.user_id
    WHERE sp.user_id = p_user_id;
$function$;
```

## File: `src/backend/dormitory_infrastructure/persistence/sql/utility_functions.sql`

SHA-256: `5e15d85019876032d56aace80e57d94cd7edf4605a560e81b9f41ebc2c184218`  
Dòng: 205

```sql
CREATE OR REPLACE FUNCTION public.fn_list_utilities()
RETURNS SETOF utilities LANGUAGE sql STABLE AS $function$
    SELECT * FROM utilities WHERE is_active = true ORDER BY code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_meters(p_room_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    room_id uuid, room_label text, meter_code varchar, serial_number varchar,
    initial_reading numeric, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT m.id, m.utility_id, u.code, u.name, m.room_id,
           b.code || '-' || r.code, m.meter_code, m.serial_number,
           m.initial_reading, m.is_active
    FROM meters m JOIN utilities u ON u.id = m.utility_id
    JOIN rooms r ON r.id = m.room_id JOIN buildings b ON b.id = r.building_id
    WHERE p_room_id IS NULL OR m.room_id = p_room_id
    ORDER BY b.code, r.code, u.code;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_meter(p_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    room_id uuid, room_label text, meter_code varchar, serial_number varchar,
    initial_reading numeric, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_meters(NULL::uuid) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_meter(
    p_id uuid, p_utility_id uuid, p_room_id uuid, p_meter_code text,
    p_serial_number text, p_installed_at date, p_initial_reading numeric, p_note text
) RETURNS text LANGUAGE plpgsql AS $function$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM utilities WHERE id = p_utility_id AND is_active) THEN
        RETURN 'UTILITY_NOT_FOUND';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM rooms WHERE id = p_room_id AND is_active) THEN
        RETURN 'ROOM_NOT_FOUND';
    END IF;
    INSERT INTO meters (id, utility_id, room_id, meter_code, serial_number,
                        installed_at, initial_reading, note, is_active)
    VALUES (p_id, p_utility_id, p_room_id, upper(trim(p_meter_code)),
            nullif(trim(p_serial_number), ''), p_installed_at, p_initial_reading, p_note, true);
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_tariffs(p_utility_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    name varchar, effective_from date, effective_to date,
    calculation_type varchar, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT t.id, t.utility_id, u.code, u.name, t.name, t.effective_from,
           t.effective_to, t.calculation_type, t.is_active
    FROM utility_tariffs t JOIN utilities u ON u.id = t.utility_id
    WHERE p_utility_id IS NULL OR t.utility_id = p_utility_id
    ORDER BY u.code, t.effective_from DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_tariff(p_id uuid)
RETURNS TABLE (
    id uuid, utility_id uuid, utility_code varchar, utility_name varchar,
    name varchar, effective_from date, effective_to date,
    calculation_type varchar, is_active boolean
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_tariffs(NULL::uuid) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_tariff_tiers(p_tariff_id uuid)
RETURNS SETOF tariff_tiers LANGUAGE sql STABLE AS $function$
    SELECT * FROM tariff_tiers WHERE tariff_id = p_tariff_id ORDER BY tier_order;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_tariff(
    p_id uuid, p_utility_id uuid, p_name text, p_effective_from date,
    p_effective_to date, p_calculation_type text, p_created_by uuid, p_tiers jsonb
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE v_tier jsonb;
BEGIN
    PERFORM 1 FROM utilities WHERE id = p_utility_id AND is_active FOR UPDATE;
    IF NOT FOUND THEN RETURN 'UTILITY_NOT_FOUND'; END IF;
    IF EXISTS (
        SELECT 1 FROM utility_tariffs WHERE utility_id = p_utility_id AND is_active
          AND (effective_to IS NULL OR effective_to >= p_effective_from)
          AND (p_effective_to IS NULL OR effective_from <= p_effective_to)
    ) THEN RETURN 'TARIFF_PERIOD_OVERLAP'; END IF;
    INSERT INTO utility_tariffs (id, utility_id, name, effective_from, effective_to,
                                 calculation_type, is_active, created_by)
    VALUES (p_id, p_utility_id, trim(p_name), p_effective_from, p_effective_to,
            p_calculation_type, true, p_created_by);
    FOR v_tier IN SELECT value FROM jsonb_array_elements(p_tiers) LOOP
        INSERT INTO tariff_tiers (id, tariff_id, tier_order, from_quantity,
                                  to_quantity, unit_price)
        VALUES ((v_tier->>'id')::uuid, p_id, (v_tier->>'tier_order')::integer,
                (v_tier->>'from_quantity')::numeric,
                (v_tier->>'to_quantity')::numeric,
                (v_tier->>'unit_price')::numeric);
    END LOOP;
    RETURN 'OK';
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_find_tariff(p_utility_id uuid, p_period_end date)
RETURNS SETOF utility_tariffs LANGUAGE sql STABLE AS $function$
    SELECT * FROM utility_tariffs
    WHERE utility_id = p_utility_id AND is_active
      AND effective_from <= p_period_end
      AND (effective_to IS NULL OR effective_to >= p_period_end)
    ORDER BY effective_from DESC LIMIT 1;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_list_readings(p_meter_id uuid, p_period_start date)
RETURNS TABLE (
    id uuid, meter_id uuid, meter_code varchar, utility_code varchar,
    period_start date, period_end date, previous_reading numeric,
    current_reading numeric, consumption numeric, calculated_amount numeric,
    tariff_id uuid, tariff_snapshot json, recorded_at timestamptz
) LANGUAGE sql STABLE AS $function$
    SELECT mr.id, mr.meter_id, m.meter_code, u.code, mr.period_start,
           mr.period_end, mr.previous_reading, mr.current_reading,
           mr.consumption, mr.calculated_amount, mr.tariff_id,
           mr.tariff_snapshot, mr.recorded_at
    FROM meter_readings mr JOIN meters m ON m.id = mr.meter_id
    JOIN utilities u ON u.id = m.utility_id
    WHERE (p_meter_id IS NULL OR mr.meter_id = p_meter_id)
      AND (p_period_start IS NULL OR mr.period_start = p_period_start)
    ORDER BY mr.recorded_at DESC;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_get_reading(p_id uuid)
RETURNS TABLE (
    id uuid, meter_id uuid, meter_code varchar, utility_code varchar,
    period_start date, period_end date, previous_reading numeric,
    current_reading numeric, consumption numeric, calculated_amount numeric,
    tariff_id uuid, tariff_snapshot json, recorded_at timestamptz
) LANGUAGE sql STABLE AS $function$
    SELECT * FROM public.fn_list_readings(NULL::uuid, NULL::date) WHERE id = p_id;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_reading_context(p_meter_id uuid, p_period_start date,
                                                      p_period_end date)
RETURNS TABLE (
    meter_id uuid, utility_id uuid, initial_reading numeric, is_active boolean,
    duplicate_id uuid, previous_reading numeric
) LANGUAGE plpgsql AS $function$
BEGIN
    PERFORM 1 FROM meters WHERE id = p_meter_id FOR UPDATE;
    RETURN QUERY SELECT m.id, m.utility_id, m.initial_reading, m.is_active,
        (SELECT mr.id FROM meter_readings mr WHERE mr.meter_id = m.id
         AND mr.period_start = p_period_start AND mr.period_end = p_period_end LIMIT 1),
        (SELECT mr.current_reading FROM meter_readings mr WHERE mr.meter_id = m.id
         AND mr.period_end < p_period_start ORDER BY mr.period_end DESC LIMIT 1)
    FROM meters m WHERE m.id = p_meter_id;
END;
$function$;

-- NEXT STATEMENT
CREATE OR REPLACE FUNCTION public.fn_create_reading(
    p_id uuid, p_meter_id uuid, p_period_start date, p_period_end date,
    p_previous numeric, p_current numeric, p_consumption numeric,
    p_tariff_id uuid, p_snapshot json, p_amount numeric, p_recorded_by uuid
) RETURNS text LANGUAGE plpgsql AS $function$
DECLARE v_initial numeric; v_previous numeric; v_utility_id uuid;
BEGIN
    SELECT m.initial_reading, m.utility_id INTO v_initial, v_utility_id
    FROM meters m WHERE m.id = p_meter_id AND m.is_active FOR UPDATE;
    IF NOT FOUND THEN RETURN 'METER_NOT_FOUND'; END IF;
    IF EXISTS (SELECT 1 FROM meter_readings WHERE meter_id = p_meter_id
               AND period_start = p_period_start AND period_end = p_period_end) THEN
        RETURN 'METER_READING_ALREADY_EXISTS';
    END IF;
    SELECT current_reading INTO v_previous FROM meter_readings
    WHERE meter_id = p_meter_id AND period_end < p_period_start
    ORDER BY period_end DESC LIMIT 1;
    IF p_previous <> coalesce(v_previous, v_initial) THEN
        RETURN 'PREVIOUS_READING_MISMATCH';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM utility_tariffs WHERE id = p_tariff_id
                   AND utility_id = v_utility_id AND is_active
                   AND effective_from <= p_period_end
                   AND (effective_to IS NULL OR effective_to >= p_period_end)) THEN
        RETURN 'TARIFF_NOT_FOUND';
    END IF;
    INSERT INTO meter_readings (id, meter_id, period_start, period_end,
        previous_reading, current_reading, consumption, tariff_id,
        tariff_snapshot, calculated_amount, recorded_by)
    VALUES (p_id, p_meter_id, p_period_start, p_period_end,
            p_previous, p_current, p_consumption, p_tariff_id,
            p_snapshot, p_amount, p_recorded_by);
    RETURN 'OK';
END;
$function$;
```

## File: `src/backend/pyproject.toml`

SHA-256: `14f108c8d13a53511f6ea7ef9c5a4fa1634825ecf7a5f0ee793ec3ef73822532`  
Dòng: 41

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "dormitory-management-api"
version = "0.1.0"
description = "Dormitory management modular monolith"
requires-python = ">=3.12"
dependencies = [
  "alembic>=1.16,<2",
  "fastapi>=0.116,<1",
  "psycopg[binary]>=3.2,<4",
  "pydantic-settings>=2.10,<3",
  "pwdlib[argon2]>=0.2,<1",
  "pyjwt>=2.10,<3",
  "sqlalchemy>=2.0,<3",
  "uvicorn>=0.35,<1",
]

[project.optional-dependencies]
dev = [
  "httpx>=0.28,<1",
  "pytest>=8.4,<9",
  "pytest-cov>=6.2,<7",
]

[tool.setuptools.packages.find]
where = ["."]

[tool.setuptools.package-data]
"dormitory_infrastructure.persistence" = ["sql/*.sql"]

[tool.pytest.ini_options]
testpaths = ["../../tests"]
python_files = ["test_*.py"]
addopts = "-q --disable-warnings"

[tool.ruff]
line-length = 100
target-version = "py312"
```

## File: `tests/integration/conftest.py`

SHA-256: `385accd5d0e7d046dbec8b75b612c495751fd5eff631cde8c55f4bce144731e4`  
Dòng: 70

```python
"""API integration tests run against a dedicated PostgreSQL database.

Set TEST_DATABASE_URL to a separate test database. The fixture never touches the
application database and deliberately has no SQLite/ORM fallback.
"""

from collections.abc import Generator
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, make_url

from dormitory_api.main import app
from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.config import get_settings


BACKEND = Path(__file__).resolve().parents[2] / "src" / "backend"


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("API integration tests require a dedicated PostgreSQL TEST_DATABASE_URL")
    if make_url(url).get_backend_name() != "postgresql":
        pytest.skip("API integration tests require PostgreSQL stored functions")
    if make_url(url) == make_url(get_settings().database_url):
        pytest.fail("TEST_DATABASE_URL must not point to the application database")

    config = Config(str(BACKEND / "alembic.ini"))
    config.set_main_option(
        "script_location",
        str(BACKEND / "dormitory_infrastructure" / "persistence" / "migrations"),
    )
    config.attributes["database_url"] = url
    command.upgrade(config, "head")

    engine = create_engine(url, pool_pre_ping=True)
    with engine.begin() as connection:
        tables = connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' "
                 "AND tablename <> 'alembic_version' ORDER BY tablename")
        ).scalars().all()
        if len(tables) != 17:
            pytest.fail(f"Expected 17 application tables in test database; found {len(tables)}")
        # Names come only from PostgreSQL's own catalog, not user input.
        quoted = ", ".join('"' + name.replace('"', '""') + '"' for name in tables)
        connection.exec_driver_sql(f"TRUNCATE TABLE {quoted} RESTART IDENTITY CASCADE")

    with engine.connect() as connection:
        seed_identity(connection)

    def override_get_db() -> Generator[Connection, None, None]:
        with engine.connect() as connection:
            yield connection

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
```

## File: `tests/integration/test_curriculum_alignment.py`

SHA-256: `63b2276a0bb4acb180152eec46defd6ae0c46c5733594252642094c2956b2428`  
Dòng: 137

```python
from uuid import uuid4

from fastapi.testclient import TestClient


def _login(client: TestClient, prefix: str = "/api/v1") -> dict:
    response = client.post(
        f"{prefix}/auth/login",
        json={"email": "admin@dormitory.local", "password": "Admin@123"},
    )
    assert response.status_code == 200, response.text
    return response.json()


def _headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def test_openapi_exposes_v1_and_keeps_legacy_routes_working(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/students" in paths
    assert "/api/auth/login" not in paths
    assert _login(client, "/api")["access_token"]


def test_refresh_token_rotates_and_logout_revokes_it(client: TestClient) -> None:
    login = _login(client)
    old_refresh_token = login["refresh_token"]
    assert login["expires_in"] == 15 * 60

    refreshed = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert refreshed.status_code == 200, refreshed.text
    new_tokens = refreshed.json()
    assert new_tokens["refresh_token"] != old_refresh_token
    assert new_tokens["access_token"] != login["access_token"]

    reused = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert reused.status_code == 401
    assert reused.headers["content-type"].startswith("application/problem+json")
    assert reused.json()["errorCode"] == "AUTH_INVALID_REFRESH_TOKEN"

    logout = client.post(
        "/api/v1/auth/logout",
        headers=_headers(new_tokens["access_token"]),
    )
    assert logout.status_code == 204
    revoked = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": new_tokens["refresh_token"]},
    )
    assert revoked.status_code == 401


def test_register_student_account(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "registered.student@example.com",
            "full_name": "Sinh viên đăng ký",
            "password": "Student@123",
            "student_code": "SV000001",
            "age": 20,
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["role"] == "Student"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "registered.student@example.com", "password": "Student@123"},
    )
    assert login.status_code == 200


def test_student_crud_read_and_pagination(client: TestClient) -> None:
    admin = _login(client)
    headers = _headers(admin["access_token"])
    created = client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "email": "student.page@example.com",
            "full_name": "Sinh viên phân trang",
            "password": "Student@123",
            "student_code": "SV000002",
            "age": 22,
        },
    )
    assert created.status_code == 201, created.text
    student = created.json()
    assert student["age"] == 22

    page = client.get("/api/v1/students?page=1&pageSize=1", headers=headers)
    assert page.status_code == 200, page.text
    assert page.json()["page"] == 1
    assert page.json()["pageSize"] == 1
    assert page.json()["total"] >= 2
    assert len(page.json()["items"]) == 1

    detail = client.get(f"/api/v1/students/{student['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["student_code"] == "SV000002"

    missing = client.get(f"/api/v1/students/{uuid4()}", headers=headers)
    assert missing.status_code == 404
    assert missing.headers["content-type"].startswith("application/problem+json")
    assert missing.json()["status"] == 404


def test_v1_validation_uses_rfc7807_problem_details(client: TestClient) -> None:
    admin = _login(client)
    response = client.post(
        "/api/v1/students",
        headers=_headers(admin["access_token"]),
        json={
            "email": "not-an-email",
            "full_name": "",
            "password": "short",
            "student_code": "123",
            "age": 12,
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["title"] == "Validation Failed"
    assert body["errorCode"] == "VALIDATION_ERROR"
    assert body["instance"] == "/api/v1/students"
    assert body["traceId"]
    assert body["errors"]
```

## File: `tests/integration/test_identity_foundation.py`

SHA-256: `658eae1d04581701244d2b01a5891da9955f3c76998cc15e168d75e92bb76b5c`  
Dòng: 84

```python
from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def test_fixed_roles_user_management_and_profile(client: TestClient) -> None:
    admin = login(client, "admin@dormitory.local", "Admin@123")
    admin_headers = auth_headers(admin["access_token"])
    assert admin["user"]["role"] == "Admin"

    created = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "email": "student2@dormitory.local",
            "full_name": "Sinh viên thứ hai",
            "password": "Student2@123",
            "role": "Student",
        },
    )
    assert created.status_code == 201, created.text
    student_id = created.json()["id"]

    updated = client.put(
        f"/api/users/{student_id}",
        headers=admin_headers,
        json={"full_name": "Sinh viên 02", "role": "Student", "is_active": True},
    )
    assert updated.status_code == 200, updated.text

    student = login(client, "student@dormitory.local", "Student@123")
    profile_headers = auth_headers(student["access_token"])
    profile = client.put(
        "/api/student-profile/me",
        headers=profile_headers,
        json={
            "student_code": "SV-DEMO-001",
            "faculty": "Công nghệ thông tin",
            "cohort": "K2023",
            "phone": "0900000000",
            "address": "Ký túc xá",
            "emergency_contact_name": "Người thân",
            "emergency_contact_phone": "0911111111",
        },
    )
    assert profile.status_code == 200, profile.text
    assert profile.json()["faculty"] == "Công nghệ thông tin"

    forbidden = client.get("/api/users", headers=profile_headers)
    assert forbidden.status_code == 403
    filtered = client.get("/api/users?role=Student", headers=admin_headers)
    assert filtered.status_code == 200, filtered.text
    assert all(item["role"] == "Student" for item in filtered.json())
    assert any(item["id"] == student_id for item in filtered.json())
    assert all("permissions" not in item for item in filtered.json())
    assert client.get("/api/permissions", headers=admin_headers).status_code == 404


def test_deactivated_user_token_is_rejected(client: TestClient) -> None:
    admin_headers = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    student = login(client, "student@dormitory.local", "Student@123")
    users = client.get("/api/users", headers=admin_headers).json()
    item = next(user for user in users if user["email"] == "student@dormitory.local")
    response = client.put(
        f"/api/users/{item['id']}",
        headers=admin_headers,
        json={"full_name": item["full_name"], "role": "Student", "is_active": False},
    )
    assert response.status_code == 200
    assert client.get("/api/auth/me", headers=auth_headers(student["access_token"])).status_code == 401


def test_inventory_delete_deactivates_instead_of_removing(client: TestClient) -> None:
    headers = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    created = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "SAFE", "name": "Tòa lưu lịch sử", "address": "", "floors": 2},
    )
    building_id = created.json()["id"]
    assert client.delete(f"/api/buildings/{building_id}", headers=headers).status_code == 204
    retained = client.get(f"/api/buildings/{building_id}", headers=headers)
    assert retained.status_code == 200
    assert retained.json()["is_active"] is False
```

## File: `tests/integration/test_week1_flow.py`

SHA-256: `bf2c5d2235d5c75df56052967c66d34679fbaf6492d44c8f2e244a148c407251`  
Dòng: 174

```python
from fastapi.testclient import TestClient


def login(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health(client: TestClient) -> None:
    root = client.get("/", follow_redirects=False)
    assert root.status_code == 307
    assert root.headers["location"] == "/docs"

    assert client.get("/docs").status_code == 200
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    bearer = openapi.json()["components"]["securitySchemes"]["HTTPBearer"]
    assert bearer == {"type": "http", "scheme": "bearer"}

    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    readiness = client.get("/readyz")
    assert readiness.status_code == 200
    assert readiness.json() == {"status": "ready", "database": "ok"}


def test_three_seeded_roles_can_login(client: TestClient) -> None:
    accounts = (
        ("admin@dormitory.local", "Admin@123", "Admin"),
        ("staff@dormitory.local", "Staff@123", "Staff"),
        ("student@dormitory.local", "Student@123", "Student"),
    )
    for email, password, expected_role in accounts:
        payload = login(client, email, password)
        assert payload["user"]["role"] == expected_role
        assert payload["access_token"]


def test_student_cannot_access_housing_management(client: TestClient) -> None:
    token = login(client, "student@dormitory.local", "Student@123")["access_token"]
    response = client.get("/api/buildings", headers=auth_headers(token))
    assert response.status_code == 403


def test_week1_admin_creates_inventory_and_views_room_matrix(client: TestClient) -> None:
    token = login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    headers = auth_headers(token)

    building = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "a1", "name": "Khu A", "address": "Cơ sở chính", "floors": 5},
    )
    assert building.status_code == 201, building.text
    building_id = building.json()["id"]
    assert building.json()["code"] == "A1"

    room_type = client.post(
        "/api/room-types",
        headers=headers,
        json={"name": "Phòng 4 sinh viên", "default_monthly_rate": 450000},
    )
    assert room_type.status_code == 201, room_type.text
    room_type_id = room_type.json()["id"]

    room = client.post(
        "/api/rooms",
        headers=headers,
        json={"building_id": building_id, "room_type_id": room_type_id, "code": "101", "floor": 1},
    )
    assert room.status_code == 201, room.text
    room_id = room.json()["id"]

    for bed_code in ("G1", "G2"):
        bed = client.post(
            "/api/beds",
            headers=headers,
            json={"room_id": room_id, "code": bed_code},
        )
        assert bed.status_code == 201, bed.text
        assert bed.json()["status"] == "Available"

    matrix = client.get("/api/room-matrix", headers=headers)
    assert matrix.status_code == 200, matrix.text
    data = matrix.json()
    assert data[0]["code"] == "A1"
    assert data[0]["rooms"][0]["code"] == "101"
    assert [bed["code"] for bed in data[0]["rooms"][0]["beds"]] == ["G1", "G2"]


def test_week1_inventory_update_delete_duplicate_and_logout(client: TestClient) -> None:
    token = login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    headers = auth_headers(token)
    building_payload = {
        "code": "C1",
        "name": "Khu C",
        "address": "Cơ sở phụ",
        "floors": 4,
        "is_active": True,
    }
    building = client.post("/api/buildings", headers=headers, json=building_payload)
    assert building.status_code == 201
    building_id = building.json()["id"]
    duplicate = client.post("/api/buildings", headers=headers, json=building_payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["errorCode"] == "RESOURCE_CONFLICT"

    updated_building = client.put(
        f"/api/buildings/{building_id}",
        headers=headers,
        json={**building_payload, "name": "Khu C mới", "floors": 5},
    )
    assert updated_building.status_code == 200
    assert updated_building.json()["name"] == "Khu C mới"

    room_type = client.post(
        "/api/room-types",
        headers=headers,
        json={"name": "Phòng đôi", "default_monthly_rate": 600000, "is_active": True},
    ).json()
    room_type_id = room_type["id"]
    updated_type = client.put(
        f"/api/room-types/{room_type_id}",
        headers=headers,
        json={"name": "Phòng hai người", "default_monthly_rate": 650000, "is_active": True},
    )
    assert updated_type.status_code == 200

    room = client.post(
        "/api/rooms",
        headers=headers,
        json={
            "building_id": building_id,
            "room_type_id": room_type_id,
            "code": "301",
            "floor": 3,
            "is_active": True,
        },
    ).json()
    room_id = room["id"]
    updated_room = client.put(
        f"/api/rooms/{room_id}",
        headers=headers,
        json={**{key: room[key] for key in ("building_id", "room_type_id", "code", "floor", "is_active")}, "code": "302"},
    )
    assert updated_room.status_code == 200
    assert updated_room.json()["code"] == "302"

    bed = client.post(
        "/api/beds",
        headers=headers,
        json={"room_id": room_id, "code": "G1", "is_active": True},
    ).json()
    bed_id = bed["id"]
    updated_bed = client.put(
        f"/api/beds/{bed_id}",
        headers=headers,
        json={"room_id": room_id, "code": "G1", "is_active": False},
    )
    assert updated_bed.status_code == 200
    assert updated_bed.json()["status"] == "Maintenance"

    assert client.delete(f"/api/beds/{bed_id}", headers=headers).status_code == 204
    assert client.delete(f"/api/rooms/{room_id}", headers=headers).status_code == 204
    assert client.delete(f"/api/room-types/{room_type_id}", headers=headers).status_code == 204
    assert client.delete(f"/api/buildings/{building_id}", headers=headers).status_code == 204
    assert client.post("/api/auth/logout", headers=headers).status_code == 204
```

## File: `tests/integration/test_week2_flow.py`

SHA-256: `f9438d98b4c725028bfc59301bb0fef107512184ab390ad0e95ec1645da8b42e`  
Dòng: 148

```python
from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def create_inventory(client: TestClient, headers: dict[str, str]) -> tuple[str, list[str]]:
    building = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "B1", "name": "Khu B", "address": "Cơ sở chính", "floors": 3},
    ).json()
    room_type = client.post(
        "/api/room-types",
        headers=headers,
        json={"name": "Phòng tiêu chuẩn", "default_monthly_rate": 500000},
    ).json()
    room = client.post(
        "/api/rooms",
        headers=headers,
        json={
            "building_id": building["id"],
            "room_type_id": room_type["id"],
            "code": "201",
            "floor": 2,
        },
    ).json()
    beds = [
        client.post(
            "/api/beds",
            headers=headers,
            json={"room_id": room["id"], "code": code},
        ).json()["id"]
        for code in ("G1", "G2")
    ]
    return room_type["id"], beds


def submit_and_approve(
    client: TestClient,
    student_headers: dict[str, str],
    staff_headers: dict[str, str],
    room_type_id: str,
    term_code: str,
) -> str:
    created = client.post(
        "/api/housing-applications",
        headers=student_headers,
        json={"term_code": term_code, "preferred_room_type_id": room_type_id},
    )
    assert created.status_code == 201, created.text
    application_id = created.json()["id"]
    approved = client.post(
        f"/api/housing-applications/{application_id}/approve",
        headers=staff_headers,
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "Approved"
    return application_id


def test_week2_application_contract_transfer_and_termination(client: TestClient) -> None:
    admin_headers = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    staff_headers = auth_headers(
        login(client, "staff@dormitory.local", "Staff@123")["access_token"]
    )
    student_headers = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    room_type_id, beds = create_inventory(client, admin_headers)

    application_id = submit_and_approve(
        client, student_headers, staff_headers, room_type_id, "HK1-2026"
    )
    assigned = client.post(
        f"/api/contracts/{application_id}/assign-bed",
        headers=staff_headers,
        json={"bed_id": beds[0], "start_date": "2026-09-20", "end_date": "2027-01-31"},
    )
    assert assigned.status_code == 201, assigned.text
    contract = assigned.json()
    contract_id = contract["id"]
    assert contract["status"] == "Active"
    assert contract["current_assignment"]["bed_id"] == beds[0]

    matrix = client.get("/api/room-matrix", headers=staff_headers).json()
    statuses = {bed["id"]: bed["status"] for bed in matrix[0]["rooms"][0]["beds"]}
    assert statuses[beds[0]] == "Occupied"
    assert statuses[beds[1]] == "Available"

    second_application_id = submit_and_approve(
        client, student_headers, staff_headers, room_type_id, "HK2-2026"
    )
    conflict = client.post(
        f"/api/contracts/{second_application_id}/assign-bed",
        headers=staff_headers,
        json={"bed_id": beds[0], "start_date": "2026-10-01", "end_date": "2027-05-31"},
    )
    assert conflict.status_code == 409
    assert conflict.json()["errorCode"] == "BED_ASSIGNMENT_CONFLICT"

    transferred = client.post(
        f"/api/contracts/{contract_id}/transfer",
        headers=staff_headers,
        json={"bed_id": beds[1], "transfer_date": "2026-10-15"},
    )
    assert transferred.status_code == 200, transferred.text
    assert transferred.json()["current_assignment"]["bed_id"] == beds[1]

    history = client.get(
        f"/api/contracts/{contract_id}/assignment-history",
        headers=student_headers,
    )
    assert history.status_code == 200, history.text
    assert [item["status"] for item in history.json()] == ["Ended", "Active"]

    own_contract = client.get("/api/contracts/me", headers=student_headers)
    assert own_contract.status_code == 200
    assert own_contract.json()["id"] == contract_id

    terminated = client.post(
        f"/api/contracts/{contract_id}/terminate",
        headers=staff_headers,
        json={"termination_date": "2026-11-01"},
    )
    assert terminated.status_code == 200, terminated.text
    assert terminated.json()["status"] == "Terminated"
    assert terminated.json()["current_assignment"] is None

    matrix = client.get("/api/room-matrix", headers=staff_headers).json()
    statuses = {bed["id"]: bed["status"] for bed in matrix[0]["rooms"][0]["beds"]}
    assert statuses[beds[0]] == "Available"
    assert statuses[beds[1]] == "Available"


def test_only_student_can_submit_application(client: TestClient) -> None:
    admin_headers = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    room_type_id, _ = create_inventory(client, admin_headers)
    response = client.post(
        "/api/housing-applications",
        headers=admin_headers,
        json={"term_code": "HK1-2026", "preferred_room_type_id": room_type_id},
    )
    assert response.status_code == 403
    assert response.json()["detail"]["errorCode"] == "STUDENT_ONLY"
```

## File: `tests/integration/test_week3_flow.py`

SHA-256: `49e09f0c49cc4f5868d7f24e5eb0ee636098e084974a7c30a15f35b40ad91b6c`  
Dòng: 174

```python
from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def _create_contract(client: TestClient, admin: dict[str, str], student: dict[str, str]) -> tuple[str, str]:
    building = client.post(
        "/api/v1/buildings",
        headers=admin,
        json={"code": "U1", "name": "Khu tiện ích", "floors": 3},
    ).json()
    room_type = client.post(
        "/api/v1/room-types",
        headers=admin,
        json={"name": "Phòng tuần 3", "default_monthly_rate": 500000},
    ).json()
    room = client.post(
        "/api/v1/rooms",
        headers=admin,
        json={
            "building_id": building["id"],
            "room_type_id": room_type["id"],
            "code": "301",
            "floor": 3,
        },
    ).json()
    bed = client.post(
        "/api/v1/beds",
        headers=admin,
        json={"room_id": room["id"], "code": "G1"},
    ).json()
    application = client.post(
        "/api/v1/housing-applications",
        headers=student,
        json={"term_code": "HK1-2026-W3", "preferred_room_type_id": room_type["id"]},
    ).json()
    client.post(
        f"/api/v1/housing-applications/{application['id']}/approve", headers=admin
    ).raise_for_status()
    contract = client.post(
        f"/api/v1/contracts/{application['id']}/assign-bed",
        headers=admin,
        json={
            "bed_id": bed["id"],
            "start_date": "2026-09-01",
            "end_date": "2027-01-31",
        },
    )
    assert contract.status_code == 201, contract.text
    return room["id"], contract.json()["id"]


def _create_tariff(
    client: TestClient,
    headers: dict[str, str],
    utility_id: str,
    name: str,
    calculation_type: str,
    tiers: list[dict],
) -> None:
    response = client.post(
        "/api/v1/utility-tariffs",
        headers=headers,
        json={
            "utility_id": utility_id,
            "name": name,
            "effective_from": "2026-09-01",
            "calculation_type": calculation_type,
            "tiers": tiers,
        },
    )
    assert response.status_code == 201, response.text


def test_week3_manual_readings_and_idempotent_bill(client: TestClient) -> None:
    admin = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    student = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    room_id, contract_id = _create_contract(client, admin, student)

    utilities_response = client.get("/api/v1/utilities", headers=admin)
    assert utilities_response.status_code == 200, utilities_response.text
    utilities = {item["code"]: item for item in utilities_response.json()}
    assert set(utilities) == {"ELECTRICITY", "WATER"}

    _create_tariff(
        client,
        admin,
        utilities["ELECTRICITY"]["id"],
        "Điện hai bậc",
        "Tiered",
        [
            {"tier_order": 1, "from_quantity": 0, "to_quantity": 50, "unit_price": 1000},
            {"tier_order": 2, "from_quantity": 50, "to_quantity": None, "unit_price": 2000},
        ],
    )
    _create_tariff(
        client,
        admin,
        utilities["WATER"]["id"],
        "Nước đồng giá",
        "Flat",
        [{"tier_order": 1, "from_quantity": 0, "to_quantity": None, "unit_price": 15000}],
    )

    meters: dict[str, dict] = {}
    for code, utility_code in (("DIEN-U301", "ELECTRICITY"), ("NUOC-U301", "WATER")):
        response = client.post(
            "/api/v1/meters",
            headers=admin,
            json={
                "utility_id": utilities[utility_code]["id"],
                "room_id": room_id,
                "meter_code": code,
                "initial_reading": 0,
            },
        )
        assert response.status_code == 201, response.text
        meters[utility_code] = response.json()

    for utility_code, current in (("ELECTRICITY", 80), ("WATER", 10)):
        response = client.post(
            "/api/v1/meter-readings",
            headers=admin,
            json={
                "meter_id": meters[utility_code]["id"],
                "period_start": "2026-09-01",
                "period_end": "2026-09-30",
                "previous_reading": 0,
                "current_reading": current,
            },
        )
        assert response.status_code == 201, response.text
        assert response.json()["tariff_snapshot"]["tiers"]

    invalid = client.post(
        "/api/v1/meter-readings",
        headers=admin,
        json={
            "meter_id": meters["WATER"]["id"],
            "period_start": "2026-10-01",
            "period_end": "2026-10-31",
            "previous_reading": 10,
            "current_reading": 9,
        },
    )
    assert invalid.status_code == 400
    assert invalid.json()["errorCode"] == "VALIDATION_ERROR"

    bill_payload = {
        "contract_id": contract_id,
        "period_start": "2026-09-01",
        "period_end": "2026-09-30",
        "issued_date": "2026-10-01",
        "due_date": "2026-10-10",
        "idempotency_key": "week3-contract-september-2026",
    }
    bill = client.post("/api/v1/bills/generate", headers=admin, json=bill_payload)
    assert bill.status_code == 201, bill.text
    assert bill.json()["total_amount"] == "760000.00"
    assert {item["item_type"] for item in bill.json()["items"]} == {
        "Housing",
        "Electricity",
        "Water",
    }
    repeated = client.post("/api/v1/bills/generate", headers=admin, json=bill_payload)
    assert repeated.status_code == 201
    assert repeated.json()["id"] == bill.json()["id"]

    assert client.get("/api/v1/meter-readings/template", headers=admin).status_code == 404
    readings = client.get("/api/v1/meter-readings", headers=admin)
    assert readings.status_code == 200
    assert len(readings.json()) == 2
```

## File: `tests/unit/test_billing_calculator.py`

SHA-256: `f4aa9f2571bfe991f89742d8a08e3837783f4319e00550cb1cd8375e9f033d98`  
Dòng: 44

```python
from decimal import Decimal

import pytest

from dormitory_domain.billing import TariffTier, calculate_utility_charge


def test_tiered_tariff_calculates_each_band_and_rounds_money() -> None:
    result = calculate_utility_charge(
        Decimal("80"),
        [
            TariffTier(1, Decimal("0"), Decimal("50"), Decimal("1000")),
            TariffTier(2, Decimal("50"), None, Decimal("2000")),
        ],
    )

    assert result.consumption == Decimal("80.000")
    assert result.total_amount == Decimal("110000.00")
    assert [item.billed_quantity for item in result.breakdown] == [
        Decimal("50.000"),
        Decimal("30.000"),
    ]


def test_flat_tariff_and_zero_consumption() -> None:
    tiers = [TariffTier(1, Decimal("0"), None, Decimal("15321.75"))]

    assert calculate_utility_charge(Decimal("10"), tiers, "Flat").total_amount == Decimal(
        "153217.50"
    )
    assert calculate_utility_charge(Decimal("0"), tiers, "Flat").total_amount == Decimal(
        "0.00"
    )


def test_tariff_rejects_gap_between_tiers() -> None:
    with pytest.raises(ValueError, match="liên tục"):
        calculate_utility_charge(
            Decimal("80"),
            [
                TariffTier(1, Decimal("0"), Decimal("50"), Decimal("1000")),
                TariffTier(2, Decimal("60"), None, Decimal("2000")),
            ],
        )
```

## File: `tests/unit/test_housing_entities.py`

SHA-256: `c95435b90dcbf9ff59f0e87bec6fb22a46ac225af028f1f011394e730a01231d`  
Dòng: 32

```python
from decimal import Decimal
from uuid import uuid4

import pytest

from dormitory_domain.common import BedStatus
from dormitory_domain.housing import Bed, Building, RoomType


def test_building_normalizes_code() -> None:
    building = Building(code=" a1 ", name="Khu A", address="", floors=5)
    assert building.code == "A1"


def test_building_requires_positive_floor_count() -> None:
    with pytest.raises(ValueError):
        Building(code="A", name="Khu A", address="", floors=0)


def test_room_type_rejects_negative_rate() -> None:
    with pytest.raises(ValueError):
        RoomType(name="Phòng 4", default_monthly_rate=Decimal("-1"))


def test_bed_status_is_derived() -> None:
    available = Bed(room_id=uuid4(), code="G1")
    occupied = Bed(room_id=uuid4(), code="G2", is_occupied=True)
    maintenance = Bed(room_id=uuid4(), code="G3", is_active=False, is_occupied=True)

    assert available.status is BedStatus.AVAILABLE
    assert occupied.status is BedStatus.OCCUPIED
    assert maintenance.status is BedStatus.MAINTENANCE
```

## File: `tests/unit/test_stored_repository_boundary.py`

SHA-256: `e222000351614b132c579f62c7c8ff94896aae6be2fb24f0db7cff38422aab36`  
Dòng: 30

```python
"""Guard the runtime persistence boundary: repositories call stored functions only."""

import ast
from pathlib import Path
import re

import dormitory_infrastructure


PERSISTENCE_ROOT = Path(dormitory_infrastructure.__file__).parent / "persistence"
DIRECT_DML = re.compile(r"\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\b", re.IGNORECASE)
SELECT = re.compile(r"\bSELECT\b", re.IGNORECASE)
STORED_CALL = re.compile(r"\bpublic\.fn_[a-z_]+\s*\(", re.IGNORECASE)


def test_repositories_only_call_postgres_functions() -> None:
    # Scan Python runtime code, not migration/SQL definitions: those must access tables.
    sources = sorted((PERSISTENCE_ROOT / "repositories").glob("*.py"))
    assert sources
    for source in sources:
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            sql = node.value
            assert not DIRECT_DML.search(sql), f"Direct table write in {source.name}:{node.lineno}"
            if SELECT.search(sql):
                assert STORED_CALL.search(sql), (
                    f"SELECT must call a stored function in {source.name}:{node.lineno}"
                )
```
