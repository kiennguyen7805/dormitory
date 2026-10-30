# Đề xuất giản lược database cho mục tiêu học xây dựng API nghiệp vụ

> Quyết định ngày 29/09/2026: áp dụng phương án B với 17 bảng, ba role cố định
> (`Admin`, `Staff`, `Student`) và chỉ nhập chỉ số điện nước thủ công. Bản
> triển khai nằm ở migration `20260929_0020`. Các phần bên dưới được giữ làm
> phân tích lựa chọn ban đầu; đề xuất lược thêm từng cột chưa được áp dụng.

## 1. Mục tiêu của tài liệu

Tài liệu này đánh giá schema hiện tại theo đúng mục tiêu của dự án: **học cách thiết kế, xây dựng và thao tác API theo nghiệp vụ**, không phải xây một hệ thống quản lý ký túc xá đủ để vận hành thực tế.

Phạm vi đánh giá dựa trên:

- 33 bảng ORM trong `persistence/models.py`;
- chuỗi migration hiện tại;
- các controller, schema request/response và repository đang có;
- các luồng đã triển khai trong tuần 1–3: tài khoản, phòng/giường, đăng ký, hợp đồng, điện nước và hóa đơn;
- các bảng mới chỉ được chuẩn bị cho tuần sau nhưng chưa có API hoàn chỉnh.

Phần phân tích dưới đây được viết trước khi triển khai. Quyết định áp dụng phương án B được ghi ở đầu tài liệu.

## 2. Kết luận ngắn

Schema hiện tại **không sai nếu mục tiêu là mô phỏng một sản phẩm tương đối đầy đủ**, nhưng đang chi tiết hơn mức cần thiết cho một dự án học API. Vấn đề chính không chỉ là số lượng 33 bảng, mà là:

1. Nhiều bảng chưa có API và chưa tham gia luồng demo hiện tại.
2. Một số tính năng được thiết kế ở mức gần production như quyền động, lưu file, import Excel hai bước, snapshot, nhật ký sự kiện và biên nhận thanh toán.
3. Người học phải hiểu quá nhiều khái niệm cùng lúc trước khi tập trung được vào request, validation, service, transaction, repository và response.
4. Schema lớn làm tăng số model, migration, khóa ngoại, seed và test phải bảo trì dù tính năng chưa được dùng.

Khuyến nghị chính là dùng **phương án cân bằng 17 bảng**. Phương án này vẫn đủ để học:

- đăng nhập, refresh token và phân vai;
- CRUD và quan hệ một-nhiều, một-một;
- đăng ký → duyệt → tạo hợp đồng → phân/chuyển giường;
- transaction và chống phân trùng giường;
- ghi chỉ số, biểu giá, tính tiền;
- hóa đơn nhiều dòng và chống tạo trùng.

Không nên gộp bảng chỉ để giảm con số nếu việc gộp làm mất ranh giới nghiệp vụ. Nên ưu tiên bỏ **module chưa dùng** và **trường không phục vụ API** trước.

## 3. Hiện trạng 33 bảng

| Nhóm | Bảng hiện tại | Tình trạng sử dụng |
|---|---|---|
| Identity | `roles`, `permissions`, `role_permissions`, `users`, `student_profiles` | Có API. `permissions` và `role_permissions` phục vụ RBAC động, trong khi dự án chỉ có ba vai trò cố định |
| Housing | `buildings`, `rooms`, `beds` | Có CRUD phòng; là phần cốt lõi |
| Contracts | `housing_applications`, `contracts`, `bed_assignments`, `room_transfer_requests`, `contract_events` | Ba bảng đầu có luồng API. Chuyển giường hiện ghi lịch sử bằng `bed_assignments`; hai bảng sau chưa được API hiện tại sử dụng trực tiếp |
| Utilities/files | `utilities`, `meters`, `utility_tariffs`, `tariff_tiers`, `stored_files`, `utility_import_batches`, `meter_readings` | Có API điện nước. Hai bảng file/import chỉ cần cho chức năng Excel hai bước |
| Billing | `bills`, `bill_items`, `payments` | Có API sinh/xem hóa đơn; chưa có API thanh toán |
| Violations | `violation_types`, `violations`, `violation_evidences` | Mới có schema nền, chưa có luồng API hoàn chỉnh |
| Maintenance | `maintenance_requests`, `maintenance_events`, `maintenance_plans` | Mới có schema nền, chưa có luồng API hoàn chỉnh |
| Notifications | `notifications`, `notification_targets`, `notification_reads` | Mới có schema nền, chưa có luồng API hoàn chỉnh |

Như vậy, 33 bảng hiện tại đang trộn ba loại phạm vi:

- chức năng cốt lõi đã chạy;
- chức năng phụ đã chạy nhưng khá nâng cao, ví dụ import Excel và quyền động;
- chức năng tương lai mới chỉ có schema.

Đây là nguyên nhân khiến database trông “quá chi tiết”.

## 4. Ba phương án để lựa chọn

### 4.1. Phương án A — An toàn, còn 21 bảng

Chỉ bỏ các bảng không có API trực tiếp hoặc không tham gia luồng hiện tại:

- `room_transfer_requests`;
- `contract_events`;
- `payments`;
- `violation_types`, `violations`, `violation_evidences`;
- `maintenance_requests`, `maintenance_events`, `maintenance_plans`;
- `notifications`, `notification_targets`, `notification_reads`.

Giữ nguyên quyền động và import Excel.

Ưu điểm:

- ít phải sửa code đang chạy;
- gần như giữ trọn API tuần 1–3;
- dễ mở rộng lại các module đã hoãn.

Nhược điểm:

- 21 bảng vẫn khá nhiều;
- người học vẫn phải xử lý RBAC động, lưu file và import theo batch;
- chưa giải quyết phần lớn cảm giác “chi tiết quá”.

Phương án này phù hợp nếu mục tiêu là giữ nguyên hầu hết bài đã làm và chỉ dọn schema tương lai.

### 4.2. Phương án B — Cân bằng, còn 17 bảng (khuyến nghị)

Giữ các bảng sau:

1. `roles`
2. `users`
3. `student_profiles`
4. `buildings`
5. `rooms`
6. `beds`
8. `housing_applications`
9. `contracts`
10. `bed_assignments`
11. `utilities`
12. `meters`
13. `utility_tariffs`
14. `tariff_tiers`
15. `meter_readings`
16. `bills`
17. `bill_items`

Ngoài 12 bảng của phương án A, bỏ thêm:

- `permissions` và `role_permissions`: thay quyền động bằng kiểm tra ba role cố định `Admin`, `Staff`, `Student`;
- `stored_files` và `utility_import_batches`: bỏ luồng import Excel hai bước, giữ API nhập chỉ số thủ công.

Lý do đây là phương án phù hợp nhất:

- Vẫn có nhiều loại quan hệ để học nhưng mỗi quan hệ đều gắn với luồng API thật.
- Vẫn có nghiệp vụ đủ sâu: duyệt đơn, phân giường, chuyển giường, tính điện nước và sinh hóa đơn.
- Không mất lịch sử chuyển giường vì `bed_assignments` đã lưu từng giai đoạn ở.
- Không mất phân quyền cơ bản; chỉ chuyển từ permission động sang role guard đơn giản.
- Không để logic xử lý file/Excel che khuất mục tiêu học API và transaction.
- Có thể thêm lại module sau bằng migration mới khi thực sự học tới tính năng đó.

### 4.3. Phương án C — Tối giản, khoảng 13 bảng

Giữ phần identity, housing, contract và billing giống phương án B, nhưng thay năm bảng điện nước:

- `utilities`;
- `meters`;
- `utility_tariffs`;
- `tariff_tiers`;
- `meter_readings`;

bằng một bảng đơn giản, ví dụ `utility_readings`:

```text
id
room_id
utility_type       -- Electricity hoặc Water
period_start
period_end
previous_reading
current_reading
unit_price
amount
created_at
```

Kết quả còn khoảng 13 bảng.

Ưu điểm:

- rất dễ hiểu và demo CRUD;
- ít join, ít seed, ít validation;
- phù hợp nếu chỉ cần học API căn bản trong thời gian ngắn.

Nhược điểm:

- không còn mô hình công tơ riêng;
- không học được biểu giá theo thời gian và lũy tiến nhiều bậc;
- dữ liệu giá bị lặp ở từng lần ghi chỉ số;
- khi yêu cầu nghiệp vụ tăng, gần như phải thiết kế lại module điện nước.

Không khuyến nghị phương án này nếu phần tính giá lũy tiến và hóa đơn là nội dung cần trình bày trong môn học.

## 5. Những bảng nên giữ riêng, không nên gộp

### 5.1. `users` và `student_profiles`

Không nên gộp trong phương án khuyến nghị. `users` chứa dữ liệu xác thực dùng cho cả Admin, Staff và Student; các trường mã sinh viên, khoa, khóa, ngày sinh chỉ thuộc Student. Gộp hai bảng sẽ tạo nhiều cột `NULL` cho Admin/Staff và làm lẫn trách nhiệm tài khoản với hồ sơ nghiệp vụ.

Quan hệ một-một này cũng là một ví dụ học tập tốt và không tạo nhiều độ phức tạp.

### 5.2. `buildings`, `rooms` và `beds`

Không nên gộp vì đây là quan hệ phân cấp thật:

```text
building 1 ── n room 1 ── n bed
```

Nếu đưa thông tin tòa vào từng phòng hoặc thông tin giường vào một cột JSON của phòng, dữ liệu sẽ lặp, khó kiểm tra khóa duy nhất và khó phân giường bằng khóa ngoại.

### 5.3. `housing_applications`, `contracts` và `bed_assignments`

Không nên gộp:

- đơn đăng ký có thể bị từ chối và không sinh hợp đồng;
- hợp đồng là cam kết đã được duyệt;
- một hợp đồng có thể có nhiều lần phân giường do chuyển chỗ.

Ba bảng này tạo ra một luồng nghiệp vụ rõ ràng để học state transition, transaction và lịch sử dữ liệu.

### 5.4. `bills` và `bill_items`

Không nên gộp vì một hóa đơn có nhiều khoản: tiền phòng, điện, nước. Nếu đưa các khoản thành các cột cố định trên `bills`, mỗi loại phí mới sẽ buộc phải sửa schema. Nếu đưa thành JSON, việc truy vấn và kiểm tra tổng tiền khó hơn.

Quan hệ header/detail này là mẫu phổ biến trong API nghiệp vụ và đáng giữ để học.

## 6. Những bảng có thể bỏ hoặc thay bằng cách đơn giản hơn

| Bảng | Đề xuất | Lý do |
|---|---|---|
| `permissions` | Bỏ trong phương án B | Ba role đã cố định; permission động chưa cần cho mục tiêu học API |
| `role_permissions` | Bỏ cùng `permissions` | Không còn quan hệ nhiều-nhiều khi quyền được kiểm tra trực tiếp theo role |
| `room_transfer_requests` | Bỏ | API hiện chuyển giường trực tiếp; bảng chưa tham gia luồng hiện tại |
| `contract_events` | Bỏ | Lịch sử chỗ ở đã thể hiện qua `bed_assignments`; bảng chưa được repository/API dùng |
| `stored_files` | Bỏ nếu không học upload/lưu file | Chỉ cần cho import Excel và minh chứng/biên nhận tương lai |
| `utility_import_batches` | Bỏ nếu giữ nhập thủ công | Preview/confirm import là luồng nâng cao, không bắt buộc để học API nghiệp vụ chính |
| `payments` | Tạm bỏ | Chưa có controller/service thanh toán; có thể thêm lại thành một bài riêng |
| 9 bảng vi phạm/bảo trì/thông báo | Bỏ khỏi MVP học tập | Hiện chỉ có model/migration, chưa có use case hoàn chỉnh |

“Bỏ” ở đây nghĩa là bỏ khỏi phạm vi triển khai hiện tại. Các ý tưởng vẫn có thể được ghi trong backlog và thêm lại bằng migration khi cần.

## 7. Đề xuất lược bớt trường trong 17 bảng được giữ

### 7.1. Nguyên tắc chung

- Giữ trường phục vụ request, response, ràng buộc nghiệp vụ hoặc truy vấn thực tế.
- Giữ `created_at`; chỉ giữ `updated_at` ở bảng có API cập nhật.
- Bỏ các trường `created_by`, `updated_by` nếu dự án không có yêu cầu audit.
- Tránh hai trường biểu diễn cùng một trạng thái, ví dụ vừa `status = Inactive` vừa `is_active = false`.
- Không lưu dữ liệu có thể suy ra một cách chắc chắn, trừ khi đó là snapshot tài chính cần bảo toàn lịch sử.

### 7.2. Đề xuất theo bảng/nhóm

| Bảng/nhóm | Trường có thể bỏ hoặc đơn giản hóa | Nhận xét |
|---|---|---|
| `roles` | `display_name`, `description`, `is_active`, `created_at`, `updated_at` | Nếu chỉ seed ba role cố định thì chỉ cần `id`, `name` |
| `users` | `last_password_changed_at`, `created_by`, `updated_by` | Giữ các trường refresh token vì API refresh đang dùng; giữ `created_at` |
| `student_profiles` | Có thể bỏ `address`, `identity_number`, `emergency_contact_name`, `emergency_contact_phone` | Các trường này có API cập nhật nhưng không tham gia luồng đăng ký/phòng/hợp đồng hiện tại |
| `buildings` | `created_by`, `updated_by` | `code`, `name`, `address`, `floors`, `is_active` vẫn phù hợp CRUD |
| `rooms` | `updated_by`, `note`; cân nhắc bỏ `managed_by_staff_id` | Chỉ bỏ `managed_by_staff_id` nếu không cần Staff chỉ quản lý phòng được giao |
| `rooms` | Chọn một trong `status` hoặc `is_active` | Nên dùng `status = Available/Maintenance/Inactive` và bỏ `is_active` để tránh mâu thuẫn |
| `beds` | `note`; cân nhắc bỏ `updated_at` | Giữ `is_active` nếu cần khóa một giường hỏng/bảo trì |
| `housing_applications` | `expected_start_date`, `expected_end_date`, `note`, `cancelled_at` | Các trường này tồn tại trong DB nhưng request/response hiện không dùng |
| `contracts` | `issued_at`, `issued_by`; cân nhắc bỏ `student_id` | `student_id` có thể suy ra từ `application_id`, nhưng giữ lại giúp truy vấn ownership đơn giản hơn; không bắt buộc phải bỏ |
| `bed_assignments` | `assigned_by`, `ended_by`, `end_reason` | Giữ `start_date`, `end_date`, `status` để thể hiện lịch sử và lần ở hiện tại |
| `utilities` | `rounding_scale`, `created_at` | Với bài học đơn giản có thể quy định làm tròn thống nhất trong code |
| `meters` | `serial_number`, `installed_at`, `retired_at`, `note` | Giữ `initial_reading` và `is_active` vì ảnh hưởng việc ghi chỉ số |
| `utility_tariffs` | `created_by` | Giữ khoảng hiệu lực và loại `Flat/Tiered` nếu vẫn dạy tính giá lũy tiến |
| `meter_readings` | `source`, `import_batch_id`, `recorded_by` | Bỏ khi bỏ import Excel; chỉ còn nguồn nhập thủ công |
| `meter_readings` | Cân nhắc bỏ `tariff_snapshot` | Có thể bỏ nếu biểu giá đã dùng là bất biến. Nếu cho sửa/xóa biểu giá thì phải giữ snapshot |
| `bills` | `student_id`, `adjustment_amount`, `paid_amount`, `balance_amount`, toàn bộ `voided_*` | Phù hợp khi chưa triển khai thanh toán/điều chỉnh/hủy hóa đơn. `student_id` suy ra từ contract |
| `bill_items` | `reference_type`, `reference_id`, `calculation_snapshot` | Có thể bỏ cho bài học đơn giản; giữ nếu cần truy vết mỗi khoản điện/nước về bản ghi nguồn |

Không nên xóa mọi cột timestamp chỉ để schema ngắn hơn. `created_at` và `updated_at` giúp học cách trả dữ liệu, sắp xếp và kiểm tra thay đổi mà gần như không làm phức tạp request.

## 8. Các quyết định nghiệp vụ đã chốt

### 8.1. Có học phân quyền theo permission không?

- Nếu **không**, bỏ `permissions`, `role_permissions`, trường `permissions` trong response và dùng role guard.
- Nếu **có**, giữ nguyên hai bảng này vì quan hệ nhiều-nhiều là đúng và không nên gộp permission vào chuỗi/JSON trong `roles`.

### 8.2. Import Excel

Không triển khai. `stored_files`, `utility_import_batches` và ba endpoint
template/preview/confirm đã bị loại; chỉ giữ nhập chỉ số thủ công.

### 8.3. Có cần demo thanh toán không?

- Nếu **chưa**, bỏ `payments` và giản lược các trường công nợ trên `bills`.
- Nếu **có trong giai đoạn kế tiếp**, giữ `payments`; không nên gộp vào `bills` vì một hóa đơn có thể được thanh toán nhiều lần.

### 8.4. Có cần Staff chỉ quản lý phòng được giao không?

- Nếu **không**, bỏ `rooms.managed_by_staff_id` để đơn giản query và authorization.
- Nếu **có**, phải giữ vì trường này đang được dùng trong repository, stored function và room matrix.

## 9. Ảnh hưởng đến mã nguồn nếu chọn phương án B

Không thể chỉ `DROP TABLE`/`DROP COLUMN` trong PostgreSQL. Dự án dùng SQLAlchemy, Alembic và PostgreSQL stored function nên phải sửa đồng bộ.

| Phần thay đổi | Mã nguồn chịu ảnh hưởng |
|---|---|
| Bỏ permission động | `models.py`, seeder, `auth.sql`, `identity.sql`, identity repository/controller, authorization dependency, schema `UserRead`/`PermissionRead`, test identity |
| Bỏ import Excel | utility controller/service/repository, schema import, dependency Excel, test tuần 3, README và hướng dẫn kiểm thử thủ công |
| Bỏ bảng tương lai | `models.py` và migration/baseline; hiện chưa có controller/repository tương ứng nên ảnh hưởng thấp |
| Bỏ transfer request/event | `models.py` và migration; API chuyển giường hiện vẫn hoạt động bằng `bed_assignments` sau khi kiểm tra lại stored function |
| Bỏ payment và trường công nợ | billing model/schema/repository, migration và response hóa đơn |
| Bỏ các trường housing/contract | file SQL trong `persistence/sql/`, stored repository, Pydantic schema và integration test liên quan |

Các migration `0011`–`0019` đang cài PostgreSQL function với chữ ký và cột trả về cụ thể. Nếu bỏ cột, phải cập nhật định nghĩa function cùng lúc; nếu không API có thể lỗi dù ORM đã sửa đúng.

## 10. Cách triển khai sau khi đã quyết định

### Trường hợp database chỉ có dữ liệu demo

Đây là cách phù hợp nhất với dự án học tập:

1. Chốt danh sách bảng và trường cuối cùng.
2. Sửa model, Pydantic schema, controller, service, repository và SQL function.
3. Gom schema thành baseline migration mới dễ đọc.
4. Xóa volume PostgreSQL của môi trường phát triển và tạo lại database.
5. Chạy seed, pytest và kiểm thử thủ công các luồng API trong Postman.
6. Cập nhật ERD, README và tài liệu nghiệp vụ.

Ưu điểm là migration sạch, người đọc không phải đi qua chuỗi “tạo rồi xóa” của nhiều bảng không còn dùng.

### Trường hợp cần giữ dữ liệu hiện có

1. Sao lưu database.
2. Bỏ hoặc sửa code sử dụng bảng/trường cũ trước.
3. Tạo migration mới để chuyển dữ liệu cần giữ.
4. Drop khóa ngoại, index, bảng và cột theo đúng thứ tự phụ thuộc.
5. Cài lại các PostgreSQL function đã cập nhật.
6. Chạy test và đối chiếu dữ liệu trước/sau migration.

Không nên sửa trực tiếp migration cũ nếu database đã được dùng ở nhiều môi trường và cần nâng cấp tại chỗ.

## 11. Quyết định được đề xuất

Đề xuất chọn **phương án B — 17 bảng**, với phạm vi cụ thể:

- giữ authentication bằng JWT và refresh token;
- giữ ba role cố định, bỏ permission động;
- giữ toàn bộ housing và luồng application/contract/bed assignment;
- giữ biểu giá lũy tiến để phần nghiệp vụ tính tiền vẫn có giá trị;
- chỉ nhập chỉ số thủ công, bỏ import Excel;
- giữ hóa đơn và dòng hóa đơn, chưa làm payment;
- hoãn vi phạm, bảo trì và thông báo sang backlog;
- lược các trường audit chi tiết và các trường chưa xuất hiện trong API;
- giữ `student_profiles`, `beds`, `bed_assignments` và `bill_items` riêng, không gộp.

Đây là điểm cân bằng giữa “database đủ đúng để học thiết kế nghiệp vụ” và “không biến bài tập API thành một sản phẩm vận hành thực tế”.

## 12. Quyết định cuối cùng

- [x] Chọn phương án B với 17 bảng.
- [x] Dùng ba role cố định, không giữ permission động.
- [x] Không triển khai import Excel.
- [x] Chưa triển khai thanh toán trong phạm vi hiện tại.
- [x] Không phân phạm vi quản lý phòng riêng theo từng Staff.
- [x] Giữ biểu giá lũy tiến nhiều bậc.
- [x] Migration `20260929_0020` là mốc chuyển schema sang phạm vi đã chốt.
