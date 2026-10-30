# Postman theo Master Plan 8 tuần

Collection chính: **Dormitory MVP - Master Plan 8 tuần** — 75 request, đủ 8 tuần và 32 công việc của sheet `Plan`.

## Dùng ngay: mở request rồi Send

1. Bật Docker Desktop. Tại thư mục gốc dự án chạy:

   ```powershell
   docker compose up -d --build
   ```

2. Mở <http://localhost:8081/readyz>. Kết quả phải có `"status": "ready"`.
3. Trong Postman chọn **Import → Files**, chọn **Dormitory_MasterPlan_8Tuan.postman_collection.json** ở thư mục này. Nếu đã import bản cũ, cập nhật/thay thế collection cũ để tránh mở nhầm.
4. Chọn **No Environment**. Mở collection → **Tuần 1**, **Tuần 2**, …, **Tuần 8**.
5. Bấm một request để mở tab (bấm đúp để giữ tab), rồi **Send**. URL, JSON body và Bearer Token đã cấu hình. Xem **Test Results** để biết test đạt hay lỗi.

Không cần nhập `access_token`, ID tòa/phòng/đơn/hợp đồng/hóa đơn hay tự đăng nhập trước. Mở thẳng request ở tuần 4, 5, 6 hoặc 8 vẫn chạy được. Script ở cấp collection tự tạo điều kiện cần thiết trước khi gửi request chính, dùng `pm.sendRequest` theo [tài liệu Postman](https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-reference/pm-send-request/).

**Nếu đang dùng Local View / Native Git:** mở chính thư mục dự án trong Postman. Bản YAML nằm ở `postman/collections/Dormitory MVP - Master Plan 8 tuần/`, có sẵn thư mục từng tuần. Không cần chỉnh `.postman/resources.yaml`: cấu hình hiện tại tự nhận các collection trong `postman/`. Các collection cũ và `New Collection` được giữ nguyên; chọn đúng tên bản mới.

## Cách bộ test hoạt động

- Mỗi **Send** tạo một kịch bản độc lập với mã và ID mới. Các request không dùng lại dữ liệu của request vừa bấm trước đó. Ví dụ “Duyệt đơn” tự tạo một đơn Pending; “Xác nhận trả đủ” tự tạo hóa đơn Issued trước khi xác nhận.
- Request mô tả chức năng chính; các request chuẩn bị nằm trong **Postman Console**. Lần Send có nhiều bước chuẩn bị sẽ lâu hơn một request HTTP đơn.
- Admin/Staff dùng tài khoản demo đã seed. Token tự lấy lại khi gần hết hạn; sinh viên mẫu được đăng ký mới cho từng kịch bản. `student_code` luôn đúng 8 ký tự.
- Mỗi request sử dụng `{{access_token}}` của đúng vai trò. Token và ID của kịch bản vừa chạy được lưu ở **Variables** của collection.
- Kỳ điện nước demo là **một ngày hiện tại**. Dùng biểu giá đang hiệu lực; nếu chưa có thì tạo biểu giá cho ngày đó. Request “Thiết lập biểu giá” dùng một ngày trống trước biểu giá sớm nhất để tránh xung đột và không sửa biểu giá cũ.
- Các request có nhãn **[400]/[401]/[403]/[409]/[422]** cố ý nhận lỗi. **Test Results xanh** khi mã HTTP và `errorCode` đúng dự kiến. Có thể chạy chung các ca này bằng Runner.
- Mỗi Send có thể thêm dữ liệu demo, hợp đồng, chỉ số và hóa đơn vào database đang chạy. Các bước thanh toán/chấm dứt chỉ tác động dữ liệu mẫu mới của chính request đó.

## Chạy tự động

Chọn **Run collection**, chọn toàn bộ request hoặc một tuần, đặt **Iterations = 1**, **Delay = 250–300 ms**. Không cần chạy tuần trước. Nếu cần giữ các biến sau lượt chạy, bật **Keep variable values / Persist variables** khi phiên bản Postman có tùy chọn này.

Chạy bằng Newman từ thư mục gốc:

```powershell
npx --yes --package newman@6 newman run postman/Dormitory_MasterPlan_8Tuan.postman_collection.json --timeout-script 60000 --delay-request 250
```

Newman chạy bản JSON v2.1. Bản YAML dành cho Local View của Postman.

## Cấu hình

Sửa **Variables** của collection nếu cần:

| Biến | Mặc định / ý nghĩa |
|---|---|
| `baseUrl` | `http://localhost:8081`, không thêm `/api/v1` |
| `adminEmail` / `adminPassword` | `admin@dormitory.local` / `Admin@123` |
| `staffEmail` / `staffPassword` | `staff@dormitory.local` / `Staff@123` |
| `studentPassword` | `Student@123`, mật khẩu sinh viên mẫu |
| `access_token` / `refresh_token` | Tự sinh; không điền token tĩnh |
| `roomId`, `applicationId`, `contractId`, `billId` | Tự sinh theo kịch bản vừa Send |

Collection chủ động dùng cấu hình của chính nó để tránh các biến trùng tên trong environment cũ ghi đè token và ID. Khi đổi tài khoản hoặc base URL, token cache tự được bỏ qua.

## Đối chiếu kế hoạch

Xem [bảng đủ 32 công việc](MASTER_PLAN_COVERAGE.md). Mỗi request có mô tả ô nguồn Excel, vai trò, endpoint, HTTP/errorCode dự kiến và code kiểm thử.

- Tuần 1: hạ tầng, tài khoản, hồ sơ, phân quyền, tòa/phòng/công tơ.
- Tuần 2: gửi/theo dõi/duyệt/từ chối đơn, lập/xem/chấm dứt hợp đồng.
- Tuần 3: tiện ích, biểu giá, nhập chỉ số, lỗi giảm/trùng, snapshot giá.
- Tuần 4: thiếu chỉ số, hóa đơn chung phòng, idempotency và trùng kỳ.
- Tuần 5: thanh toán đủ, thông tin xác nhận, chặn trả lặp, đối chiếu tổng.
- Tuần 6: hai sinh viên một hóa đơn; phòng đầy, đơn chưa duyệt, trùng hợp đồng; quyền và lỗi nghiệp vụ.
- Tuần 7: Swagger/OpenAPI đúng phạm vi, ví dụ lỗi và luồng E2E một Send.
- Tuần 8: gateway/readiness/Swagger và demo đầu cuối hai sinh viên.

Checklist Excel còn `/auth/logout`, nhưng backend hiện tại đã bỏ endpoint này. Bộ test bám sheet Plan và API đang có, gồm cả `/auth/refresh`. Các công việc build Docker, viết tài liệu và lưu người xác nhận nội bộ không có endpoint riêng để thực hiện/xác minh toàn bộ qua Postman; phạm vi kiểm tra tương ứng ghi trong bảng đối chiếu.

## Khi gặp lỗi

- **ECONNREFUSED:** bật Docker Desktop, chạy Compose và kiểm tra `docker compose ps`.
- **502 sau khi rebuild API:** gateway có thể giữ IP container cũ. Chạy `docker compose restart gateway`, sau đó thử lại `/readyz`.
- **Setup prerequisites / Setup completed thất bại:** mở Console đọc bước chuẩn bị lỗi; request chính sẽ bị chặn để tránh dùng ID cũ. Kiểm tra tài khoản seed, URL và database.
- **401 với tài khoản đã đổi mật khẩu:** sửa biến tài khoản trong collection. Xóa `_auth_admin` / `_auth_staff` nếu cần ép đăng nhập lại.
- **Postman web không gọi được localhost:** dùng ứng dụng Postman Desktop hoặc Desktop Agent.
- **Đổi tên request thủ công:** tên đang dùng để chọn kịch bản; nên sửa ở generator rồi sinh lại.

## Bảo trì

```powershell
.venv/Scripts/python.exe scripts/generate_masterplan_postman.py
```

Generator đọc workbook, tạo lại JSON, YAML Local View và bảng đối chiếu. Không sửa Excel. Logic chuẩn bị nằm ở `scripts/postman/masterplan_prerequest.js`. Bản import được giao với token rỗng; sau khi tự chạy, không commit/chia sẻ các giá trị token hoặc cache còn hiệu lực.

`Dormitory_MVP.postman_collection.json`, `Dormitory_QuickRun.postman_collection.json` và các collection YAML cũ là bản trước đây, được giữ lại; dùng collection chính ở trên cho kế hoạch 8 tuần.

