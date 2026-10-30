# Bảng thống kê database ký túc xá

Tài liệu này mô tả schema `public` theo đúng yêu cầu, gồm **17 bảng** nghiệp vụ và **1 bảng kỹ thuật** do Alembic quản lý. 

## 1. Cách đọc kiểu dữ liệu

| Kiểu Adminer hiển thị | Cách viết thường gặp | Ý nghĩa và lý do sử dụng |
|---|---|---|
| `uuid` | `uuid` | Mã định danh 128 bit; dùng làm khóa chính/khóa ngoại, phù hợp khi dữ liệu có thể được tạo từ nhiều dịch vụ. |
| `character varying(n)` | `varchar(n)` | Chuỗi có độ dài tối đa `n`; hai tên này tương đương trong PostgreSQL. |
| `boolean` | `bool` | Giá trị đúng/sai, ví dụ đang hoạt động hay đã khóa. |
| `integer` | `int` | Số nguyên, ví dụ tầng, sức chứa và thứ tự bậc giá. |
| `numeric` | `decimal` | Số thập phân chính xác; phù hợp cho tiền, đơn giá và chỉ số điện nước. |
| `date` | `date` | Chỉ lưu ngày, không lưu giờ; phù hợp cho kỳ hợp đồng và kỳ hóa đơn. |
| `timestamp with time zone` | `timestamptz` | Lưu một thời điểm có xử lý múi giờ; phù hợp cho lịch sử thao tác. |
| `json` | `json` | Lưu một cấu trúc JSON; dùng để chụp lại biểu giá/cách tính tại một thời điểm. |

Ký hiệu: **PK** là khóa chính; **FK** là khóa ngoại; **UQ** là giá trị hoặc nhóm giá trị không được trùng; **NULL** là được phép để trống.

## 2. Danh sách tổng quát theo thứ tự chữ cái

| STT | Bảng | Loại | Chức năng |
|---:|---|---|---|
| 1 | `alembic_version` | Kỹ thuật | Ghi phiên bản migration đang áp dụng. |
| 2 | `bed_assignments` | Nghiệp vụ | Lưu lịch sử phân và chuyển giường của hợp đồng. |
| 3 | `beds` | Nghiệp vụ | Danh mục giường trong từng phòng. |
| 4 | `bill_items` | Nghiệp vụ | Các khoản tiền chi tiết của hóa đơn. |
| 5 | `bills` | Nghiệp vụ | Thông tin chung và tổng tiền hóa đơn. |
| 6 | `buildings` | Nghiệp vụ | Danh mục tòa nhà ký túc xá. |
| 7 | `contracts` | Nghiệp vụ | Hợp đồng ở của sinh viên. |
| 8 | `housing_applications` | Nghiệp vụ | Đơn đăng ký ở ký túc xá. |
| 9 | `meter_readings` | Nghiệp vụ | Chỉ số công tơ và tiền điện/nước theo kỳ. |
| 10 | `meters` | Nghiệp vụ | Công tơ điện/nước gắn với phòng. |
| 11 | `roles` | Nghiệp vụ | Ba vai trò `Admin`, `Staff`, `Student`. |
| 12 | `room_types` | Nghiệp vụ | Loại phòng, sức chứa và giá mặc định. |
| 13 | `rooms` | Nghiệp vụ | Phòng thuộc tòa nhà và loại phòng. |
| 14 | `student_profiles` | Nghiệp vụ | Thông tin riêng của tài khoản sinh viên. |
| 15 | `tariff_tiers` | Nghiệp vụ | Các bậc giá của một biểu giá lũy tiến. |
| 16 | `users` | Nghiệp vụ | Tài khoản, xác thực và vai trò người dùng. |
| 17 | `utilities` | Nghiệp vụ | Danh mục dịch vụ điện và nước. |
| 18 | `utility_tariffs` | Nghiệp vụ | Biểu giá dịch vụ theo thời gian. |

## 3. Thuộc tính của từng bảng

### 3.1. `alembic_version` — phiên bản database

Đây là bảng kỹ thuật do Alembic quản lý, không tính vào 17 bảng nghiệp vụ.

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `version_num` | `varchar(32)` | PK | Mã migration mới nhất đã chạy, hiện tại là `20261004_0022`. |

### 3.2. `bed_assignments` — lịch sử phân giường

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã duy nhất của một lần phân giường. |
| `contract_id` | `uuid` | FK → `contracts.id` | Hợp đồng được phân giường. |
| `bed_id` | `uuid` | FK → `beds.id` | Giường được sử dụng. |
| `start_date` | `date` | Bắt buộc | Ngày bắt đầu sử dụng giường. |
| `end_date` | `date` | NULL | Ngày kết thúc; để trống nếu đang ở. |
| `status` | `varchar(20)` | Bắt buộc | Trạng thái của lần phân giường. |
| `assigned_by` | `uuid` | FK → `users.id`, NULL | Cán bộ đã phân giường. |
| `ended_by` | `uuid` | FK → `users.id`, NULL | Cán bộ kết thúc lần ở. |
| `end_reason` | `varchar(500)` | NULL | Lý do kết thúc hoặc chuyển giường. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo bản ghi. |

### 3.3. `beds` — giường

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã giường. |
| `room_id` | `uuid` | FK → `rooms.id` | Phòng chứa giường. |
| `code` | `varchar(20)` | Bắt buộc | Mã giường, ví dụ `G01`. |
| `is_active` | `boolean` | Bắt buộc | Giường còn được sử dụng hay không. |
| `note` | `varchar(300)` | NULL | Ghi chú tình trạng hoặc vị trí giường. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật gần nhất. |

Nhóm (`room_id`, `code`) là duy nhất: một phòng không thể có hai giường cùng mã.

### 3.4. `bill_items` — chi tiết hóa đơn

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã dòng hóa đơn. |
| `bill_id` | `uuid` | FK → `bills.id` | Hóa đơn chứa dòng này. |
| `item_type` | `varchar(30)` | Bắt buộc | Loại khoản thu, ví dụ tiền phòng, điện hoặc nước. |
| `reference_type` | `varchar(50)` | NULL | Loại dữ liệu nguồn dùng để tính khoản tiền. |
| `reference_id` | `uuid` | NULL | Mã bản ghi nguồn, nếu có. |
| `description` | `varchar(300)` | Bắt buộc | Nội dung hiển thị của khoản thu. |
| `quantity` | `numeric` | Bắt buộc | Số lượng, ví dụ số tháng hoặc số kWh. |
| `unit_price` | `numeric` | Bắt buộc | Đơn giá. |
| `amount` | `numeric` | Bắt buộc | Thành tiền của dòng. |
| `calculation_snapshot` | `json` | NULL | Bản chụp chi tiết cách tính tại lúc lập hóa đơn. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo dòng hóa đơn. |

### 3.5. `bills` — hóa đơn

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã hóa đơn. |
| `bill_no` | `varchar(50)` | UQ | Số hóa đơn không được trùng. |
| `contract_id` | `uuid` | FK → `contracts.id` | Hợp đồng được lập hóa đơn. |
| `student_id` | `uuid` | FK → `users.id` | Sinh viên phải thanh toán. |
| `period_start` | `date` | Bắt buộc | Ngày đầu kỳ tính tiền. |
| `period_end` | `date` | Bắt buộc | Ngày cuối kỳ tính tiền. |
| `issued_date` | `date` | Bắt buộc | Ngày phát hành hóa đơn. |
| `due_date` | `date` | Bắt buộc | Hạn thanh toán. |
| `status` | `varchar(20)` | Bắt buộc | Trạng thái hóa đơn. |
| `subtotal` | `numeric` | Bắt buộc | Tổng các dòng trước điều chỉnh. |
| `adjustment_amount` | `numeric` | Bắt buộc | Khoản cộng/trừ điều chỉnh. |
| `total_amount` | `numeric` | Bắt buộc | Tổng số tiền phải trả. |
| `paid_amount` | `numeric` | Bắt buộc | Số tiền đã thanh toán. |
| `balance_amount` | `numeric` | Bắt buộc | Số tiền còn thiếu. |
| `idempotency_key` | `varchar(100)` | UQ | Khóa chống tạo trùng hóa đơn khi gửi lại request. |
| `issued_by` | `uuid` | FK → `users.id`, NULL | Người phát hành hóa đơn. |
| `voided_by` | `uuid` | FK → `users.id`, NULL | Người hủy hóa đơn. |
| `voided_at` | `timestamptz` | NULL | Thời điểm hủy. |
| `void_reason` | `varchar(500)` | NULL | Lý do hủy. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |

### 3.6. `buildings` — tòa nhà

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã tòa nhà. |
| `code` | `varchar(20)` | UQ | Mã tòa, ví dụ `A1`. |
| `name` | `varchar(120)` | Bắt buộc | Tên tòa. |
| `address` | `varchar(250)` | Bắt buộc | Địa chỉ tòa nhà. |
| `floors` | `integer` | Bắt buộc | Số tầng. |
| `is_active` | `boolean` | Bắt buộc | Tòa còn hoạt động hay không. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `created_by` | `uuid` | FK → `users.id`, NULL | Người tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |
| `updated_by` | `uuid` | FK → `users.id`, NULL | Người cập nhật. |

### 3.7. `contracts` — hợp đồng ở

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã hợp đồng. |
| `contract_no` | `varchar(50)` | UQ | Số hợp đồng. |
| `student_id` | `uuid` | FK → `users.id` | Sinh viên đứng tên hợp đồng. |
| `application_id` | `uuid` | FK → `housing_applications.id`, UQ | Đơn được dùng để tạo hợp đồng; một đơn chỉ có một hợp đồng. |
| `start_date` | `date` | Bắt buộc | Ngày hợp đồng bắt đầu. |
| `end_date` | `date` | Bắt buộc | Ngày hợp đồng kết thúc. |
| `status` | `varchar(20)` | Bắt buộc | Trạng thái hợp đồng. |
| `base_rate` | `numeric` | Bắt buộc | Giá phòng cơ bản được chốt trong hợp đồng. |
| `terminated_at` | `timestamptz` | NULL | Thời điểm chấm dứt trước hạn. |
| `issued_at` | `timestamptz` | NULL | Thời điểm phát hành. |
| `issued_by` | `uuid` | FK → `users.id`, NULL | Người phát hành. |
| `termination_reason` | `varchar(500)` | NULL | Lý do chấm dứt. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |

### 3.8. `housing_applications` — đơn đăng ký ở

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã đơn đăng ký. |
| `student_id` | `uuid` | FK → `users.id` | Sinh viên gửi đơn. |
| `term_code` | `varchar(30)` | Bắt buộc | Mã học kỳ hoặc đợt đăng ký. |
| `preferred_room_type_id` | `uuid` | FK → `room_types.id` | Loại phòng mong muốn. |
| `status` | `varchar(20)` | Bắt buộc | Trạng thái đơn. |
| `rejection_reason` | `varchar(500)` | NULL | Lý do từ chối. |
| `reviewed_by_user_id` | `uuid` | FK → `users.id`, NULL | Cán bộ duyệt đơn. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm gửi đơn. |
| `reviewed_at` | `timestamptz` | NULL | Thời điểm duyệt hoặc từ chối. |
| `expected_start_date` | `date` | NULL | Ngày dự kiến bắt đầu ở. |
| `expected_end_date` | `date` | NULL | Ngày dự kiến kết thúc ở. |
| `note` | `varchar(1000)` | NULL | Ghi chú của sinh viên. |
| `cancelled_at` | `timestamptz` | NULL | Thời điểm sinh viên hủy đơn. |

### 3.9. `meter_readings` — chỉ số công tơ

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã lần ghi chỉ số. |
| `meter_id` | `uuid` | FK → `meters.id` | Công tơ được ghi. |
| `period_start` | `date` | Bắt buộc | Ngày đầu kỳ. |
| `period_end` | `date` | Bắt buộc | Ngày cuối kỳ. |
| `previous_reading` | `numeric` | Bắt buộc | Chỉ số đầu kỳ. |
| `current_reading` | `numeric` | Bắt buộc | Chỉ số cuối kỳ. |
| `consumption` | `numeric` | Bắt buộc | Lượng sử dụng = chỉ số cuối − chỉ số đầu. |
| `tariff_id` | `uuid` | FK → `utility_tariffs.id` | Biểu giá được áp dụng. |
| `tariff_snapshot` | `json` | Bắt buộc | Bản chụp biểu giá tại thời điểm tính. |
| `calculated_amount` | `numeric` | Bắt buộc | Số tiền đã tính cho lượng sử dụng. |
| `recorded_by` | `uuid` | FK → `users.id`, NULL | Người nhập chỉ số. |
| `recorded_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm nhập. |

Nhóm (`meter_id`, `period_start`, `period_end`) là duy nhất để một công tơ không có hai bản ghi trùng kỳ.

### 3.10. `meters` — công tơ

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã công tơ. |
| `utility_id` | `uuid` | FK → `utilities.id` | Công tơ đo điện hay nước. |
| `room_id` | `uuid` | FK → `rooms.id` | Phòng được gắn công tơ. |
| `meter_code` | `varchar(50)` | UQ | Mã quản lý công tơ. |
| `serial_number` | `varchar(100)` | NULL | Số sê-ri của thiết bị. |
| `installed_at` | `date` | NULL | Ngày lắp đặt. |
| `initial_reading` | `numeric` | Bắt buộc | Chỉ số ban đầu khi đưa vào sử dụng. |
| `is_active` | `boolean` | Mặc định `true` | Công tơ còn hoạt động hay không. |
| `retired_at` | `date` | NULL | Ngày ngừng sử dụng. |
| `note` | `varchar(500)` | NULL | Ghi chú. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |

### 3.11. `roles` — vai trò

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã vai trò. |
| `name` | `varchar(30)` | UQ | Tên kỹ thuật: `Admin`, `Staff` hoặc `Student`. |
| `display_name` | `varchar(100)` | NULL | Tên thân thiện để hiển thị. |
| `description` | `varchar(300)` | NULL | Mô tả quyền hạn của vai trò. |
| `is_active` | `boolean` | Mặc định `true` | Vai trò còn được sử dụng hay không. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |

### 3.12. `room_types` — loại phòng

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã loại phòng. |
| `name` | `varchar(120)` | UQ | Tên loại phòng. |
| `default_monthly_rate` | `numeric` | Bắt buộc | Giá thuê mặc định mỗi tháng. |
| `is_active` | `boolean` | Bắt buộc | Loại phòng còn được sử dụng hay không. |
| `default_capacity` | `integer` | NULL | Sức chứa mặc định. |
| `description` | `varchar(500)` | NULL | Mô tả loại phòng. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |

### 3.13. `rooms` — phòng

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã phòng. |
| `building_id` | `uuid` | FK → `buildings.id` | Tòa chứa phòng. |
| `room_type_id` | `uuid` | FK → `room_types.id` | Loại phòng. |
| `code` | `varchar(20)` | Bắt buộc | Mã phòng, ví dụ `101`. |
| `floor` | `integer` | Bắt buộc | Tầng của phòng. |
| `is_active` | `boolean` | Bắt buộc | Phòng còn được sử dụng hay không. |
| `gender_policy` | `varchar(20)` | Mặc định `Unassigned` | Quy định giới tính của phòng. |
| `managed_by_staff_id` | `uuid` | FK → `users.id`, NULL | Cán bộ phụ trách phòng. |
| `status` | `varchar(20)` | Mặc định `Available` | Trạng thái vận hành của phòng. |
| `note` | `varchar(500)` | NULL | Ghi chú. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |
| `updated_by` | `uuid` | FK → `users.id`, NULL | Người cập nhật. |

Nhóm (`building_id`, `code`) là duy nhất: hai tòa khác nhau có thể cùng có phòng `101`, nhưng một tòa không thể có hai phòng `101`.

### 3.14. `student_profiles` — hồ sơ sinh viên

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `user_id` | `uuid` | PK, FK → `users.id` | Tài khoản sở hữu hồ sơ; đồng thời bảo đảm quan hệ một-một. |
| `student_code` | `varchar(30)` | UQ | Mã sinh viên. |
| `faculty` | `varchar(150)` | Mặc định chuỗi rỗng | Khoa. |
| `cohort` | `varchar(30)` | Mặc định chuỗi rỗng | Khóa học. |
| `date_of_birth` | `date` | NULL | Ngày sinh. |
| `phone` | `varchar(30)` | Mặc định chuỗi rỗng | Số điện thoại. |
| `address` | `varchar(300)` | Mặc định chuỗi rỗng | Địa chỉ. |
| `emergency_contact_name` | `varchar(120)` | Mặc định chuỗi rỗng | Người liên hệ khẩn cấp. |
| `emergency_contact_phone` | `varchar(30)` | Mặc định chuỗi rỗng | Số điện thoại khẩn cấp. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo hồ sơ. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật hồ sơ. |
| `gender` | `varchar(20)` | NULL | Giới tính, phục vụ kiểm tra chính sách phòng. |
| `identity_number` | `varchar(30)` | NULL | CCCD hoặc giấy tờ định danh. |

### 3.15. `tariff_tiers` — bậc giá

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã bậc giá. |
| `tariff_id` | `uuid` | FK → `utility_tariffs.id` | Biểu giá chứa bậc này. |
| `tier_order` | `integer` | Bắt buộc | Thứ tự bậc 1, 2, 3… |
| `from_quantity` | `numeric` | Bắt buộc | Sản lượng bắt đầu của bậc. |
| `to_quantity` | `numeric` | NULL | Sản lượng kết thúc; để trống cho bậc cuối không giới hạn. |
| `unit_price` | `numeric` | Bắt buộc | Đơn giá của bậc. |

Nhóm (`tariff_id`, `tier_order`) là duy nhất: một biểu giá không có hai bậc cùng thứ tự.

### 3.16. `users` — tài khoản người dùng

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã người dùng. |
| `email` | `varchar(254)` | UQ | Email đăng nhập. |
| `full_name` | `varchar(120)` | Bắt buộc | Họ tên. |
| `password_hash` | `varchar(255)` | Bắt buộc | Mật khẩu đã băm; không lưu mật khẩu gốc. |
| `is_active` | `boolean` | Bắt buộc | Tài khoản còn hoạt động hay bị khóa. |
| `role_id` | `uuid` | FK → `roles.id` | Vai trò của người dùng. |
| `last_password_changed_at` | `timestamptz` | NULL | Lần đổi mật khẩu gần nhất. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo tài khoản. |
| `created_by` | `uuid` | FK tự tham chiếu → `users.id`, NULL | Người tạo tài khoản. |
| `updated_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm cập nhật. |
| `updated_by` | `uuid` | FK tự tham chiếu → `users.id`, NULL | Người cập nhật. |
| `refresh_token_hash` | `varchar(64)` | UQ, NULL | Bản băm refresh token. |
| `refresh_token_expires_at` | `timestamptz` | NULL | Thời điểm refresh token hết hạn. |
| `refresh_token_revoked_at` | `timestamptz` | NULL | Thời điểm refresh token bị thu hồi. |

### 3.17. `utilities` — loại dịch vụ

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã dịch vụ. |
| `code` | `varchar(30)` | UQ | Mã kỹ thuật, ví dụ `ELECTRICITY` hoặc `WATER`. |
| `name` | `varchar(100)` | Bắt buộc | Tên dịch vụ. |
| `unit` | `varchar(30)` | Bắt buộc | Đơn vị đo, ví dụ `kWh` hoặc `m3`. |
| `rounding_scale` | `integer` | Bắt buộc | Số chữ số thập phân dùng khi làm tròn. |
| `is_active` | `boolean` | Mặc định `true` | Dịch vụ còn sử dụng hay không. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |

### 3.18. `utility_tariffs` — biểu giá điện nước

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Giải thích |
|---|---|---|---|
| `id` | `uuid` | PK | Mã biểu giá. |
| `utility_id` | `uuid` | FK → `utilities.id` | Dịch vụ áp dụng biểu giá. |
| `name` | `varchar(120)` | Bắt buộc | Tên biểu giá. |
| `effective_from` | `date` | Bắt buộc | Ngày bắt đầu hiệu lực. |
| `effective_to` | `date` | NULL | Ngày hết hiệu lực; để trống nếu còn hiệu lực. |
| `calculation_type` | `varchar(20)` | Bắt buộc | Kiểu tính đồng giá hoặc lũy tiến. |
| `is_active` | `boolean` | Mặc định `true` | Biểu giá còn được sử dụng hay không. |
| `created_by` | `uuid` | FK → `users.id`, NULL | Người tạo biểu giá. |
| `created_at` | `timestamptz` | Mặc định thời điểm hiện tại | Thời điểm tạo. |

## 4. Luồng quan hệ dễ ghi nhớ

```text
roles → users → student_profiles
                  ↓
          housing_applications → contracts → bed_assignments → beds
                                                              ↓
buildings → rooms ← room_types                              rooms
               ↓
utilities → meters → meter_readings ← utility_tariffs → tariff_tiers
                              ↓
contracts → bills → bill_items
```

Đọc theo nghiệp vụ: người dùng có vai trò; sinh viên có hồ sơ và gửi đơn; đơn được duyệt thành hợp đồng; hợp đồng được phân giường; phòng có công tơ điện/nước; chỉ số được tính theo biểu giá; cuối kỳ hợp đồng nhận hóa đơn gồm nhiều dòng chi tiết.

## 5. Nguồn đối chiếu kiểu dữ liệu

- [PostgreSQL — Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL — Character Types](https://www.postgresql.org/docs/current/datatype-character.html)
- [PostgreSQL — Numeric Types](https://www.postgresql.org/docs/current/datatype-numeric.html)
- [PostgreSQL — Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)
- [PostgreSQL — UUID Type](https://www.postgresql.org/docs/current/datatype-uuid.html)
- [PostgreSQL — JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL — Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

Các tên cột, kiểu dữ liệu và quan hệ trong tài liệu này được đọc trực tiếp từ schema PostgreSQL của dự án ngày 04/10/2026; nguồn PostgreSQL ở trên dùng để giải thích ý nghĩa chuẩn của kiểu dữ liệu và ràng buộc.
