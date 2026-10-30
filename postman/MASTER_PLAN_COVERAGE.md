# Đối chiếu Master Plan và Postman

Sinh tự động từ sheet Plan; không sửa workbook.

| Tuần | STT | Công việc trong Plan | Ô nguồn | Số request |
|---|---:|---|---|---:|
| 1 | 1 | Chạy FastAPI, PostgreSQL, Docker Compose và Alembic | Plan!B4 | 2 |
| 1 | 2 | Giữ đúng ba vai trò Admin, Staff, Student; đăng nhập, đăng ký và phân quyền | Plan!B5 | 14 |
| 1 | 3 | Admin tạo tòa; Admin/Staff tạo phòng với sức chứa và giá ở | Plan!B6 | 2 |
| 1 | 4 | Phòng tự tạo vị trí ở và công tơ điện/nước; sinh viên xem danh sách phòng | Plan!B7 | 3 |
| 2 | 5 | Sinh viên chọn phòng, gửi đăng ký theo kỳ và theo dõi trạng thái | Plan!B9 | 2 |
| 2 | 6 | Staff/Admin duyệt hoặc từ chối đăng ký, có lý do từ chối | Plan!B10 | 2 |
| 2 | 7 | Staff/Admin lập hợp đồng gắn phòng đã đăng ký; kiểm tra chỗ trống | Plan!B11 | 1 |
| 2 | 8 | Sinh viên xem hợp đồng; Staff/Admin có thể chấm dứt hợp đồng | Plan!B12 | 3 |
| 3 | 9 | Duy trì hai tiện ích điện và nước; mỗi phòng có một công tơ cho từng loại | Plan!B14 | 2 |
| 3 | 10 | Staff/Admin thiết lập biểu giá và nhập chỉ số theo kỳ cho phòng | Plan!B15 | 4 |
| 3 | 11 | Chặn chỉ số giảm và chỉ số trùng công tơ/kỳ | Plan!B16 | 2 |
| 3 | 12 | Kiểm tra tiền điện, nước và snapshot giá sau khi ghi chỉ số | Plan!B17 | 1 |
| 4 | 13 | Chỉ phát hành khi phòng đủ chỉ số điện và nước của cùng kỳ | Plan!B19 | 1 |
| 4 | 14 | Phát đúng một hóa đơn cho phòng/kỳ, gồm hai dòng điện và nước | Plan!B20 | 1 |
| 4 | 15 | Sinh viên từng ở phòng trong kỳ xem chung hóa đơn phòng | Plan!B21 | 2 |
| 4 | 16 | Chặn phát hành trùng và kiểm tra khóa idempotency | Plan!B22 | 3 |
| 5 | 17 | Staff/Admin xác nhận hóa đơn phòng đã thanh toán đủ | Plan!B24 | 1 |
| 5 | 18 | Lưu phương thức, mã tham chiếu, người và thời điểm xác nhận | Plan!B25 | 1 |
| 5 | 19 | Chặn xác nhận thanh toán lại; sinh viên xem trạng thái đã trả | Plan!B26 | 2 |
| 5 | 20 | Đối chiếu tổng tiền hóa đơn với hai dòng điện và nước | Plan!B27 | 1 |
| 6 | 21 | Kiểm thử hai sinh viên cùng phòng chỉ nhận một hóa đơn chung | Plan!B29 | 1 |
| 6 | 22 | Kiểm thử phòng đủ/chật, đơn chưa duyệt và hợp đồng trùng | Plan!B30 | 3 |
| 6 | 23 | Kiểm thử quyền Admin, Staff, Student trên các API chính | Plan!B31 | 7 |
| 6 | 24 | Kiểm thử lỗi chỉ số, hóa đơn thiếu dữ liệu và thanh toán lặp | Plan!B32 | 4 |
| 7 | 25 | Cập nhật OpenAPI/Swagger cho API MVP; bỏ sơ đồ, chuyển phòng và giường công khai | Plan!B34 | 2 |
| 7 | 26 | Cập nhật Postman Collection cho luồng đăng ký đến thanh toán | Plan!B35 | 1 |
| 7 | 27 | Ghi ví dụ request/response, mã lỗi và cách chạy dữ liệu demo | Plan!B36 | 1 |
| 7 | 28 | Rà lại ba vai trò và endpoint theo checklist | Plan!B37 | 1 |
| 8 | 29 | Build và chạy API, PostgreSQL, Adminer bằng Docker Compose | Plan!B39 | 1 |
| 8 | 30 | Chạy migration và kiểm tra /readyz, Swagger trên môi trường demo | Plan!B40 | 2 |
| 8 | 31 | Dùng database mẫu, kiểm thử đầu cuối và lưu hướng dẫn chạy | Plan!B41 | 1 |
| 8 | 32 | Demo: sinh viên đăng ký → cán bộ duyệt → hợp đồng phòng → chỉ số → hóa đơn phòng → trả đủ | Plan!B42 | 1 |

Các mục tài liệu/build Docker được kiểm tra bằng HTTP và luồng E2E; Postman không thực hiện build Docker hoặc sửa tài liệu.
Checklist Excel còn POST /api/v1/auth/logout nhưng backend hiện tại đã bỏ API này; không tạo request giả.
BillRead trả phương thức, tham chiếu và thời điểm thanh toán; người xác nhận lưu nội bộ, không có trường public để assert qua API.
