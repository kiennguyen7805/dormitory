# Kế hoạch hoàn thiện dự án theo Giáo trình Bài 1–Bài 5

Ngày rà soát: 27/09/2026

## 1. Mục tiêu

- Giữ kiến trúc Python 3.12, FastAPI và PostgreSQL; dùng SQLAlchemy Core để thực thi SQL, không dùng ORM.
- Ánh xạ đầy đủ các khái niệm trong giáo trình ASP.NET Core sang công nghệ tương đương.
- Dùng Swagger tại `/docs` làm giao diện chạy và kiểm thử API.
- Giữ tương thích `/api/...`, đồng thời công khai hợp đồng mới tại `/api/v1/...`.
- Phạm vi hiện hành là 17 bảng; ba role cố định, không import Excel.

## 2. P0 — Bắt buộc để bám Bài 1–Bài 5

### P0.1. API versioning

Trạng thái: **Đã hoàn thành**.

- API chính: `/api/v1`.
- `/api` cũ vẫn hoạt động nhưng bị ẩn khỏi OpenAPI.
- Swagger mô tả phiên bản `1.0.0`.
- Kiểm thử thủ công trên Postman với URL gốc `http://localhost:8000/api/v1`.

Tiêu chí nghiệm thu:

- `/openapi.json` có `/api/v1/auth/login` và `/api/v1/students`.
- `/api/auth/login` vẫn gọi được nhưng không xuất hiện trong OpenAPI.

### P0.2. Student API theo bài thực hành Bài 2

Trạng thái: **Đã hoàn thành**.

Endpoint:

```http
GET  /api/v1/students?page=1&pageSize=10
GET  /api/v1/students/{id}
POST /api/v1/students
```

Validation:

- `student_code`: đúng 8 ký tự và không chứa khoảng trắng.
- `full_name`: bắt buộc.
- `age`: từ 18 đến 60.
- `email`: đúng định dạng cơ bản.
- `password`: từ 8 đến 128 ký tự.

Phân quyền:

- Xem danh sách/chi tiết: `students.read`.
- Tạo sinh viên: `students.manage`.

### P0.3. Access Token và Refresh Token

Trạng thái: **Đã hoàn thành**.

Endpoint:

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

Quy tắc:

- Access Token mặc định sống 15 phút.
- Refresh Token mặc định sống 7 ngày.
- Chỉ lưu SHA-256 hash của Refresh Token trong database.
- Mỗi lần refresh sẽ rotation token; token cũ không dùng lại được.
- JWT có `sub`, `email`, `role`, `jti`, `iss`, `aud`, `iat`, `exp`.

Migration: `20260927_0010_refresh_tokens.py`.

### P0.4. Problem Details RFC 7807

Trạng thái: **Đã hoàn thành cho API v1**.

API v1 trả `application/problem+json` với các trường:

```json
{
  "type": "https://dormitory.local/problems/validation-error",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Dữ liệu đầu vào không hợp lệ.",
  "instance": "/api/v1/students",
  "errorCode": "VALIDATION_ERROR",
  "traceId": "..."
}
```

Đã bao phủ validation, HTTP exception, lỗi nghiệp vụ và lỗi 500 không xác định. API `/api` cũ giữ response lỗi cũ để bảo đảm tương thích ngược.

## 3. P1 — Cần làm tiếp để hoàn thành Bài 1 và Bài 5

### P1.1. API Key middleware

Trạng thái: **Chưa làm**.

- Header `X-API-KEY`.
- Thiếu key trả 401; sai key trả 403.
- Chỉ áp dụng cho `/api/v1/integrations/*` hoặc endpoint public cần service-to-service.
- Không chặn `/docs`, `/openapi.json`, `/healthz`, `/readyz` và `/api/v1/auth/*`.

### P1.2. Structured logging và request timing

Trạng thái: **Chưa làm**.

- Log JSON ra stdout.
- Ghi method, path, status code, duration, user ID và trace ID.
- Trả `X-Request-ID` trong response.
- Không ghi password, access token hoặc refresh token vào log.

### P1.3. Response compression

Trạng thái: **Chưa làm**.

- Thêm `GZipMiddleware`.
- Kiểm thử `Content-Encoding: gzip` với response đủ lớn.

### P1.4. Rate limiting

Trạng thái: **Chưa làm**.

- `/api/v1/auth/login`: 5 request/phút/IP.
- API thông thường: 100 request/phút/IP.
- Request vượt hạn mức trả 429 theo Problem Details.

### P1.5. Redis cache và invalidation

Trạng thái: **Chưa làm**.

- Thêm Redis vào Docker Compose.
- Cache `/api/v1/room-matrix` hoặc `/api/v1/reports/occupancy` trong 15 phút.
- Xóa cache khi phân giường, chuyển giường, chấm dứt hợp đồng hoặc thay đổi phòng/giường.
- `/readyz` kiểm tra cả PostgreSQL và Redis.

## 4. P2 — Minh chứng nâng cao

### P2.1. PostgreSQL function/stored procedure

Trạng thái: **Tùy yêu cầu giảng viên**.

Nếu cần minh chứng tương đương Stored Procedure của Bài 3, tạo function:

```sql
fn_get_contracts_by_student(student_id uuid)
```

Repository gọi function bằng tham số hóa. Không cần chuyển toàn bộ dự án sang Dapper.

### P2.2. Hoàn thiện OpenAPI

- Thêm `summary`, `description` và `responses` cho toàn bộ endpoint.
- Thêm ví dụ request/response thành công và thất bại.
- Chia tag Auth, Students, Housing, Contracts, Utilities, Billing và Violations.

### P2.3. Hoàn thiện các module nghiệp vụ

- Utilities: **Đã hoàn thành phạm vi tuần 3** gồm catalog điện/nước, công tơ,
  biểu giá theo thời gian, bậc giá và ghi chỉ số thủ công. Không có import Excel.
- Billing: **Đã hoàn thành phạm vi tuần 3** gồm bộ tính tiền độc lập, snapshot biểu giá,
  hóa đơn tiền phòng + điện + nước và idempotency. Payments tiếp tục ở tuần sau.
- Violations.
- Maintenance.
- Notifications.
- Files và Reports.

Các bảng đã tồn tại nhưng cần đủ controller, service, repository và test để trở thành dịch vụ sử dụng được.

## 5. Kiểm thử và cách chạy

Chạy test:

```powershell
cd src/backend
..\..\.venv\Scripts\python.exe -m pytest
```

Kết quả cần duy trì sau khi bổ sung tuần 3:

```text
pytest: toàn bộ test pass; có unit test BillingCalculator và integration test luồng tuần 3
```

Chạy hệ thống sau khi Docker Desktop đã hoạt động:

```powershell
docker compose up -d --build
docker compose exec api alembic upgrade head
```

Địa chỉ kiểm thử:

- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Health: `http://localhost:8000/healthz`
- Readiness: `http://localhost:8000/readyz`

## 6. Điều kiện hoàn thành toàn bộ Bài 1–Bài 5

- [x] REST endpoint, JSON, status code và Swagger.
- [x] Dependency Injection và Repository Pattern.
- [x] Validation DTO và Student API có phân trang.
- [x] Có thể nhập request thủ công trong Postman hoặc dùng Swagger UI.
- [x] SQL có tham số và transaction commit/rollback, không dùng ORM.
- [x] JWT, role/permission, register và refresh.
- [x] CORS.
- [x] Global error contract theo RFC 7807 cho API v1.
- [x] API versioning `/api/v1`.
- [x] Health và PostgreSQL readiness.
- [ ] API Key middleware.
- [ ] Structured logging và request timing.
- [ ] Response compression.
- [ ] Rate limiting.
- [ ] Redis cache, invalidation và Redis readiness.
- [ ] PostgreSQL function nếu giảng viên yêu cầu Stored Procedure.
