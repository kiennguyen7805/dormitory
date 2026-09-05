# PHÂN TÍCH BÀI TOÁN — HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ (MVP 5 TUẦN)

> Bản điều chỉnh từ tài liệu phân tích gốc, thu gọn phạm vi để **làm được trong 5 tuần**, mô tả rõ **từng chức năng làm gì**, và bổ sung **bộ thiết kế giao diện/màu sắc** còn thiếu trong bản gốc.
>
> Đi kèm file `02-cau-truc-du-an.md` (kiến trúc, thư mục, tech stack, database, API).

---

## 1. Nhắc lại mục tiêu & ràng buộc

- Thời gian: **5 tuần**, phải chạy được **đầy đủ chức năng cơ bản** (không phải chỉ demo giả).
- Có **tích hợp AI cơ bản** (không cần RAG/vector DB/agent phức tạp).
- 3 vai trò: **Admin, Cán bộ KTX (Staff), Sinh viên (Student)**.
- Ưu tiên: **chạy đúng luồng nghiệp vụ đầu-cuối** hơn là làm đẹp từng chi tiết nhỏ.

### Nguyên tắc cắt scope để kịp 5 tuần

So với bản phân tích gốc, các mục sau được **đơn giản hoá** (không xoá hẳn, chỉ giảm độ phức tạp) để nhóm không bị sa lầy:

| Mục trong bản gốc | Xử lý cho MVP 5 tuần |
|---|---|
| `room_transfer_requests` (luồng xin chuyển phòng 2 bước: sinh viên yêu cầu → duyệt) | Giữ nguyên **nếu còn thời gian ở tuần 5**; nếu gấp, cho phép Staff **chuyển phòng trực tiếp** (vẫn ghi lịch sử qua `bed_assignments`), sinh viên chỉ "gửi nguyện vọng" bằng ghi chú, không cần state machine riêng |
| `contract_amendments` (log thay đổi hợp đồng dạng JSON) | Bỏ bảng riêng ở MVP; nếu đổi giá khi chuyển phòng, chỉ cần tạo `bill_item` loại `Adjustment` có ghi chú lý do |
| Vi phạm có trạng thái `Appealed` (khiếu nại) | Bỏ ở MVP. Chỉ còn: `Recorded → Confirmed/Rejected → Resolved` |
| `import_batches` chi tiết (tracking từng batch import) | Giữ tối giản: chỉ cần bảng lưu file đã import + trạng thái, không cần thống kê valid/invalid rows đầy đủ nếu thiếu thời gian |
| Audit log toàn hệ thống | Chỉ log các hành động tài chính nhạy cảm: phát hành hoá đơn, ghi nhận thanh toán, huỷ/điều chỉnh hoá đơn, chấm dứt hợp đồng |
| CI/CD, Testcontainers, observability nâng cao | Có Docker Compose + 1 pipeline build/test đơn giản là đủ; không cần Testcontainers, không cần structured logging nâng cao |
| AI "giải thích dashboard bằng ngôn ngữ tự nhiên" | Để **dự phòng tuần 5** nếu còn dư thời gian; 2 use case bắt buộc là *soạn nhắc nợ* và *tóm tắt vi phạm* |

Điều **không được cắt** (đây là xương sống của đề bài, cắt là hỏng đề): danh mục tòa/phòng/giường, đăng ký → hợp đồng → phân giường, chỉ số điện nước → tính tiền theo bậc, hóa đơn → thu phí → công nợ → biên lai, kỷ luật cơ bản, dashboard lấp đầy/doanh thu.

---

## 2. Vai trò & quyền hạn (rút gọn để code nhanh)

| Chức năng | Admin | Cán bộ KTX | Sinh viên |
|---|:---:|:---:|:---:|
| Quản lý user, cấu hình hệ thống | ✅ | ❌ | ❌ |
| Quản lý tòa/phòng/giường, loại phòng | ✅ | ✅ | Chỉ xem chỗ ở của mình |
| Duyệt đăng ký, phân giường, chuyển phòng | ✅ | ✅ | Chỉ được **tạo** đăng ký/nguyện vọng |
| Cấu hình biểu giá điện/nước | ✅ | Chỉ xem | ❌ |
| Nhập/ import chỉ số điện nước | ✅ | ✅ | ❌ |
| Phát hành hoá đơn, ghi nhận thanh toán, biên lai | ✅ | ✅ | Chỉ xem của mình |
| Ghi nhận & xử lý vi phạm | ✅ | ✅ | Chỉ xem của mình |
| Xem dashboard toàn KTX | ✅ | ✅ | ❌ |
| Dùng AI soạn nhắc nợ / tóm tắt vi phạm | ✅ | ✅ | ❌ |

Kỹ thuật: dùng **ASP.NET Core Identity** (3 role cố định), kiểm tra thêm "ownership" cho sinh viên (chỉ xem dữ liệu của chính mình) bằng policy-based authorization đơn giản, không cần hệ thống permission động.

---

## 3. Danh sách chức năng chi tiết theo module

Mỗi chức năng được mô tả theo: **Actor** (ai dùng) — **Input** — **Hệ thống làm gì** — **Output/kết quả** — **Rule quan trọng**.

### 3.1. Module Danh mục cơ sở vật chất (Housing Inventory)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F01 | Quản lý tòa nhà | Admin | Thêm/sửa/ẩn tòa nhà (mã, tên, địa chỉ, số tầng, trạng thái Active/Inactive). Không cho xoá cứng nếu đã có phòng gắn vào. |
| F02 | Quản lý loại phòng | Admin | Định nghĩa loại phòng (VD: 4 người, 6 người), giá mặc định/tháng — dùng làm giá gợi ý khi tạo hợp đồng. |
| F03 | Quản lý phòng | Admin/Staff | Thêm/sửa phòng thuộc 1 tòa, gán loại phòng, trạng thái (Available/Maintenance/Inactive). |
| F04 | Quản lý giường | Admin/Staff | Thêm/sửa giường thuộc 1 phòng. Trạng thái `Occupied` **được suy ra tự động** từ bảng phân giường đang hiệu lực, không cho sửa tay để tránh sai lệch dữ liệu. |
| F05 | Sơ đồ phòng/giường (Room matrix) | Admin/Staff | Màn hình trực quan: mỗi tòa → danh sách phòng → từng giường tô màu theo trạng thái, bấm vào xem chi tiết ai đang ở. |

### 3.2. Module Đăng ký — Hợp đồng — Phân giường (Applications, Contracts, Assignments)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F06 | Sinh viên gửi đăng ký ở KTX | Student | Chọn kỳ học, loại phòng mong muốn, thời gian dự kiến ở, ghi chú. Trạng thái ban đầu `Submitted`. |
| F07 | Cán bộ duyệt đăng ký | Staff/Admin | Xem danh sách đăng ký `Submitted`, Approve (chuyển `Approved`) hoặc Reject kèm lý do. |
| F08 | Phân giường & tạo hợp đồng | Staff/Admin | Từ đăng ký đã duyệt, chọn 1 giường còn trống → hệ thống tạo `Contract` (Active) + `BedAssignment` (start_date = hôm nay hoặc ngày chọn). **Không cho chọn giường đã có người ở trùng thời gian** (kiểm tra chồng lấp). |
| F09 | Xem hợp đồng & lịch sử ở | Student/Staff | Sinh viên xem hợp đồng hiện tại, phòng/giường đang ở. Staff xem toàn bộ lịch sử `bed_assignments` của 1 hợp đồng (phục vụ tra soát khi có tranh chấp). |
| F10 | Chuyển phòng | Staff/Admin (sinh viên gửi nguyện vọng) | Staff chọn giường mới còn trống cho sinh viên đang có hợp đồng Active. Hệ thống **trong 1 transaction**: kết thúc `bed_assignment` cũ tại ngày chuyển, tạo `bed_assignment` mới. Nếu giá phòng mới khác, tạo `bill_item` điều chỉnh có ghi chú lý do. |
| F11 | Chấm dứt hợp đồng | Staff/Admin | Kết thúc hợp đồng (hết hạn/vi phạm nặng/sinh viên xin nghỉ), đóng `bed_assignment`, giường trở lại `Available`. |

### 3.3. Module Điện nước & Tính phí (Utilities)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F12 | Cấu hình biểu giá theo bậc | Admin | Tạo `utility_tariff` (điện/nước) với các bậc giá (VD: bậc 1: 0–50kWh giá X, bậc 2: 51–100kWh giá Y...). Giá **snapshot** vào hoá đơn tại thời điểm phát hành, đổi giá sau không ảnh hưởng hoá đơn cũ. |
| F13 | Ghi chỉ số điện nước thủ công | Staff | Nhập chỉ số mới cho từng đồng hồ/phòng theo kỳ, hệ thống tự tính `consumption = current - previous`, chặn nếu current < previous. |
| F14 | Import chỉ số bằng Excel | Staff | Tải template `.xlsx` mẫu → điền chỉ số nhiều phòng → upload → hệ thống **preview** (validate: giường đúng phòng, current ≥ previous, không trùng kỳ) → Staff xem lỗi theo từng dòng → **Confirm** mới thực sự lưu. |
| F15 | Tính tiền điện nước theo bậc | Hệ thống | Áp bảng giá đang hiệu lực tại kỳ tính, cộng dồn từng bậc, tạo `bill_item` loại Electricity/Water, lưu chi tiết cách tính (snapshot) để tra soát về sau. |

### 3.4. Module Hóa đơn & Thu phí (Billing & Payments)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F16 | Phát hành hoá đơn hàng tháng | Staff/Admin | Gộp phí ở (theo hợp đồng, có prorate nếu vào ở giữa tháng) + điện + nước + phạt vi phạm (nếu có, đã confirm) thành 1 `bill` với nhiều `bill_items`. Không cho phát hành trùng 2 lần cho cùng 1 kỳ/hợp đồng (idempotent). |
| F17 | Xem hoá đơn & công nợ | Student/Staff | Sinh viên xem hoá đơn của mình, số tiền còn nợ (`balance_due`), hạn thanh toán. Staff xem danh sách công nợ toàn KTX, lọc theo quá hạn. |
| F18 | Ghi nhận thanh toán | Staff/Admin | Ghi 1 khoản thanh toán (tiền mặt/chuyển khoản) cho 1 hoá đơn — **cho phép trả nhiều lần** (partial payment). Hệ thống tự cập nhật `paid_amount`, `balance_due`, chuyển trạng thái hoá đơn (`PartiallyPaid`/`Paid`). Không cho trả vượt quá số còn nợ. |
| F19 | Xuất biên lai | Staff/Student | Sau khi thanh toán, hệ thống sinh số biên lai duy nhất, hiển thị trang in được (HTML → in PDF qua trình duyệt, chưa cần thư viện PDF riêng). |

### 3.5. Module Kỷ luật (Violations)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F20 | Ghi nhận vi phạm | Staff/Admin | Chọn sinh viên, loại vi phạm (danh mục có sẵn), thời gian/địa điểm, mô tả, mức độ. Trạng thái ban đầu `Recorded`. |
| F21 | Xác nhận/từ chối vi phạm | Staff/Admin | Chuyển `Recorded → Confirmed` hoặc `Rejected`. Chỉ khi `Confirmed` và có `fine_amount` mới sinh `bill_item` loại `ViolationFine` — **không tự động phạt tiền khi chưa xác nhận**. |
| F22 | Xem lịch sử vi phạm | Student/Staff | Sinh viên xem vi phạm của mình; Staff xem toàn bộ, có thể lọc theo mức độ/trạng thái. |

### 3.6. Module Báo cáo (Dashboard)

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F23 | Dashboard lấp đầy | Admin/Staff | Tổng số giường, số giường đang ở, tỷ lệ lấp đầy (%) toàn KTX và theo từng tòa. |
| F24 | Dashboard tài chính | Admin/Staff | Tổng tiền đã lập hoá đơn (billed) **tách riêng** khỏi tổng tiền đã thu (collected) trong kỳ, tổng công nợ, số hoá đơn quá hạn. |
| F25 | Biểu đồ theo thời gian | Admin/Staff | Biểu đồ đường/cột: doanh thu thu được theo tháng, tiêu thụ điện/nước theo kỳ. |

### 3.7. Module AI Assistant (bắt buộc tối thiểu 1–2 tính năng)

AI **không** quyết định tiền, không tự duyệt đăng ký, không tự chọn giường, không tự đổi trạng thái vi phạm. AI chỉ **soạn nội dung/tóm tắt** để người dùng đọc và tự quyết định gửi/dùng.

| # | Chức năng | Actor | Mô tả |
|---|---|---|---|
| F26 | AI soạn tin nhắn nhắc nợ | Staff | Bấm "Soạn nhắc nợ" trên 1 hoá đơn quá hạn → hệ thống gửi dữ liệu đã tính sẵn (tên SV, số hoá đơn, số tiền còn nợ, hạn) cho LLM → nhận bản nháp tiếng Việt lịch sự → Staff chỉnh sửa trước khi gửi. Luôn gắn nhãn **"Bản nháp AI"**. |
| F27 | AI tóm tắt lịch sử vi phạm | Staff | Trên trang chi tiết sinh viên, bấm "Tóm tắt bằng AI" → hệ thống lấy danh sách vi phạm, gửi LLM tóm tắt thành 1 đoạn ngắn giúp Staff đọc nhanh. |
| F28 *(tuỳ chọn nếu dư thời gian)* | AI diễn giải dashboard | Admin | Backend tính sẵn KPI bằng SQL, gửi các con số tổng hợp cho LLM để sinh 1 đoạn nhận xét ngôn ngữ tự nhiên. Không cho LLM truy vấn DB trực tiếp. |

Yêu cầu kỹ thuật tối thiểu cho AI: 1 interface `ILlmClient` gọi 1 nhà cung cấp (VD OpenAI), có timeout, giới hạn độ dài input, không log dữ liệu nhạy cảm, và **nếu AI lỗi/timeout thì các chức năng khác của hệ thống vẫn hoạt động bình thường** (trả lỗi `AI_PROVIDER_UNAVAILABLE`, không làm sập luồng billing/contract).

---

## 4. Business rule bắt buộc phải đúng (dù MVP)

1. Không được gán 2 sinh viên vào cùng 1 giường trong cùng khoảng thời gian (chống double-booking).
2. Giá điện/nước, giá phòng dùng để tính hoá đơn phải **snapshot** tại thời điểm phát hành — sửa bảng giá sau không được đổi hoá đơn cũ.
3. Thanh toán không xoá hoá đơn, chỉ giảm `balance_due` và đổi trạng thái.
4. Vi phạm chỉ tạo nghĩa vụ tài chính khi đã **Confirmed**.
5. Không phát hành trùng 2 hoá đơn cho cùng kỳ + cùng hợp đồng.
6. Không hard-delete dữ liệu đã phát sinh nghiệp vụ (building/room/bed có hợp đồng, hoá đơn đã issue, thanh toán đã ghi) — chỉ đổi trạng thái/huỷ có lý do.
7. Sinh viên chỉ được xem dữ liệu của chính mình (hợp đồng, hoá đơn, vi phạm).

---

## 5. Lộ trình 5 tuần (bám sát để kịp deadline)

> Giả định nhóm 2–4 người, làm song song Backend/Frontend. Mỗi tuần kết thúc bằng 1 **demo được** (không phải chỉ code xong, chưa chạy).

### Tuần 1 — Nền tảng + Danh mục cơ sở vật chất
- Khởi tạo repo, Docker Compose (PostgreSQL), solution backend, EF Core migration đầu tiên.
- ASP.NET Core Identity: 3 role, đăng nhập/đăng xuất, seed 1 tài khoản mỗi role.
- CRUD F01–F05 (tòa/phòng/giường/loại phòng + room matrix).
- Khung React: layout Admin/Staff, layout Student, routing theo role, trang login.
- **Demo cuối tuần:** đăng nhập 3 role, tạo được tòa → phòng → giường, thấy sơ đồ giường trống/đã ở.

### Tuần 2 — Đăng ký → Hợp đồng → Phân giường → Chuyển phòng
- F06–F11: đăng ký, duyệt, phân giường, chống chồng lấp giường, chấm dứt hợp đồng.
- Chuyển phòng (F10) — chỉ cần bản đơn giản (Staff thao tác trực tiếp) trong tuần này.
- Frontend: form đăng ký (Student), danh sách chờ duyệt + thao tác duyệt/phân giường (Staff), trang "chỗ ở của tôi" (Student).
- **Demo cuối tuần:** 1 sinh viên đăng ký → được duyệt → có hợp đồng active → chuyển sang giường khác, lịch sử vẫn còn.

### Tuần 3 — Điện nước & Tính hoá đơn
- F12–F15: biểu giá theo bậc, nhập tay chỉ số, import Excel (preview/confirm), tính tiền theo bậc.
- F16: phát hành hoá đơn (phí ở + điện + nước), đảm bảo idempotent.
- Unit test riêng cho bộ tính tiền theo bậc (đây là phần dễ sai nhất, nên test kỹ).
- **Demo cuối tuần:** tải template Excel → điền số liệu → import → hệ thống ra đúng hoá đơn có điện/nước tính theo bậc.

### Tuần 4 — Thu phí, Công nợ, Kỷ luật
- F17–F19: xem hoá đơn/công nợ, ghi nhận thanh toán (kể cả trả nhiều lần), xuất biên lai in được.
- F20–F22: ghi nhận, xác nhận, xem lịch sử vi phạm; phạt tiền tạo bill item khi confirm.
- **Demo cuối tuần:** từ 1 hoá đơn, trả 2 lần cho hết nợ, in biên lai; ghi 1 vi phạm có phạt tiền, xác nhận và thấy khoản phạt lên hoá đơn kỳ sau.

### Tuần 5 — Báo cáo, AI, Hoàn thiện & Demo
- F23–F25: dashboard lấp đầy + tài chính + biểu đồ.
- F26–F27 (F28 nếu dư thời gian): tích hợp `ILlmClient`, 2 endpoint AI, gắn nhãn "Bản nháp AI", xử lý khi AI lỗi.
- Áp bộ màu/giao diện theo Mục 6 lên toàn bộ trang đã làm ở 4 tuần trước.
- Rà lại RBAC (sinh viên không xem được dữ liệu người khác), test lại toàn bộ luồng chính đầu-cuối, chuẩn bị kịch bản demo + dữ liệu mẫu.
- **Demo cuối tuần = demo cuối kỳ:** chạy trọn luồng đăng ký–ở–điện nước–hoá đơn–thu phí–vi phạm–dashboard–AI trong một lượt liền mạch.

### Nếu tuần nào bị trễ, ưu tiên cắt theo thứ tự sau (từ dễ cắt nhất)
1. F28 (AI giải thích dashboard).
2. Biểu đồ xu hướng theo thời gian (F25) — giữ lại số liệu dạng bảng/KPI card là đủ.
3. Luồng "sinh viên gửi yêu cầu chuyển phòng" 2 bước — giữ bản Staff thao tác trực tiếp.
4. Trang in biên lai đẹp — giữ bản hiển thị thông tin tối thiểu, không cần layout công phu.

**Tuyệt đối không cắt:** F08 (phân giường + chống double-booking), F15–F16 (tính tiền + phát hành hoá đơn), F18 (thanh toán), vì đây là các chức năng đề bài chấm trực tiếp.

---

## 6. Thiết kế giao diện & Bộ màu (Design System)

> Phần này **chưa có trong bản phân tích gốc** — bổ sung để đảm bảo giao diện chuyên nghiệp, tông sáng, dễ chịu, nhất quán giữa các trang.

### 6.1. Nguyên tắc thiết kế

- **Sáng, thoáng, ít chi tiết thừa**: nền tổng thể màu xám rất nhạt, card nền trắng, nhiều khoảng trắng (whitespace) — tránh cảm giác "bảng tính chằng chịt".
- **Một màu chủ đạo duy nhất** cho hành động chính (nút, link, trạng thái active) để tránh loạn màu.
- **Màu ngữ nghĩa (semantic color)** chỉ dùng cho trạng thái nghiệp vụ (thành công/cảnh báo/lỗi/thông tin), không dùng tuỳ tiện cho trang trí.
- **Bo góc mềm (8–12px)** và **đổ bóng rất nhẹ** cho card/nút để tạo cảm giác thân thiện, phù hợp cả sinh viên lẫn cán bộ hành chính.
- Không dùng đen tuyệt đối (`#000000`) cho chữ — dùng xám than để dịu mắt hơn.

### 6.2. Bảng màu chính

| Nhóm | Tên token | Mã màu | Dùng ở đâu |
|---|---|---|---|
| **Primary** (thương hiệu, hành động chính) | primary-50 | `#EFF4FF` | nền hover, nền item menu đang chọn |
| | primary-100 | `#DCE7FF` | nền badge nhẹ liên quan primary |
| | primary-500 | `#4C7DF0` | icon, border nhấn |
| | **primary-600** | **`#2F6FED`** | nút chính, link, active nav, focus ring |
| | primary-700 | `#1E54C9` | trạng thái hover/pressed của nút chính |
| **Accent** (điểm nhấn phụ, dùng nhiều ở Student Portal cho gần gũi) | accent-50 | `#ECFDF9` | nền card "chỗ ở hiện tại" |
| | **accent-500** | **`#14B8A6`** | icon phụ, số liệu nổi bật không mang tính cảnh báo |
| **Nền & bề mặt** | bg-app | `#F7F9FC` | nền toàn trang (rất sáng, không chói) |
| | bg-surface | `#FFFFFF` | card, bảng, modal, form |
| | border | `#E4E7EC` | viền input, viền bảng, chia section |
| **Chữ** | text-primary | `#1F2937` | tiêu đề, nội dung chính |
| | text-secondary | `#6B7280` | chú thích, nhãn phụ |
| | text-disabled | `#9CA3AF` | trạng thái vô hiệu hoá |

### 6.3. Bảng màu trạng thái (semantic) — áp cho badge/tag trạng thái

| Ý nghĩa | Màu chữ | Màu nền badge | Dùng cho trạng thái |
|---|---|---|---|
| **Thành công / Hoàn tất** | `#16A34A` | `#ECFDF3` | `Paid`, `Active`, `Approved`, `Available`, `Resolved` |
| **Cảnh báo / Đang chờ** | `#D97706` | `#FFFBEB` | `Pending`, `Submitted`, `PartiallyPaid`, `Reserved`, `UnderReview` |
| **Lỗi / Cần chú ý** | `#DC2626` | `#FEF2F2` | `Overdue`, `Rejected`, `Confirmed` (vi phạm), `Maintenance` |
| **Thông tin / Trung tính mới** | `#0EA5E9` | `#F0F9FF` | `Draft`, đang import, thông báo hệ thống |
| **Không hoạt động** | `#6B7280` | `#F3F4F6` | `Inactive`, `Cancelled`, `Terminated` |

> Nguyên tắc: mỗi badge **luôn có chữ kèm theo**, không chỉ dựa vào màu (để không phụ thuộc khả năng phân biệt màu sắc của người xem).

### 6.4. Typography

- Font chữ: **Be Vietnam Pro** (hỗ trợ dấu tiếng Việt tốt, trông hiện đại, chuyên nghiệp) cho toàn bộ hệ thống — cả tiêu đề lẫn nội dung, chỉ đổi độ đậm (weight).
- Thang cỡ chữ: `12 / 14 / 16 / 20 / 24 / 30 px`.
- Trọng lượng: `400` cho nội dung thường, `500` cho label/nhãn, `600` cho tiêu đề mục, `700` cho tiêu đề trang/số liệu KPI lớn.

### 6.5. Bố cục tổng quan

**Admin/Staff Portal**
- Sidebar trắng bên trái, item đang chọn có **thanh accent primary-600 bên trái + nền primary-50**, icon/label màu primary-600.
- Topbar trắng: tên hệ thống, avatar, vai trò, chuông thông báo.
- Vùng nội dung nền `bg-app` (#F7F9FC), các khối chức năng đặt trong card nền trắng bo góc 12px.
- Dashboard: KPI card hàng đầu (4 card: tổng giường, đang ở, tỷ lệ lấp đầy, công nợ) — icon tròn nền màu nhạt tương ứng ngữ nghĩa; biểu đồ bên dưới.

**Student Portal**
- Bố cục đơn giản hơn, ít menu, tập trung 4 mục: Chỗ ở hiện tại, Hoá đơn, Vi phạm, Đăng ký/chuyển phòng.
- Dùng thêm **accent-500 (teal)** cho card "chỗ ở hiện tại" để tạo cảm giác thân thiện, khác biệt nhẹ so với các trang quản trị.

### 6.6. Hướng dẫn thành phần (component)

- **Nút chính (Primary button)**: nền `primary-600`, chữ trắng, bo góc 8px, hover đổi `primary-700`.
- **Nút phụ (Secondary/outline)**: nền trắng, viền `primary-600`, chữ `primary-600`.
- **Nút nguy hiểm (Danger)**: chỉ dùng cho hành động huỷ/chấm dứt, nền `#DC2626`, cần có bước xác nhận (confirm dialog) trước khi thực thi.
- **Bảng dữ liệu**: header nền `bg-app`, chữ đậm `text-primary`; hover dòng nền `primary-50`; border mỏng `#E4E7EC`, không cần zebra-stripe.
- **Form**: input viền `border` mặc định, khi focus viền `primary-600` kèm ring nhạt `primary-100`; báo lỗi validate dùng chữ/viền `#DC2626`.
- **Badge/Tag trạng thái**: bo góc pill (999px), theo bảng màu Mục 6.3.
- **AI content**: mọi nội dung do AI sinh ra bọc trong khung có nhãn nhỏ "Bản nháp AI" nền `accent-50`, viền đứt nhẹ `accent-500`, để người dùng luôn phân biệt được với dữ liệu hệ thống.

### 6.7. Cấu hình nhanh cho Ant Design (React)

```ts
// src/web/src/app/theme.ts
export const themeTokens = {
  token: {
    colorPrimary: '#2F6FED',
    colorSuccess: '#16A34A',
    colorWarning: '#D97706',
    colorError: '#DC2626',
    colorInfo: '#0EA5E9',
    colorTextBase: '#1F2937',
    colorTextSecondary: '#6B7280',
    colorBgLayout: '#F7F9FC',
    colorBgContainer: '#FFFFFF',
    colorBorder: '#E4E7EC',
    borderRadius: 8,
    borderRadiusLG: 12,
    fontFamily: "'Be Vietnam Pro', -apple-system, sans-serif",
  },
};
```

Dùng trực tiếp trong `<ConfigProvider theme={themeTokens}>` bọc ngoài App — mọi component AntD (Button, Table, Tag, Card, Form) tự động đồng bộ theo bộ màu này, không cần override từng nơi.

### 6.8. Kiểm tra khả năng tiếp cận (accessibility) tối thiểu

- Độ tương phản chữ/nền chính đạt tối thiểu **4.5:1** (primary-600 trên nền trắng ≈ đạt chuẩn AA cho text thường).
- Không truyền tải thông tin **chỉ bằng màu** — luôn kèm chữ hoặc icon (áp dụng cho mọi badge trạng thái ở Mục 6.3).
- Kích thước chữ tối thiểu 14px cho nội dung thao tác, 12px chỉ dùng cho chú thích phụ.

---

## 7. Checklist nghiệm thu MVP (rút gọn, dùng để tự chấm trước khi nộp)

```text
[ ] Đăng nhập đúng theo 3 vai trò, phân quyền đúng (sinh viên không xem được dữ liệu người khác)
[ ] Tạo được tòa → phòng → giường, thấy sơ đồ trạng thái giường
[ ] Sinh viên đăng ký ở → Staff duyệt → phân giường → hợp đồng Active
[ ] Chuyển phòng: giường cũ trống lại, giường mới có người, lịch sử vẫn còn
[ ] Tải template Excel, nhập chỉ số, import (có preview lỗi), confirm
[ ] Tính tiền điện/nước đúng theo bậc giá đã cấu hình
[ ] Phát hành hoá đơn gồm phí ở + điện + nước, không phát hành trùng kỳ
[ ] Thanh toán một phần → còn nợ đúng số; thanh toán đủ → hết nợ, có biên lai
[ ] Ghi nhận vi phạm → xác nhận → (nếu có phạt) khoản phạt lên hoá đơn kỳ sau
[ ] Dashboard: tỷ lệ lấp đầy đúng, tổng đã lập hoá đơn khác tổng đã thu
[ ] AI soạn được 1 bản nháp nhắc nợ, có nhãn "Bản nháp AI"
[ ] AI tóm tắt được lịch sử vi phạm 1 sinh viên
[ ] Khi AI lỗi/timeout, các chức năng khác vẫn chạy bình thường
[ ] Giao diện dùng nhất quán bộ màu ở Mục 6, không lẫn nhiều theme/màu tuỳ tiện
```
