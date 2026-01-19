# Teeinblue Order Sync Service

Hệ thống đồng bộ đơn hàng tự động từ Teeinblue về Database nội bộ (PostgreSQL) sử dụng FastAPI, SQLAlchemy và Docker.

## 1. Cấu trúc Dự án

```
teeinblue/
├── app/
│   ├── main.py        # Entry point, API routes
│   ├── services.py    # Logic nghiệp vụ (Sync, Bot)
│   ├── scheduler.py   # Cấu hình APScheduler (Hẹn giờ chạy Bot)
│   ├── client.py      # Giao tiếp với API Teeinblue
│   ├── models.py      # Định nghĩa DB Models (SQLAlchemy)
│   └── ...
├── alembic/           # Quản lý Migrations (thay đổi cấu trúc DB)
├── docker-compose.yml # Cấu hình chạy Docker
└── .env               # Cấu hình môi trường (API Key, DB URL)
```

## 2. Cài đặt và Chạy

### Yêu cầu
*   Docker & Docker Compose

### Bước 1: Cấu hình
Tạo file `.env` từ file mẫu (hoặc điền thông tin):
```env
TEEINBLUE_API_KEY=your_teeinblue_api_key
TEEINBLUE_API_URL=https://api.teeinblue.com/openapi/v1
DB_HOST=192.168.1.12
DB_PORT=5432
DB_NAME=teeinblue
DB_USER=your_user
DB_PASSWORD=your_password
REDIS_URL=redis://:your_password@host:port/0
```

### Bước 2: Khởi chạy
Chạy lệnh sau để build và start service:
```bash
docker-compose up -d --build
```
Dịch vụ sẽ chạy tại `http://localhost:8005`.

## 3. Logic Hoạt Động (Scheduler)

Hệ thống có 2 Bot chạy ngầm:

1.  **Quick Sync (24h qua)**
    *   **Tần suất**: 1 phút/lần.
    *   **Phạm vi**: Quét các đơn từ `00:00 hôm nay` đến `hiện tại`.
    *   **Mục đích**: Bắt đơn hàng mới nhất gần như realtime.

2.  **Deep Sync (7 ngày qua)**
    *   **Tần suất**: 60 phút/lần.
    *   **Phạm vi**: Quét từ `00:00 ngày cách đây 7 ngày` đến `23:59 ngày hôm qua`.
    *   **Mục đích**: Rà soát, cập nhật các đơn cũ bị sót hoặc thay đổi trạng thái trong tuần.

**Điều kiện dừng (Pagination)**:
*   Mỗi lần quét sẽ lặp qua các trang (Page 1, 2, 3...) mỗi trang 25 đơn.
*   Dừng khi: API trả về rỗng HOẶC đến trang cuối cùng HOẶC vượt quá giới hạn an toàn (50 trang).

## 4. API Endpoints

Bạn có thể thao tác qua Swagger UI tại: `http://localhost:8005/docs`

*   `GET /orders`: Xem danh sách đơn đã đồng bộ.
*   `POST /sync`: Kích hoạt đồng bộ thủ công ngay lập tức.
    *   Input JSON (Tùy chọn):
        ```json
        { "option": "7d" }
        // Hoặc
        { "days_start": 30, "days_end": 0 }
        ```

## 5. Quản lý Database (Alembic Migrations)

Khi bạn sửa file `app/models.py` (ví dụ thêm/sửa cột), bạn cần tạo migration để cập nhật DB mà không mất dữ liệu.

### Bước 1: Tạo file migration
Chạy lệnh sau (thay `mesage` bằng mô tả của bạn):
```bash
docker-compose exec teeinblue-api alembic revision --autogenerate -m "Mo ta thay doi"
```
*Lệnh này sẽ tạo ra 1 file mới trong thư mục `alembic/versions/`.*

### Bước 2: Áp dụng lên DB
Chạy lệnh sau để thực thi thay đổi:
```bash
docker-compose exec teeinblue-api alembic upgrade head
```

### Lưu ý quan trọng
*   Nếu không chạy migration sau khi sửa code Model, Service sẽ bị lỗi vì code Python và DB thực tế không khớp nhau.
*   Nếu muốn tạo lại từ đầu (xóa sạch dữ liệu), có thể dùng `docker-compose down -v`.
