# PHÂN TÍCH BÀI TOÁN — BACKEND QUẢN LÝ KÝ TÚC XÁ

Phạm vi chính thức chỉ gồm backend API. Swagger UI và Postman được dùng để thao
tác, kiểm thử và demo. Dự án không triển khai frontend và không hỗ trợ import
chỉ số điện/nước bằng Excel.

## 1. Mục tiêu

- Xây dựng REST API bằng Python 3.12 và FastAPI.
- Lưu dữ liệu trong PostgreSQL 16.
- Dùng SQL có tham số qua SQLAlchemy Core; không dùng ORM.
- Quản lý schema bằng Alembic và giữ phạm vi 17 bảng.
- Xác thực JWT với ba role cố định `Admin`, `Staff`, `Student`.
- Kiểm thử bằng pytest, Swagger UI và Postman.

## 2. Phạm vi chức năng

### Xác thực và tài khoản

- Đăng ký, đăng nhập, refresh token, đăng xuất và xem phiên hiện tại.
- Admin quản lý tài khoản.
- Student cập nhật và xem hồ sơ của chính mình.

### Cơ sở vật chất

- F01–F04: CRUD tòa nhà, loại phòng, phòng và giường.

### Đăng ký và hợp đồng

- F06–F07: Student gửi đơn; Admin/Staff duyệt hoặc từ chối.
- F08: phân giường và tạo hợp đồng trong một transaction.
- F09: xem hợp đồng theo quyền sở hữu.
- F11: chấm dứt hợp đồng và giải phóng giường.

### Điện, nước và hóa đơn

- F12: quản lý công tơ và biểu giá hiệu lực theo thời gian.
- F13: nhập thủ công chỉ số bằng JSON API.
- F15: tính tiền đồng giá hoặc nhiều bậc và lưu snapshot biểu giá.
- F16: sinh hóa đơn tiền phòng, điện, nước với idempotency.

F14 import Excel không thuộc dự án. Không có template, upload, preview, confirm,
file storage hoặc import batch.

## 3. Business rule bắt buộc

1. Chỉ phân giường cho đơn đã duyệt.
2. Không cho hai assignment chồng thời gian trên cùng giường.
4. `current_reading` không được nhỏ hơn `previous_reading`.
5. Không có hai chỉ số của cùng công tơ trong cùng kỳ.
6. Hóa đơn không được sinh trùng theo hợp đồng/kỳ hoặc idempotency key.
7. Student chỉ được truy cập dữ liệu thuộc chính mình.

## 4. Phạm vi đã triển khai

- Docker Compose, PostgreSQL, migration, seed và health/readiness.
- OpenAPI tại `/docs`, API chính tại `/api/v1`.

Thu phí, vi phạm, báo cáo và AI là các giai đoạn tiếp theo; không được mô tả là
đã hoàn thành nếu chưa có controller, service, repository và test tương ứng.

## 5. Tiêu chí nghiệm thu hiện tại

- [ ] `docker compose up -d --build` khởi động API và PostgreSQL.
- [ ] `/healthz`, `/readyz` và `/docs` hoạt động.
- [ ] Đăng nhập được ba role demo và RBAC đúng.
- [ ] Luồng đơn → duyệt → phân giường → chấm dứt hoạt động đúng.
- [ ] Nhập chỉ số thủ công chặn dữ liệu giảm hoặc trùng kỳ.
- [ ] Tính tiền đúng tại biên bậc giá.
- [ ] Sinh hóa đơn lặp không tạo bản ghi trùng.
- [ ] pytest pass cho phạm vi đã triển khai.

Kế hoạch 8 tuần đã điều chỉnh nằm tại
[`05-ke-hoach-backend-only.md`](05-ke-hoach-backend-only.md).
