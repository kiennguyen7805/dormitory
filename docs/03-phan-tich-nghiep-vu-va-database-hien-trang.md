# Phân tích nghiệp vụ, bài toán và database — hiện trạng backend

> Phạm vi: backend/API và PostgreSQL của dự án ký túc xá. Tài liệu này mô tả cả nghiệp vụ cần có lẫn phần đã triển khai.

## 1. Bài toán cần giải quyết

Hệ thống quản lý toàn bộ vòng đời ở ký túc xá: sinh viên đăng ký, cán bộ duyệt, phân giường, lập hợp đồng, ghi điện/nước, phát hành hóa đơn, thu tiền, chuyển chỗ và chấm dứt hợp đồng. Mục tiêu không chỉ là CRUD từng bảng mà là giữ cho các bước nhất quán với nhau và có thể tra soát lịch sử.

Chuỗi nghiệp vụ chính:

```text
Tài khoản sinh viên
  → Đăng ký ở → Duyệt/từ chối
  → Phân giường + tạo hợp đồng
  → Ghi chỉ số điện/nước → Tính phí → Phát hành hóa đơn
  → Thanh toán/công nợ
  → Chuyển giường hoặc chấm dứt hợp đồng
```

Các bất biến quan trọng:

- Một giường không được cấp cho hai hợp đồng trong cùng khoảng thời gian.
- Một đơn đăng ký chỉ tạo tối đa một hợp đồng; chỉ đơn đã duyệt mới được phân giường.
- Việc chuyển giường phải giữ lịch sử giường cũ và giường mới trong một transaction.
- Giá và cách tính tiền đã phát hành phải được lưu thành snapshot; sửa biểu giá sau đó không được làm đổi hóa đơn cũ.
- Một hợp đồng không được có hai hóa đơn chưa hủy cho cùng kỳ.
- Tiền đã lập hóa đơn, tiền đã thu và tiền còn nợ là ba đại lượng khác nhau.
- Sinh viên chỉ được đọc dữ liệu thuộc về mình; thao tác quản trị phải kiểm tra vai trò/quyền.

## 2. Vai trò và phạm vi

| Vai trò | Nghiệp vụ chính |
|---|---|
| Admin | Quản lý tài khoản, danh mục tòa/phòng/giường, biểu giá, các nghiệp vụ cán bộ |
| Staff | Duyệt đăng ký, phân/chuyển giường, ghi chỉ số, lập hóa đơn |
| Student | Cập nhật hồ sơ, gửi đăng ký, xem hợp đồng và dữ liệu của mình |


## 3. Mô hình dữ liệu hiện có

Nguồn đối chiếu lịch sử: các migration Alembic. Từ phương án 17 bảng, runtime không còn ORM model; xem migration `20260929_0020` và các repository SQL để biết trạng thái hiện hành.

| Cụm dữ liệu | Bảng quan trọng | Ý nghĩa và quan hệ |
|---|---|---|
| Danh tính | `roles`, `users`, `student_profiles` | User thuộc một trong ba role cố định; hồ sơ sinh viên gắn 1–1 với user |
| Cơ sở vật chất | `buildings`, `rooms`, `beds` | Tòa có nhiều phòng; phòng có sức chứa và đơn giá riêng; phòng có nhiều giường |
| Đăng ký/chỗ ở | `housing_applications`, `contracts`, `bed_assignments` | Đơn đã duyệt sinh hợp đồng; hợp đồng có nhiều giai đoạn phân giường |
| Điện nước | `utilities`, `meters`, `utility_tariffs`, `tariff_tiers`, `meter_readings` | Công tơ theo phòng; biểu giá có hiệu lực theo thời gian; chỉ số lưu snapshot tính phí |
| Tài chính | `bills`, `bill_items` | Hóa đơn gồm nhiều dòng; chưa có bảng thu tiền trong schema hiện hành |

Các quan hệ đáng chú ý:

```text
buildings 1─n rooms 1─n beds
users(Student) 1─n housing_applications 1─0..1 contracts
contracts 1─n bed_assignments n─1 beds
rooms 1─n meters 1─n meter_readings
utility_tariffs 1─n tariff_tiers
contracts 1─n bills 1─n bill_items
```

ID phần lớn dùng UUID; tiền dùng `numeric`; thời gian lưu bằng `date` hoặc timestamp. Các ràng buộc đã có gồm mã phòng duy nhất trong tòa, mã giường duy nhất trong phòng, kỳ chỉ số duy nhất theo công tơ, một phân giường `Active` cho mỗi hợp đồng, và một hóa đơn chưa `Void` cho mỗi hợp đồng/kỳ. Chi tiết nằm trong migration `20260921_0004`, `0005`, `0006` và `0009`.

## 4. Luồng nghiệp vụ và các quyết định dữ liệu

### 4.1. Đăng ký → hợp đồng → giường

Sinh viên tạo đơn ở trạng thái `Submitted`. Cán bộ duyệt thành `Approved` hoặc từ chối kèm lý do. Chỉ đơn `Approved` mới được tạo hợp đồng và phân giường. Khi phân/chuyển giường, stored function khóa hàng giường và kiểm tra khoảng thời gian trước khi ghi để tránh hai request đồng thời cùng nhận một giường. Lịch sử nằm ở `bed_assignments`, không ghi đè trực tiếp giường hiện tại trên `contracts`.

Trạng thái `Occupied` là dữ liệu suy ra từ phân giường, không phải cột được phép chỉnh tay trên `beds`. Cần chốt rõ quy ước khoảng ngày: nên dùng `[start_date, end_date)` (ngày kết thúc không còn ở giường cũ), hoặc một quy ước khác được áp dụng thống nhất cho kiểm tra trùng, lịch sử, tính phí và room matrix.

### 4.2. Điện nước → hóa đơn

Công tơ gắn với **phòng**, còn hóa đơn gắn với **hợp đồng/sinh viên**. Đây là điểm cần một quy tắc phân bổ rõ ràng. Một chỉ số công tơ của phòng nhiều người không thể được tính nguyên khoản tiền cho từng sinh viên. Các phương án nghiệp vụ khả thi: chia đều theo số người ở trong kỳ, chia theo số ngày thực ở, hoặc thu theo phòng/đại diện. Quy tắc được chọn phải được lưu cùng snapshot để tra soát và xử lý người vào/ra giữa kỳ.

`meter_readings` lưu chỉ số đầu/cuối, lượng tiêu thụ, biểu giá và `tariff_snapshot`. `bills` lưu tổng tiền; `bill_items` lưu khoản phòng/điện/nước và chi tiết tính. Hóa đơn đã phát hành không nên tính lại từ biểu giá hiện tại.

### 4.3. Thanh toán và công nợ

Schema hiện hành không có bảng `payments` và chưa có API thanh toán. Nếu triển khai sau này, cần migration mới, quy tắc cho nhiều khoản thu trên một hóa đơn, chặn tổng thu vượt số còn nợ và cập nhật công nợ trong cùng transaction. Hủy hoặc từ chối một khoản thanh toán phải đảo tác động lên công nợ một cách có kiểm soát, không xóa lịch sử.

## 5. Đánh giá hiện trạng và khoảng trống

| Mức ưu tiên | Phát hiện | Tác động / việc cần chốt |
|---|---|---|
| Rất cao | `billing_repositories.py` lấy **toàn bộ tiền công tơ phòng** khi tạo hóa đơn cho từng hợp đồng | Phòng nhiều người có nguy cơ bị thu lặp điện/nước. Chốt quy tắc chia và kiểm thử trường hợp nhiều hợp đồng cùng phòng trước khi dùng dữ liệu thật |
| Cao | Chuyển giường đặt `end_date` giường cũ bằng `start_date` giường mới, trong khi kiểm tra chồng lấp dùng biên ngày bao gồm | Chuẩn hóa quy ước khoảng ngày trên stored function, room matrix và hóa đơn |
| Cao | `fn_list_beds`/`fn_room_matrix` suy `Occupied` từ assignment `Active` nhưng chưa xét ngày hiện tại; chưa tính phòng `Maintenance/Inactive` | Phân biệt đang ở hôm nay với phân giường tương lai; trạng thái phòng phải chi phối khả dụng của giường |
| Cao | Chống trùng giường nằm ở đường ghi qua stored function, chưa có exclusion constraint bao phủ ghi trực tiếp | Chỉ cấp API quyền `EXECUTE` cần thiết, hạn chế ghi bảng trực tiếp; cân nhắc ràng buộc khoảng thời gian ở PostgreSQL |
| Cao | Tài liệu yêu cầu phí phòng theo ngày, phạt đã xác nhận và thanh toán nhiều lần, nhưng API hóa đơn hiện mới tính `base_rate` cùng điện/nước | Xác định chính sách prorate, tiền phạt và hoàn/điều chỉnh trước khi mở rộng billing |
| Trung bình | `housing_applications` có ngày dự kiến/ghi chú trong schema nhưng request tạo đơn hiện chỉ nhận kỳ và loại phòng | Quyết định có bổ sung input hay lược bỏ phần schema chưa dùng |
| Trung bình | Giá của `rooms.monthly_rate` được chốt vào `contracts.base_rate` lúc phân phòng | Cần quy tắc khi chuyển phòng: giữ giá cũ, đổi giá hợp đồng, hay tạo dòng điều chỉnh |
| Trung bình | Tài liệu kế hoạch gốc có nhiều chức năng chưa có API | Dùng tài liệu backend-only hiện hành để không nhầm “thiết kế” với “đã triển khai” |

## 6. Kiến trúc truy vấn PostgreSQL

Đường đi mục tiêu:

```text
HTTP API → kiểm tra quyền/input → repository → SELECT public.fn_...(:tham_so)
                                      ↓
                              PostgreSQL function
                                      ↓
                              bảng, index, transaction
```

SQL cho tài khoản, xác thực, sinh viên, cơ sở vật chất và hợp đồng hiện nằm trong `src/backend/dormitory_infrastructure/persistence/sql/`, được cài bằng các migration `20260928_0011`–`0019`. API điện nước và hóa đơn gọi stored function qua repository. Integration test cần PostgreSQL test database riêng; không có nhánh SQLite ORM.

Có thể thay `CREATE OR REPLACE FUNCTION` trong PostgreSQL để tối ưu mà không sửa API **nếu** giữ nguyên chữ ký, kiểu kết quả, mã lỗi và ý nghĩa nghiệp vụ. Mọi thay đổi đã thử trực tiếp trong database phải được ghi lại vào file SQL và migration mới; nếu không, các môi trường sẽ chạy các phiên bản logic khác nhau. Đừng coi stored function là lớp phân quyền tự động: API vẫn phải kiểm tra quyền/ownership, còn tài khoản database nên được cấp quyền tối thiểu.

## 7. Thứ tự xử lý đề xuất

1. Chốt quy tắc chia điện/nước, ngày ở/ngày chuyển và cách tính phí phòng giữa kỳ bằng ví dụ số cụ thể.
2. Viết test cho phòng nhiều sinh viên, chuyển giường đúng ngày ranh giới, hai request phân cùng giường và phát hành trùng kỳ.
3. Bổ sung ràng buộc database và điều chỉnh stored function cho các bất biến thời gian/chỗ ở.
4. Hoàn thiện luồng billing–payment–công nợ trước khi mở rộng báo cáo tài chính.
5. Chuyển repository điện nước và hóa đơn sang stored function sau khi quy tắc tính tiền đã được xác nhận.

Tài liệu này là phân tích hiện trạng, không phải xác nhận các chức năng chưa có API đã hoàn thành.
