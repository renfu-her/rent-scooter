# Flask Rent Scooter Management System

機車租借管理系統 - 使用 Flask MVC 架構開發

## 技術棧

- Python 3.12+
- Flask 3.x
- SQLAlchemy (ORM)
- MySQL
- Alembic (資料庫遷移)
- Pillow (圖片處理)
- Flask-Login (認證)
- UV (套件管理)

## 專案結構

```
rent-scooter/
├── app/
│   ├── models/          # 資料模型
│   ├── controllers/      # 業務邏輯控制器
│   ├── views/           # 路由視圖
│   │   ├── api/        # REST API
│   │   └── admin/       # 管理後台
│   ├── utils/           # 工具函數
│   └── templates/       # Jinja2 模板
├── static/              # 靜態檔案 (CSS, JS, images)
├── migrations/          # Alembic 遷移檔案
├── uploads/            # 上傳的圖片
└── run.py              # 應用程式入口
```

## 安裝步驟

### 1. 確保已安裝 MySQL

建立資料庫：
```sql
CREATE DATABASE `rent-scooter` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 安裝依賴

```bash
uv sync
```

### 3. 設定環境變數

複製 `.env.example` 為 `.env` 並編輯：

**Windows:**
```powershell
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

編輯 `.env` 檔案，設定您的資料庫連線：
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost/rent-scooter
SECRET_KEY=your-secret-key-here
```

**注意：** 如果沒有 `.env` 檔案，系統會使用預設值（無密碼的 root 使用者）。

### 4. 初始化資料庫

```bash
uv run python init_db.py
```

這會建立所有資料表並建立預設管理員帳號：
- 使用者名稱: `admin`
- 密碼: `admin123`

**重要：請在生產環境中更改預設密碼！**

### 5. 執行應用程式

```bash
uv run python run.py
```

應用程式將在 `http://localhost:5000` 啟動

## 功能說明

### 認證系統
- 使用者類型：admin, customer, store_admin
- 登入/登出功能
- 基於角色的權限控制

### 合作商管理
- CRUD 操作
- 合作商名稱、地址、統編

### 商店管理
- CRUD 操作
- 商店名稱、地址、電話

### 機車管理
- CRUD 操作
- 圖片上傳（自動轉換為 WebP）
- 顏色選擇（黑/白）
- 車款類型（白牌/綠牌/電輔車）
- 狀態管理（待出租/出租中/維修中）

### 訂單管理
- 建立訂單（多選機車）
- 車牌號碼搜尋
- 機車型號統計
- 所有選填欄位支援

### Banner 管理
- CRUD 操作
- 圖片上傳（自動轉換為 WebP）
- 顯示順序控制

## API 端點

所有 API 端點都需要認證，位於 `/api/` 路徑下：
- `/api/partners` - 合作商 API
- `/api/stores` - 商店 API
- `/api/motorcycles` - 機車 API
- `/api/orders` - 訂單 API
- `/api/banners` - Banner API

## 開發說明

### 資料庫遷移

建立遷移：
```bash
uv run alembic revision --autogenerate -m "描述"
```

執行遷移：
```bash
uv run alembic upgrade head
```

### 圖片上傳

- 支援格式：jpg, jpeg, png, gif
- 自動轉換為 WebP 格式
- 儲存在 `uploads/` 目錄下

## 注意事項

1. 請確保 MySQL 服務正在運行
2. 確保 `uploads/` 目錄有寫入權限
3. 生產環境請更改 SECRET_KEY 和管理員密碼
4. 建議使用環境變數管理敏感資訊

