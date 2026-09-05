# Dormitory UI — Hệ thống Quản lý Ký túc xá

Bản prototype frontend cho MVP quản lý ký túc xá. Giao diện hiện dùng HTML, CSS và JavaScript thuần với dữ liệu mẫu; cấu trúc mã được chia theo **feature nghiệp vụ** để bám sát modular monolith trong tài liệu và thuận tiện chuyển dần sang React + TypeScript.

## Chạy dự án

Không cần cài dependency hoặc build. Mở `index.html` bằng trình duyệt, chọn vai trò **Admin / Cán bộ / Sinh viên**, sau đó bấm **Đăng nhập**.

Ứng dụng cần Internet để tải font Be Vietnam Pro và Chart.js từ CDN. Khi offline, các trang vẫn hiển thị bằng font hệ thống nhưng biểu đồ không được tải.

## Cấu trúc thư mục

```text
dormitory-ui/
├── docs/                              # Phân tích MVP và kiến trúc mục tiêu
│   ├── 01-phan-tich-bai-toan-mvp.md
│   └── 02-cau-truc-du-an.md
├── src/
│   ├── features/                      # Trang và logic được nhóm theo nghiệp vụ
│   │   ├── auth/                      # Đăng nhập và chọn vai trò demo
│   │   ├── dashboard/                 # Dashboard Admin và Student
│   │   ├── housing/                   # Tòa, phòng, giường, room matrix
│   │   ├── applications/              # Đăng ký, duyệt, nguyện vọng chuyển phòng
│   │   ├── contracts/                 # Hợp đồng, phân giường, chuyển phòng
│   │   ├── utilities/                 # Chỉ số và biểu giá điện nước
│   │   ├── billing/                   # Hóa đơn, thanh toán, công nợ
│   │   ├── violations/                # Ghi nhận và theo dõi vi phạm
│   │   └── ai/                        # Nhắc nợ và nội dung do AI soạn
│   └── shared/                        # Tài nguyên dùng chung giữa các feature
│       ├── scripts/
│       │   ├── app.js                 # Modal, tab, toast, format, badge
│       │   ├── layout.js              # Sidebar, topbar và điều hướng theo role
│       │   └── mock-data.js           # Dữ liệu demo tập trung
│       └── styles/
│           └── design-system.css      # Token và component giao diện dùng chung
├── index.html                         # Entry point / màn hình đăng nhập
└── README.md
```

## Ánh xạ màn hình theo module

| Module | Màn hình quản trị/cán bộ | Màn hình sinh viên | Chức năng MVP |
|---|---|---|---|
| Dashboard | `dashboard/admin-dashboard.html` | `dashboard/student-dashboard.html` | F23–F25, tổng quan chỗ ở |
| Housing | `housing/room-matrix.html` | — | F01–F05 |
| Applications | `applications/application-management.html` | `applications/student-application.html` | F06–F08, nguyện vọng chuyển phòng |
| Contracts | `contracts/contract-management.html` | Hiển thị trong dashboard | F09–F11 |
| Utilities | `utilities/utility-management.html` | — | F12–F15 |
| Billing | `billing/billing-management.html` | `billing/student-bills.html` | F16–F19 |
| Violations | `violations/violation-management.html` | `violations/student-violations.html` | F20–F22, F27 |
| AI | `ai/ai-assistant.html` | — | F26 |

Tất cả đường dẫn trong bảng bắt đầu từ `src/features/`.

## Nguyên tắc tổ chức

- `features/` sở hữu màn hình và logic riêng của từng nghiệp vụ; không đặt mã dùng chung vào một feature tùy ý.
- `shared/` chỉ chứa thành phần thực sự được nhiều feature sử dụng như layout, design system, định dạng và dữ liệu demo.
- Tên trạng thái trong JavaScript dùng tiếng Anh (`Approved`, `PartiallyPaid`); nhãn tiếng Việt được ánh xạ ở tầng giao diện.
- Mỗi feature tương ứng trực tiếp với module backend dự kiến trong `Dormitory.Application`, giúp thay mock data bằng API theo từng module mà không phải sửa toàn bộ dự án.
- Khi chuyển sang React/Vite, giữ nguyên ranh giới feature này và thay từng trang HTML bằng component/route trong chính thư mục feature tương ứng.

## Tài liệu nền

- [Phân tích bài toán MVP](docs/01-phan-tich-bai-toan-mvp.md)
- [Kiến trúc và cấu trúc dự án mục tiêu](docs/02-cau-truc-du-an.md)

## Phạm vi hiện tại

Đây là prototype giao diện, chưa kết nối API thật. Các nút nghiệp vụ đang mô phỏng bằng toast và dữ liệu trong `src/shared/scripts/mock-data.js`. Backend ASP.NET Core, PostgreSQL, xác thực thật, kiểm tra quyền sở hữu dữ liệu và các business rule tài chính vẫn cần được triển khai theo tài liệu trong `docs/`.
