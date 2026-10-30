# API MVP ký túc xá

Base URL qua gateway: `http://localhost:8081/api/v1`.

## Xác thực

Đăng nhập bằng `POST /auth/login`:

```json
{"email":"staff@dormitory.local","password":"Staff@123"}
```

Phản hồi chứa `access_token`. Các request được bảo vệ dùng header:

```text
Authorization: Bearer <access_token>
```

Hệ thống chỉ hỗ trợ đăng ký, đăng nhập, refresh token và xem phiên hiện tại. Logout và reset password đã bị loại khỏi phạm vi.

## Luồng demo

1. `POST /buildings` tạo tòa bằng tài khoản Admin.
2. `POST /rooms` tạo phòng bằng Admin hoặc Staff. Request gồm `building_id`, `code`, `floor`, `capacity`, `monthly_rate`. Hệ thống tự tạo vị trí ở và hai công tơ điện/nước.
3. Student gọi `POST /housing-applications` với `term_code` và `room_id`.
4. Admin/Staff gọi `POST /housing-applications/{id}/approve`, sau đó `POST /contracts/{id}/assign-room`.
5. Admin/Staff tạo biểu giá qua `POST /utility-tariffs`, rồi ghi hai chỉ số cùng kỳ qua `POST /meter-readings`.
6. `POST /bills/generate` tạo đúng một hóa đơn phòng/kỳ:

```json
{
  "room_id": "<uuid>",
  "period_start": "2026-10-01",
  "period_end": "2026-10-31",
  "issued_date": "2026-11-01",
  "due_date": "2026-11-15",
  "idempotency_key": "room-201-202610"
}
```

7. `POST /bills/{bill_id}/confirm-payment` xác nhận thanh toán đủ:

```json
{"method":"Cash","reference":"PAY-001"}
```

## Mã lỗi nghiệp vụ chính

API v1 trả lỗi theo `application/problem+json`, gồm `status`, `detail`, `errorCode`, `traceId` và `instance`.

| Mã | HTTP | Ý nghĩa |
|---|---:|---|
| `AUTH_INVALID_CREDENTIALS` | 401 | Email hoặc mật khẩu không đúng |
| `STUDENT_ONLY` | 403 | Chỉ Student được gửi đăng ký |
| `OWN_DATA_ONLY` | 403 | Student truy cập dữ liệu ngoài phạm vi của mình |
| `APPLICATION_ALREADY_EXISTS` | 409 | Đã có đơn cùng kỳ đang chờ hoặc được duyệt |
| `APPLICATION_NOT_APPROVED` | 409 | Chưa thể lập hợp đồng vì đơn chưa duyệt |
| `ROOM_FULL` | 409 | Phòng không còn vị trí trống |
| `METER_READING_ALREADY_EXISTS` | 409 | Công tơ đã có chỉ số trong kỳ |
| `PREVIOUS_READING_MISMATCH` | 422 | Chỉ số đầu kỳ không khớp kỳ trước |
| `READINGS_INCOMPLETE` | 422 | Chưa đủ chỉ số điện và nước cùng kỳ |
| `BILL_PERIOD_ALREADY_EXISTS` | 409 | Phòng đã có hóa đơn trong kỳ |
| `IDEMPOTENCY_KEY_REUSED` | 409 | Khóa idempotency được dùng cho dữ liệu khác |
| `BILL_NOT_PAYABLE` | 409 | Hóa đơn đã trả hoặc không còn ở trạng thái có thể trả |

## Chạy kiểm thử

```powershell
$env:TEST_DATABASE_URL='postgresql+psycopg://dormitory:changeme@localhost:5432/dormitory_test'
Set-Location src/backend
..\..\.venv\Scripts\python.exe -m pytest -q ..\..\tests
```

Database kiểm thử phải tách biệt với database ứng dụng. Fixture tự chạy migration, seed ba tài khoản và dọn dữ liệu giữa các test.
