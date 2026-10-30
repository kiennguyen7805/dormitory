# Chạy nhanh Postman

Dùng **Dormitory_MasterPlan_8Tuan.postman_collection.json** — collection chính đủ tuần 1–8.

1. Bật Docker Desktop và chạy `docker compose up -d --build` tại thư mục gốc.
2. Kiểm tra <http://localhost:8081/readyz> trả `ready`.
3. Postman → **Import → Files** → chọn file JSON trên.
4. Chọn **No Environment** → mở **Dormitory MVP - Master Plan 8 tuần**.
5. Mở một tuần → bấm đúp request → **Send** → xem **Test Results**.

Token, mã và ID tự được chuẩn bị. Có thể mở bất kỳ request ở bất kỳ tuần nào mà không chạy tuần trước. Mỗi Send có thể tạo dữ liệu demo mới.

Muốn chạy cả bộ: **Run collection → Iterations 1 → Delay 250–300 ms**. Ca lỗi 4xx cũng phải có Test Results xanh khi phản hồi đúng dự kiến.

Nếu mở dự án bằng Local View, chọn collection cùng tên trong `postman/collections/`.

Chi tiết cấu hình, xử lý lỗi và phạm vi kiểm thử: [README.md](README.md).

