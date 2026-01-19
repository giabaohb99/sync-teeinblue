# Teeinblue Integration (FastAPI + ORM)

## 1. Project Setup
- [x] **Dependencies**: `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `psycopg2-binary`, `requests`, `python-dotenv`.
- [x] **Structure**: Standard FastAPI layout (`app/` folder, `models`, `schemas`, `crud`).
- [x] **Environment**: `.env` for DB credentials and API Keys.

## 2. Database Design (PostgreSQL + SQLAlchemy)
- [x] **Schema Definition**:
    -   **Table**: `orders`
    -   **Columns**:
        -   `id` (String, PK): Teeinblue Order ID.
        -   `ref_id` (String, Index): Readable Order Number (e.g., #1001).
        -   `status` (String): Current status (e.g., "Ready To Fulfill").
        -   `customer_info` (JSON): Name, Address, etc.
        -   `line_items` (JSON): Item details.
        -   `print_url` (String, Nullable): URL to the print file.
        -   `synced_at` (DateTime): Last sync time.
- [x] **Migration System**: Initialize `alembic` to handle schema changes.
- [x] **Auto-Creation**: Ensure tables are created on startup if they don't exist.

## 3. Teeinblue Client (Service Layer)
- [x] **API Interaction**:
    -   `fetch_orders(status_id)`: Get list of orders.
    -   `get_order_details(order_id)`: Get full payload.

## 4. Business Logic (CRUD)
- [x] **Upsert Logic**: Check if order exists. If yes, update details; if no, create new record.
- [x] **Sync Process**: Background task to:
    1.  Poll Teeinblue.
    2.  Process & Map data.
    3.  Save to DB.

## 5. API Endpoints
- [x] `GET /orders`: List synced orders.
- [x] `POST /sync`: Trigger manual sync.
- [x] `GET /health`: Health check.

## 6. Deployment
- [x] **Docker**: Dockerfile for the API.
- [x] **Compose**: Service definition including Database connection.
