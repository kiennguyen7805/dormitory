# KẾ HOẠCH BACKEND-ONLY TỪ MASTER PLAN 8 TUẦN

Tài liệu này tóm tắt `Master_Plan_MVP_8Tuan.xlsx` đã được cập nhật trực tiếp.
Mỗi tuần có 5 ngày công, làm và kiểm thử chức năng trong cùng tuần.

## Nguyên tắc điều chỉnh

- Chỉ phát triển FastAPI, PostgreSQL, migration, seed, test và tài liệu API.
- Demo bằng Swagger UI hoặc Postman.
- Chỉ số điện/nước chỉ nhập thủ công qua JSON API.
- Không có frontend, import Excel, gateway hoặc dashboard.
- Kiểm thử được gắn với từng chức năng thay vì dồn thành một tuần riêng.

## Kế hoạch 8 tuần

| Tuần | Mục tiêu backend | Kết quả cần có |
|---|---|---|
| 1 | Nền tảng, auth, tòa/phòng/giường | Test đăng nhập, CRUD và trạng thái giường; demo room matrix |
| 2 | Đăng ký, duyệt, hợp đồng, phân/chuyển giường | Test trạng thái, giường trùng và luồng đơn đến hợp đồng |
| 3 | Công tơ, biểu giá, chỉ số thủ công | Test kỳ hiệu lực, bậc giá và chỉ số sai |
| 4 | Phát hành và tra cứu hóa đơn | Test tổng tiền, quyền xem và sinh lặp cùng kỳ |
| 5 | Thanh toán, công nợ, biên lai | Test số dư, giao dịch trùng và thanh toán nhiều lần |
| 6 | Vi phạm và khoản phạt | Test trạng thái, quyền xem và phạt sau xác nhận |
| 7 | AI Assistant và bộ kiểm thử API | Test lỗi provider, hoàn thiện Postman/Newman |
| 8 | Triển khai và bàn giao backend | Migration, staging, smoke test, README và demo cuối kỳ |

## Các hạng mục đã loại

| Hạng mục trong workbook gốc | Xử lý |
|---|---|
| Khung React, layout, routing, login page | Loại |
| Các màn hình đăng ký, hợp đồng, điện nước, hóa đơn, vi phạm | Loại; thao tác qua Swagger/Postman |
| Recharts và tuần hoàn thiện UI/UX | Loại; thay bằng kiểm thử và hardening backend |
| F14 template/preview/confirm Excel | Loại hoàn toàn |
| ClosedXML/openpyxl cho nghiệp vụ import | Không thêm dependency |
| Docker frontend + Nginx và service Web | Loại; chỉ PostgreSQL + API, Adminer tùy chọn |

## Checklist nghiệm thu backend

- [ ] `docker compose up -d --build` khởi động thành công.
- [ ] `/healthz`, `/readyz` và `/docs` trả thành công.
- [ ] Đăng nhập được ba role demo.
- [ ] Student không truy cập được dữ liệu của sinh viên khác.
- [ ] Luồng đơn → duyệt → phân giường → chuyển/chấm dứt giữ đúng lịch sử.
- [ ] Double-booking bị chặn trong transaction.
- [ ] Chỉ số điện/nước chỉ được nhập thủ công và chặn chuỗi chỉ số sai.
- [ ] Tính tiền theo bậc đúng ở các biên.
- [ ] Sinh hóa đơn lặp cùng idempotency key không tạo bản ghi trùng.
- [ ] Không có route hoặc dependency import Excel.
- [ ] pytest và Postman/Newman pass cho phạm vi đã triển khai.
