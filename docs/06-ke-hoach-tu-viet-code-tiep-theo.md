---
title: Kế hoạch tự viết tiếp backend ký túc xá
document_type: implementation-plan
status: planning-only
updated: 2026-10-05
source_of_truth: Master_Plan_MVP_8Tuan.xlsx
implementation_owner: Người học tự viết code
scope: Backend FastAPI + PostgreSQL
---

# Kế hoạch tự viết code phần tiếp theo

## 1. Cách dùng tài liệu này

Đây là **đặc tả công việc, không phải mã nguồn**. Có thể đưa từng mục `TASK-*` cho
công cụ web để hỏi cách làm, giải thích luồng dữ liệu, kiểm tra thiết kế hoặc xem
lại code **do mình tự viết**. Đừng yêu cầu công cụ sinh trọn module rồi chép vào;
hãy làm từng bước nhỏ và chạy test sau mỗi bước.

Khi đưa một task cho công cụ web, gửi kèm: mã task, cấu trúc thư mục ở mục 3,
quy ước ở mục 4, phần API/dữ liệu/test của task và code hiện tại có liên quan.
Hỏi công cụ nêu thứ tự thực hiện, rủi ro và trường hợp kiểm thử; chỉ xin ví dụ
ngắn khi thật sự không hiểu một kỹ thuật.

## 2. Phạm vi và trạng thái hiện tại

- Chỉ làm backend API. Không làm frontend, import Excel, gateway, dashboard hay
  báo cáo thống kê.
- API gốc là `/api/v1`. Swagger ở `/docs`. PostgreSQL quản lý schema bằng Alembic.
- Auth, người dùng/sinh viên, tòa/phòng/giường, đơn/hợp đồng, công tơ/biểu giá/
  chỉ số và **danh sách/sinh hóa đơn** đã có router, service hoặc repository.
  Không viết lại các phần này khi chưa kiểm tra hành vi hiện tại.
- Chưa có router thanh toán, biên lai, vi phạm, AI. API chi tiết hóa đơn
  `GET /bills/{id}` cũng chưa có dù repository có hàm đọc hóa đơn.
- Migration `20260929_0020` đã bỏ bảng `payments`, `violation_types`, `violations`.
  Schema đang chốt 17 bảng. Kế hoạch trong Master Plan tuần 5–6 muốn thêm các
  chức năng này, nên **phải chấp nhận tăng số bảng bằng migration mới**. Nếu bài
  học bắt buộc giữ đúng 17 bảng, cần sửa lại phạm vi Master Plan trước khi code;
  không giả vờ các chức năng đó đã có dữ liệu.
- Migration cũ của `payments` tham chiếu `stored_files`, bảng cũng đã bị bỏ.
  Không sao chép nguyên migration cũ để tạo lại bảng thanh toán.
- Bộ test hiện có: `tests/unit` và `tests/integration`. Integration test cần
  `TEST_DATABASE_URL` trỏ tới database PostgreSQL **riêng**, không dùng database
  thật hoặc database demo.

## 3. Bản đồ thư mục cần dùng

| Thành phần | Nơi đặt | Vai trò |
|---|---|---|
| HTTP router | `src/backend/dormitory_api/controllers/` | Nhận request, lấy user, gọi service, trả status/response |
| Schema và nghiệp vụ | `src/backend/dormitory_application/<module>/` | Validation, luồng xử lý, kiểu request/response |
| Quy tắc thuần | `src/backend/dormitory_domain/<module>/` | Phép tính và quy tắc không phụ thuộc database |
| Repository | `src/backend/dormitory_infrastructure/persistence/repositories/` | Chỉ gọi stored function với tham số bind |
| SQL function | `src/backend/dormitory_infrastructure/persistence/sql/` | Đọc/ghi bảng, khóa giao dịch, kiểm tra bất biến |
| Migration | `src/backend/dormitory_infrastructure/persistence/migrations/versions/` | Thay đổi schema và cài/cập nhật function |
| Test | `tests/unit/`, `tests/integration/` | Kiểm thử quy tắc và luồng API với PostgreSQL test |

Không tạo lại thư mục bọc `Dormitory.Api/Dormitory.Infrastructure/...`. Không
truy vấn trực tiếp bảng nghiệp vụ từ controller/service/repository. SQL đọc/ghi
bảng nằm trong stored function; Python gọi `public.fn_*` có bind tham số.

## 4. Quy ước cho mọi task

1. Trước khi sửa, tìm route/service/repository/SQL function liên quan và chạy
   test hiện có để có mốc so sánh.
2. Làm theo chiều phụ thuộc: migration → stored function → repository → service
   và schema → router → test → hướng dẫn dùng API. Một task nhỏ có thể chỉ chạm
   vài lớp; không tạo file rỗng cho đủ lớp.
3. Kiểm tra role ở API **và** quyền truy cập đối tượng ở nghiệp vụ hoặc SQL.
   Student chỉ xem dữ liệu của chính mình; Staff/Admin theo quyền được chỉ định.
4. Mọi tiền tệ dùng `NUMERIC/Decimal`, không dùng số thực nhị phân; mọi thao tác
   thay đổi số dư hoặc trạng thái quan trọng chạy trong một transaction.
5. Trả lỗi có HTTP status và `errorCode` nhất quán. Không trả lỗi SQL thô hoặc
   khóa/API key cho client.
6. Migration mới chỉ tiến lên từ head hiện tại; không sửa migration đã chạy.
   Trước migration thay đổi dữ liệu, sao lưu database không phải demo.
7. Kết thúc một task khi test trường hợp thành công, thất bại và phân quyền đều
   đạt; cập nhật README/Swagger nếu API đổi.

## 5. Thứ tự thực hiện

### TASK-01 — Khép kín API hóa đơn hiện có (ưu tiên trước tuần 5)

**Mục tiêu:** Đọc được chi tiết một hóa đơn và các dòng tính tiền trước khi ghi
nhận thanh toán. Không thay đổi thuật toán sinh hóa đơn nếu không có lỗi cụ thể.

- API dự kiến: `GET /api/v1/bills/{bill_id}`.
- Dữ liệu trả về: mã hóa đơn, sinh viên, hợp đồng, kỳ, hạn trả, trạng thái, tổng,
  đã trả, còn nợ và danh sách dòng phí kèm snapshot cách tính.
- Quyền: Student chỉ đọc hóa đơn của mình; Staff/Admin được đọc theo phạm vi
  được giao. Hóa đơn không tồn tại hoặc không thuộc quyền phải có phản hồi rõ.
- Kiểm thử: đọc thành công; ID sai; Student A không đọc được hóa đơn Student B;
  tổng các dòng phí khớp tổng hóa đơn; sinh lặp cùng kỳ không tạo bản ghi trùng.
- Hoàn thành khi route, service, repository/stored function liên quan và test
  thống nhất cùng một dữ liệu trả về.

### TASK-02 — Thiết kế lại dữ liệu thanh toán và biên lai (tuần 5)

**Phụ thuộc:** TASK-01 và xác nhận được phép tăng số bảng.

- Tạo migration **mới** cho bảng `payments`. Biên lai có thể là các cột và
  snapshot trên payment như thiết kế cũ; chưa cần bảng `receipts` riêng.
- Các trường tối thiểu: `id`, `bill_id`, `payment_no`, `amount`, `method`,
  `status`, `paid_at`, `transaction_reference`, người ghi nhận, `receipt_no`,
  `receipt_issued_at`, `receipt_snapshot`. Chốt enum/status trước khi viết SQL.
- Ràng buộc: số tiền > 0; mã thanh toán và mã biên lai duy nhất; mã giao dịch
  ngoài không trùng; không phát biên lai cho payment chưa xác nhận.
- Không dùng `proof_file_id` tham chiếu `stored_files` vì bảng đó không còn.
  Nếu thật sự cần chứng từ, phải đặc tả lưu trữ riêng và xin quyết định trước.
- Kiểm thử migration trên database test rỗng và database test đã ở head;
  kiểm tra ràng buộc unique/FK/check.
- Hoàn thành khi migration chạy được từ head hiện tại và có mô tả schema mới.

### TASK-03 — Ghi nhận thanh toán và cập nhật công nợ (tuần 5)

**Phụ thuộc:** TASK-02.

- API dự kiến: `POST /api/v1/payments`, `GET /api/v1/bills/{bill_id}/payments`,
  `GET /api/v1/receipts/{payment_id}`. Chỉ Staff/Admin ghi nhận hoặc xác nhận
  thanh toán; Student chỉ đọc khoản thanh toán/biên lai của mình.
- Stored function ghi payment và cập nhật `bills.paid_amount`,
  `balance_amount`, `status` **trong cùng transaction**. Khóa hóa đơn khi xử lý
  đồng thời để hai request không cùng tiêu hết số dư.
- Quy tắc: cho phép trả nhiều lần; không cho trả quá số dư; request trùng
  `transaction_reference` không thu tiền lần hai; xác nhận rồi mới có biên lai;
  tổng các payment đã xác nhận bằng `paid_amount` của hóa đơn.
- Thống nhất status tối thiểu: chưa trả, trả một phần, đã trả; định nghĩa rõ
  cách xử lý payment bị từ chối/hủy để không cộng vào công nợ.
- Kiểm thử: trả một phần rồi trả đủ; trả quá; số tiền ≤ 0; request trùng;
  hai request đồng thời; Student khác chủ hóa đơn bị từ chối; biên lai duy nhất.
- Hoàn thành khi có thể demo hóa đơn → hai lần thanh toán → số dư 0 → biên lai.

### TASK-04 — Dữ liệu và API vi phạm (tuần 6)

**Phụ thuộc:** TASK-03, vì khoản phạt sẽ vào hóa đơn.

- Tạo migration mới cho `violation_types` và `violations`. Tái dùng ý tưởng
  trường từ migration cũ `20260921_0007`, nhưng kiểm tra lại FK với schema hiện
  tại; không tạo lại bảng bảo trì hoặc file minh chứng ngoài phạm vi.
- API dự kiến: danh sách loại vi phạm, ghi nhận vi phạm, xác nhận/từ chối,
  danh sách/lịch sử vi phạm của sinh viên. Chốt tên route trong cùng module.
- Dữ liệu tối thiểu: loại vi phạm, sinh viên, hợp đồng nếu có, thời điểm,
  mô tả, mức độ, số tiền phạt, trạng thái, người ghi/duyệt và thời điểm duyệt.
- Quy tắc: Staff/Admin ghi và duyệt; Student chỉ xem của mình; không phạt vi
  phạm chưa xác nhận; không cộng cùng một vi phạm vào hai dòng hóa đơn.
- Stored function xử lý chuyển trạng thái và nối khoản phạt vào `bill_items`
  một cách idempotent. Quy định rõ kỳ hóa đơn nhận tiền phạt; nếu kỳ đã phát
  hành thì nêu cách xử lý trước khi code, không âm thầm sửa hóa đơn đã chốt.
- Kiểm thử: xác nhận/từ chối; quyền sở hữu; số tiền âm; xác nhận lặp; sinh hóa
  đơn có đúng một dòng phạt; vi phạm chưa xác nhận không được thu.
- Hoàn thành khi demo vi phạm → xác nhận → hóa đơn có một khoản phạt đúng kỳ.

### TASK-05 — AI Assistant có kiểm soát (tuần 7)

**Phụ thuộc:** TASK-03 và TASK-04 để có dữ liệu nhắc nợ, vi phạm.

- API dự kiến: `POST /api/v1/ai/draft-payment-reminder` và
  `POST /api/v1/ai/summarize-violations` cho Staff/Admin.
- Tách interface gọi LLM khỏi service nghiệp vụ; khóa API, model và timeout ở
  biến môi trường. Không gửi mật khẩu, token hay dữ liệu người khác cho provider.
- Đầu ra là **bản nháp AI**, không tự gửi thông báo, không tự sửa hóa đơn hoặc
  trạng thái vi phạm. Người dùng phải xem lại trước khi sử dụng.
- Khi provider lỗi/timeout, trả lỗi có kiểm soát; các API hợp đồng, điện nước,
  hóa đơn và thanh toán vẫn hoạt động.
- Kiểm thử bằng fake client: prompt chỉ chứa dữ liệu được phép, đầu ra có nhãn
  bản nháp, timeout/lỗi không làm hỏng nghiệp vụ chính. Không bắt test tự động
  gọi API LLM thật.
- Hoàn thành khi có demo hai bản nháp và test lỗi provider đạt.

### TASK-06 — Hoàn thiện kiểm thử API và bàn giao (tuần 7–8)

- Lập request Postman cho từng API đã triển khai, theo đúng tuần ở sheet
  `API Checklist (Postman)` của Master Plan. Test status, schema, `errorCode`,
  token thiếu/hết hạn và quyền Student/Staff/Admin.
- Chạy integration test với `TEST_DATABASE_URL` riêng, migration từ đầu và dữ
  liệu test có kiểm soát. Không chạy test xóa dữ liệu trên database thật/demo.
- Chạy Newman/CI khi collection ổn định; ghi lại test nào đạt, bỏ qua hoặc chưa
  có API. Không ghi “đã hoàn thành” cho tính năng mới chỉ có kế hoạch.
- Kiểm tra Docker build, migration, `/healthz`, `/readyz`, `/docs`, biến môi
  trường và smoke test trên staging. Chưa cần gateway.
- Cập nhật README: cách cài, migrate, seed tối thiểu, chạy API, chạy test và
  các API thực sự đã có. Demo cuối kỳ bằng Swagger/Postman, không cần frontend.
- Hoàn thành khi một người khác làm theo README có thể dựng backend và chạy
  luồng đăng ký → hợp đồng → điện nước → hóa đơn → thanh toán → vi phạm → AI.

## 6. Theo dõi tiến độ

| Task | Trạng thái ban đầu | Phụ thuộc | Bằng chứng khi hoàn thành |
|---|---|---|---|
| TASK-01 | Chưa làm | API hóa đơn hiện có | Route chi tiết + test quyền và dòng phí |
| TASK-02 | Chưa làm | Quyết định mở rộng 17 bảng | Migration mới + test schema |
| TASK-03 | Chưa làm | TASK-02 | API thanh toán/biên lai + test transaction |
| TASK-04 | Chưa làm | TASK-03 | API vi phạm + test khoản phạt |
| TASK-05 | Chưa làm | TASK-03, TASK-04 | API AI + test fake provider |
| TASK-06 | Chưa làm | Các task trước | Postman/Newman, staging, README, demo |

Chỉ đổi trạng thái sau khi có bằng chứng test/demonstration tương ứng. Nếu phát
hiện quy tắc nghiệp vụ chưa rõ (nhất là thanh toán chuyển khoản và khoản phạt
vào kỳ đã chốt), ghi câu hỏi và chốt quyết định trước khi tự viết code.
