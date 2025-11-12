# 安裝指南 (Installation Guide)

本文檔提供機車租借管理系統的完整安裝說明。

## 目錄

- [系統需求](#系統需求)
- [前置準備](#前置準備)
- [安裝步驟](#安裝步驟)
- [配置說明](#配置說明)
- [初始化資料庫](#初始化資料庫)
- [啟動應用程式](#啟動應用程式)
- [驗證安裝](#驗證安裝)
- [故障排除](#故障排除)
- [生產環境部署](#生產環境部署)

---

## 系統需求

### 必要軟體

- **Python**: 3.12 或更高版本
- **MySQL**: 5.7 或更高版本（建議 8.0+）
- **UV**: Python 套件管理器（用於依賴管理）

### 作業系統

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)

### 硬體需求

- **最低配置**:
  - CPU: 2 核心
  - RAM: 2GB
  - 硬碟空間: 5GB

- **建議配置**:
  - CPU: 4 核心或更多
  - RAM: 4GB 或更多
  - 硬碟空間: 10GB 或更多（用於圖片儲存）

---

## 前置準備

### 1. 安裝 Python

確認 Python 版本：

```bash
python --version
# 或
python3 --version
```

如果未安裝或版本低於 3.12，請前往 [Python 官網](https://www.python.org/downloads/) 下載安裝。

### 2. 安裝 UV

UV 是一個快速的 Python 套件管理器：

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

驗證安裝：
```bash
uv --version
```

### 3. 安裝 MySQL

#### Windows

1. 下載 MySQL Installer: https://dev.mysql.com/downloads/installer/
2. 執行安裝程式，選擇 "Developer Default" 或 "Server only"
3. 設定 root 密碼（記住此密碼，後續會用到）

#### macOS

使用 Homebrew:
```bash
brew install mysql
brew services start mysql
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 4. 設定 MySQL

登入 MySQL：
```bash
mysql -u root -p
```

建立資料庫：
```sql
CREATE DATABASE IF NOT EXISTS `rent-scooter` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

建立專用使用者（可選，建議生產環境使用）：
```sql
CREATE USER 'rentscooter'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON `rent-scooter`.* TO 'rentscooter'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 安裝步驟

### 1. 下載專案

使用 Git 克隆專案：
```bash
git clone <repository-url>
cd rent-scooter
```

或直接下載 ZIP 檔案並解壓縮。

### 2. 安裝 Python 依賴

在專案根目錄執行：

```bash
uv sync
```

這會自動安裝所有必要的 Python 套件，包括：
- Flask 3.x
- SQLAlchemy
- Flask-SocketIO
- Pillow
- 以及其他依賴項

### 3. 建立上傳目錄

專案會自動建立上傳目錄，但您也可以手動建立：

```bash
# Windows
mkdir uploads
mkdir uploads\motorcycles
mkdir uploads\banners
mkdir uploads\stores

# macOS/Linux
mkdir -p uploads/{motorcycles,banners,stores}
```

---

## 配置說明

### 環境變數配置

專案已包含 `.env.example` 範本檔案。建立您的 `.env` 檔案：

**Windows:**
```powershell
# 複製範本檔案
copy .env.example .env

# 然後編輯 .env 檔案，填入您的資料庫資訊
notepad .env
```

**macOS/Linux:**
```bash
# 複製範本檔案
cp .env.example .env

# 然後編輯 .env 檔案，填入您的資料庫資訊
nano .env
# 或
vim .env
```

**`.env` 檔案內容範例：**

```env
# 資料庫連線設定
# 格式: mysql+pymysql://使用者名稱:密碼@主機:埠號/資料庫名稱
# 範例: mysql+pymysql://root:password@localhost:3306/rent-scooter
DATABASE_URL=mysql+pymysql://root:your_password@localhost/rent-scooter

# 如果使用專用使用者：
# DATABASE_URL=mysql+pymysql://rentscooter:your_password@localhost/rent-scooter

# Flask Secret Key（生產環境必須更改）
# 可以使用以下命令生成: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-super-secret-key-change-in-production

# 上傳檔案大小限制（MB，可選）
# MAX_UPLOAD_SIZE=16
```

**重要提示：**
- `.env` 檔案已加入 `.gitignore`，不會被提交到版本控制
- 如果沒有 `.env` 檔案，系統會使用預設值
- 預設資料庫連線：`mysql+pymysql://root@localhost/rent-scooter`（無密碼）
- 預設 Secret Key 僅用於開發環境，生產環境必須更改
- 如果 MySQL 有設定密碼，請在 `DATABASE_URL` 中包含密碼

### 修改資料庫連線

如果您的 MySQL 設定不同，可以：

1. **使用環境變數**（推薦）：
   ```bash
   # Windows PowerShell
   $env:DATABASE_URL="mysql+pymysql://user:password@localhost/rent-scooter"
   
   # macOS/Linux
   export DATABASE_URL="mysql+pymysql://user:password@localhost/rent-scooter"
   ```

2. **修改 `app/config.py`**：
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/rent-scooter'
   ```

---

## 初始化資料庫

### 執行初始化腳本

```bash
uv run python init_db.py
```

這個腳本會：
1. 建立所有必要的上傳目錄
2. 嘗試建立資料庫（如果不存在）
3. 建立所有資料表
4. 建立預設管理員帳號

### 預設管理員帳號

- **使用者名稱**: `admin`
- **密碼**: `admin123`

**⚠️ 安全警告：請在首次登入後立即更改密碼！**

### 資料庫遷移（可選）

如果專案包含遷移檔案，可以執行：

```bash
# 建立新的遷移
uv run flask db migrate -m "描述訊息"

# 執行遷移
uv run flask db upgrade
```

---

## 啟動應用程式

### 開發模式

```bash
uv run python run.py
```

應用程式將在 `http://127.0.0.1:8000` 啟動。

### 訪問應用程式

- **前端首頁**: http://127.0.0.1:8000/
- **後台管理**: http://127.0.0.1:8000/backend/
- **登入頁面**: http://127.0.0.1:8000/auth/login

### 停止應用程式

在終端機按 `Ctrl+C` 停止應用程式。

---

## 驗證安裝

### 1. 檢查資料庫連線

```bash
uv run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Database connection:', db.engine.url)"
```

### 2. 檢查依賴套件

```bash
uv run python -c "from app import create_app; app = create_app(); print('✓ All dependencies installed successfully')"
```

### 3. 測試 WebSocket 連線

1. 開啟瀏覽器開發者工具（F12）
2. 前往後台管理頁面
3. 在 Console 中應該看到 "WebSocket connected"

### 4. 測試登入

1. 前往登入頁面
2. 使用預設帳號登入：
   - 使用者名稱: `admin`
   - 密碼: `admin123`
3. 成功登入後應該會導向後台儀表板

---

## 故障排除

### 問題 1: 無法連線到 MySQL

**錯誤訊息**: `(2003, "Can't connect to MySQL server")`

**解決方案**:
1. 確認 MySQL 服務正在運行：
   ```bash
   # Windows
   net start mysql
   
   # macOS/Linux
   sudo systemctl status mysql
   # 或
   brew services list
   ```

2. 檢查 MySQL 連線設定是否正確
3. 確認防火牆允許 MySQL 連線（預設埠 3306）

### 問題 2: 資料庫不存在

**錯誤訊息**: `(1049, "Unknown database 'rent-scooter'")`

**解決方案**:
```sql
CREATE DATABASE `rent-scooter` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

或執行 `init_db.py`，它會自動建立資料庫。

### 問題 3: 權限錯誤

**錯誤訊息**: `(1045, "Access denied for user")`

**解決方案**:
1. 確認 MySQL 使用者名稱和密碼正確
2. 確認使用者有權限存取資料庫：
   ```sql
   GRANT ALL PRIVILEGES ON `rent-scooter`.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 問題 4: 圖片上傳失敗

**錯誤訊息**: `Permission denied` 或 `No such file or directory`

**解決方案**:
1. 確認 `uploads/` 目錄存在且有寫入權限：
   ```bash
   # Windows
   icacls uploads /grant Users:F
   
   # macOS/Linux
   chmod -R 755 uploads
   ```

2. 確認子目錄存在：
   ```bash
   mkdir -p uploads/{motorcycles,banners,stores}
   ```

### 問題 5: WebSocket 連線失敗

**錯誤訊息**: `WebSocket connection failed`

**解決方案**:
1. 確認應用程式使用 `socketio.run()` 啟動（已在 `run.py` 中設定）
2. 檢查防火牆是否允許 WebSocket 連線
3. 確認瀏覽器支援 WebSocket（所有現代瀏覽器都支援）

### 問題 6: 依賴套件安裝失敗

**錯誤訊息**: `Package installation failed`

**解決方案**:
1. 確認 Python 版本 >= 3.12：
   ```bash
   python --version
   ```

2. 更新 UV：
   ```bash
   uv self update
   ```

3. 清除快取並重新安裝：
   ```bash
   uv cache clean
   uv sync
   ```

### 問題 7: 埠號被佔用

**錯誤訊息**: `Address already in use` 或 `Port 8000 is already in use`

**解決方案**:
1. 更改埠號（修改 `run.py`）：
   ```python
   socketio.run(app, debug=True, host='127.0.0.1', port=8001)
   ```

2. 或關閉佔用埠號的程式：
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -ti:8000 | xargs kill -9
   ```

---

## 生產環境部署

### 1. 安全設定

#### 更改 Secret Key

在 `.env` 檔案中設定強隨機密鑰：
```env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

#### 更改預設管理員密碼

登入後立即在後台更改管理員密碼。

#### 使用專用資料庫使用者

不要使用 root 使用者，建立專用使用者並限制權限。

### 2. 使用生產級 WSGI 伺服器

#### 使用 Gunicorn (Linux/macOS)

```bash
uv add gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 --worker-class eventlet run:app
```

#### 使用 Waitress (Windows/跨平台)

```bash
uv add waitress
waitress-serve --host=0.0.0.0 --port=8000 run:app
```

### 3. 設定反向代理 (Nginx)

範例 Nginx 設定：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /socket.io/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4. 設定 SSL/TLS

使用 Let's Encrypt 取得免費 SSL 憑證：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 5. 設定系統服務 (systemd)

建立服務檔案 `/etc/systemd/system/rent-scooter.service`：

```ini
[Unit]
Description=Rent Scooter Management System
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/rent-scooter
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 --worker-class eventlet run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

啟動服務：
```bash
sudo systemctl daemon-reload
sudo systemctl enable rent-scooter
sudo systemctl start rent-scooter
```

### 6. 定期備份

設定資料庫自動備份：

```bash
# 建立備份腳本
cat > /path/to/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p rent-scooter > "$BACKUP_DIR/rent-scooter_$DATE.sql"
# 保留最近 30 天的備份
find $BACKUP_DIR -name "rent-scooter_*.sql" -mtime +30 -delete
EOF

chmod +x /path/to/backup.sh

# 設定 cron 每日備份
crontab -e
# 添加：0 2 * * * /path/to/backup.sh
```

### 7. 監控和日誌

- 設定日誌輪轉
- 監控應用程式健康狀態
- 設定錯誤通知

---

## 額外資源

- [Flask 官方文檔](https://flask.palletsprojects.com/)
- [SQLAlchemy 文檔](https://docs.sqlalchemy.org/)
- [Flask-SocketIO 文檔](https://flask-socketio.readthedocs.io/)
- [MySQL 官方文檔](https://dev.mysql.com/doc/)

---

## 取得協助

如果遇到問題：

1. 檢查本文檔的「故障排除」章節
2. 查看專案的 `README.md`
3. 檢查應用程式日誌檔案
4. 聯繫專案維護者或提交 Issue

---

**祝您安裝順利！** 🚀

