# Kết quả kiểm thử Postman

Kiểm tra ngày 30/10/2026 trên API Docker local qua gateway http://localhost:8081.

| Kiểm tra | Kết quả |
|---|---|
| Toàn bộ collection JSON bằng Newman 6 | 75/75 request chính, 173/173 assertions đạt, không lỗi script |
| HTTP gồm cả bước chuẩn bị | 504 lời gọi, không lỗi truyền tải |
| Mở riêng request cuối tuần 8, không chạy các tuần trước | Đạt |
| Chạy riêng request đó 2 lần | Đạt; tạo 2 hóa đơn với ID khác nhau |
| Environment chứa URL, token và ID cũ/sai | Đạt; cấu hình collection được dùng đúng |
| Sai mật khẩu Admin trong khâu chuẩn bị | Đạt; báo test thất bại, chỉ gửi bước login, không gửi request hóa đơn chính |
| JSON và YAML Local View | Đủ 75 request; URL, method, body, auth, code test và thứ tự khớp |
| Cú pháp JavaScript | Script collection và tất cả post-response hợp lệ |

Đã build và chạy API, PostgreSQL, gateway, Adminer. Các lần kiểm thử thêm dữ liệu demo vào database local; không xóa dữ liệu có sẵn.

Bản JSON được chạy bằng Newman; bản YAML được kiểm tra đối chiếu nội dung, chưa kiểm tra giao diện Postman trực tiếp. Không đưa báo cáo Newman thô vào đây vì báo cáo có thể chứa token và dữ liệu đăng nhập.
