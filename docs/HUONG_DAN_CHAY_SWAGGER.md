# Hướng dẫn chạy backend và thao tác trên Swagger

## 1. Chạy bằng Docker

Yêu cầu: Docker Desktop đang chạy.

Tại thư mục gốc dự án:

```powershell
docker compose up --build
```

Lệnh trên sẽ tự động:

1. khởi động PostgreSQL;
2. chờ PostgreSQL healthy;
3. chạy `alembic upgrade head`;
4. seed tài khoản demo;
5. chạy FastAPI tại cổng `8000`.

Mở trình duyệt:

- Trang thao tác chính: <http://localhost:8000/> — tự chuyển đến Swagger.
- Swagger UI: <http://localhost:8000/docs>.
- OpenAPI JSON: <http://localhost:8000/openapi.json>.
- Liveness: <http://localhost:8000/healthz>.
- Readiness PostgreSQL: <http://localhost:8000/readyz>.
- Adminer: <http://localhost:8080>.

## 2. Tài khoản demo

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@dormitory.local` | `Admin@123` |
| Staff | `staff@dormitory.local` | `Staff@123` |
| Student | `student@dormitory.local` | `Student@123` |

Các tài khoản này chỉ dùng cho môi trường development/demo.

## 3. Đăng nhập và Authorize trên Swagger

1. Mở nhóm **Auth**.
2. Chọn `POST /api/v1/auth/login`.
3. Bấm **Try it out**.
4. Nhập JSON, ví dụ:

```json
{
  "email": "admin@dormitory.local",
  "password": "Admin@123"
}
```

5. Bấm **Execute**.
6. Sao chép giá trị `access_token` từ response.
7. Bấm **Authorize** ở đầu trang Swagger.
8. Dán token vào ô Bearer và xác nhận.
9. Gọi các endpoint có biểu tượng ổ khóa.

Muốn thử phân quyền, đăng nhập lại bằng Staff hoặc Student rồi thay token trong **Authorize**.

## 4. Luồng demo đang hoạt động

### Quản lý phòng

1. Admin đăng nhập.
2. Tạo building bằng `POST /api/buildings`.
3. Tạo room type bằng `POST /api/room-types`.
4. Tạo room bằng `POST /api/rooms`.
5. Tạo bed bằng `POST /api/beds`.
6. Xem sơ đồ bằng `GET /api/room-matrix`.

### Đơn đăng ký và hợp đồng

1. Student gọi `POST /api/housing-applications`.
2. Staff/Admin gọi API approve application.
3. Staff/Admin gọi API assign bed để tạo contract.
4. Xem contract và assignment history.
5. Thử transfer hoặc terminate contract.

## 5. Dừng hệ thống

```powershell
docker compose down
```

Lệnh trên giữ dữ liệu PostgreSQL trong volume `pgdata`.

Nếu muốn tạo lại database demo từ đầu, cần chủ động xóa volume; thao tác này sẽ xóa dữ liệu hiện có nên không thực hiện mặc định.

## 6. Chạy test backend

Từ thư mục `src/backend`:

```powershell
..\..\.venv\Scripts\python.exe -m pytest
```

Baseline hiện tại: `14 passed`.
