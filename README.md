# Quản lý ký túc xá — MVP đơn giản

Dự án backend FastAPI, PostgreSQL và Docker Compose. Thao tác qua Swagger tại http://localhost:8000/docs. Có đúng ba loại tài khoản: **Admin**, **Staff** và **Student**.

## Luồng chính

1. Admin thêm tòa. Admin hoặc Staff thêm phòng, nhập sức chứa và giá ở tham khảo. Hệ thống tự tạo chỗ ở nội bộ và hai công tơ điện, nước cho phòng.
2. Student xem phòng, gửi đăng ký chọn một phòng.
3. Staff hoặc Admin duyệt/từ chối. Sau khi duyệt, cán bộ lập hợp đồng cho sinh viên ở **phòng đã chọn**; hệ thống tự kiểm tra còn chỗ.
4. Staff hoặc Admin nhập chỉ số điện, nước theo phòng và kỳ; tiền điện nước được tính theo biểu giá.
5. Staff hoặc Admin phát hành **một hóa đơn điện nước cho mỗi phòng trong mỗi kỳ**. Hóa đơn có hai dòng điện và nước, không nhân theo số người và không cộng tiền phòng. Sinh viên ở phòng trong kỳ đều xem được cùng hóa đơn.
6. Khi phòng thanh toán đủ, Staff hoặc Admin xác nhận một lần, lưu phương thức, mã tham chiếu và thời điểm. MVP chưa kết nối cổng thanh toán và chưa quản lý phần đóng góp của từng cá nhân.

Hợp đồng thuộc từng sinh viên và cố định một phòng. Không có sơ đồ phòng, lịch sử chuyển giường/phòng, chuyển phòng, AI, vi phạm hay biên lai trong luồng MVP. Cơ sở dữ liệu vẫn dùng vị trí ở nội bộ để kiểm soát sức chứa và giữ tương thích dữ liệu cũ; người dùng chỉ thao tác với phòng.

## Chạy

```bash
docker compose up -d --build
docker compose ps
```

Gateway/API docs: http://localhost:8081/docs · API readiness: http://localhost:8081/readyz · Gateway health: http://localhost:8081/gateway/healthz · Adminer: http://localhost:8080.

Gateway Nginx chuyển tiếp request đến API, giữ `Authorization` và `X-Request-ID`, nén phản hồi JSON, giới hạn request body 2 MB và áp dụng rate limit riêng cho đăng nhập/đăng ký. Các container API và gateway đều có healthcheck trong Docker Compose.

Tài khoản demo (chỉ dùng cho môi trường phát triển):

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@dormitory.local` | `Admin@123` |
| Staff | `staff@dormitory.local` | `Staff@123` |
| Student | `student@dormitory.local` | `Student@123` |

Đăng nhập bằng `POST /api/v1/auth/login`, dùng access token dạng Bearer cho các API yêu cầu xác thực.

## API theo trình tự demo

| Bước | Endpoint |
|---|---|
| Tòa, phòng | `GET/POST /api/v1/buildings`, `GET/POST /api/v1/rooms` |
| Đăng ký | `POST/GET /api/v1/housing-applications` |
| Duyệt | `POST /api/v1/housing-applications/{application_id}/approve` |
| Hợp đồng | `POST /api/v1/contracts/{application_id}/assign-room`, `GET /api/v1/contracts/me` |
| Điện nước | `GET /api/v1/meters`, `POST /api/v1/utility-tariffs`, `POST /api/v1/meter-readings` |
| Hóa đơn phòng | `POST /api/v1/bills/generate`, `GET /api/v1/bills`, `GET /api/v1/bills/{bill_id}` |
| Thanh toán | `POST /api/v1/bills/{bill_id}/confirm-payment` |

`POST /api/v1/bills/generate` nhận `room_id`, `period_start`, `period_end`, `issued_date`, `due_date` và `idempotency_key`. Phải có cả chỉ số điện và nước cho đúng kỳ trước khi phát hành. API chặn hóa đơn trùng phòng/kỳ.

## Kỹ thuật và kiểm thử

Mã backend ở `src/backend/dormitory_*`. Alembic quản lý migration; repository gọi PostgreSQL stored functions. Chạy `alembic upgrade head` và `python -m dormitory_infrastructure.identity.seed_cli` khi chạy ngoài Compose.

Smoke test luồng hai sinh viên chung một hóa đơn dùng database thử riêng: `scripts/smoke_simple_flow.py`. Import `postman/Dormitory_MasterPlan_8Tuan.postman_collection.json` để mở collection **Dormitory MVP - Master Plan 8 tuần**. Có đủ Tuần 1–8; mỗi request tự lấy token, tạo dữ liệu phụ thuộc và có thể bấm Send độc lập. Hướng dẫn: [postman/README.md](postman/README.md).

Các ví dụ request/response và mã lỗi chính nằm trong `docs/API_MVP.md`.
