# Repositories

Mỗi repository trong thư mục này chỉ gọi PostgreSQL stored function có tiền tố
`fn_`. Repository không viết `SELECT ... FROM <table>`, `INSERT`, `UPDATE` hoặc
`DELETE` trực tiếp lên bảng nghiệp vụ.

Luồng thực thi:

```text
FastAPI controller
  -> Application service
  -> Stored*Repository
  -> SELECT public.fn_*(tham số)
  -> PostgreSQL
```

- `auth.py`, `identity.py`, `students.py`: tài khoản và hồ sơ.
- `housing.py`: facade nghiệp vụ cơ sở vật chất; tách đọc/ghi ở `housing_*`.
- `contracts.py`: facade đơn đăng ký/hợp đồng; tách đọc/ghi ở `contract_*`.
- `utilities.py`: công tơ, biểu giá và chỉ số nhập thủ công.
- `billing.py`: truy vấn và sinh hóa đơn.

SQL định nghĩa function nằm trong `../sql/`. Migration cài function vào database.
`sqlalchemy.text()` ở đây chỉ bọc câu gọi function và bind parameter, không phải
ORM hay truy vấn bảng trực tiếp.
