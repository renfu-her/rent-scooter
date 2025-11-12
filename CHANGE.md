# 修改記錄 (Change Log)

本文檔記錄專案的所有重要修改和功能更新。

**最後更新時間：2025-11-12 15:27:26**

---

## 2025-11-12 15:27 - 訂單系統添加承租人資料

### 修改內容
- **資料庫模型更新**：在 `Order` 模型中添加承租人詳細資訊欄位
  - `renter_name`：承租人姓名
  - `renter_id_number`：身份證號碼
  - `has_license`：是否有駕照
- **訂單創建表單**：添加「承租人資訊」區塊，包含姓名、身份證號碼、駕照狀態欄位
- **訂單列表頁面**：新增「承租人」欄位，顯示姓名和身份證號碼
- **訂單詳情頁面**：完整顯示承租人資訊（姓名、身份證號碼、是否有駕照）
- **資料庫遷移**：執行遷移添加新欄位

### 修改檔案
- `app/models/order.py`
- `app/controllers/order_controller.py`
- `app/views/admin/orders.py`
- `app/templates/admin/orders/create.html`
- `app/templates/admin/orders/index.html`
- `app/templates/admin/orders/detail.html`
- `migrations/versions/add_renter_info_to_orders.py`

---

## 2025-11-12 15:27 - 身份證號碼驗證功能

### 修改內容
- **後端驗證**：創建 `id_validator.py` 工具模組，實現台灣身份證號碼完整驗證
  - 格式驗證（10碼、字母+數字組合）
  - 檢查碼驗證（使用台灣身份證標準算法）
- **前端驗證**：JavaScript 實現即時驗證和格式化
  - 自動轉換為大寫
  - 自動過濾無效字元
  - 檢查碼驗證
- **預訂表單**：添加身份證號碼輸入欄位，包含格式提示和即時驗證

### 修改檔案
- `app/utils/id_validator.py`
- `app/views/frontend.py`
- `app/templates/frontend/store_detail.html`

---

## 2025-11-12 15:27 - 前端機車預訂功能

### 修改內容
- **預訂模型**：創建 `Reservation` 模型存儲預訂資訊
  - 承租人姓名、身份證號碼、是否有駕照
  - 預訂狀態、到期時間
- **預訂功能**：前端商店詳情頁面添加「訂購」按鈕和預訂 Modal
  - 顯示機車詳細資料和圖片
  - 預訂狀態選擇（預訂、出租中、已出租）
  - 承租人資訊表單（姓名、身份證、駕照狀態）
- **駕照驗證**：根據車款類型驗證駕照要求
  - 白牌、綠牌：需要駕照
  - 電輔車：不需要駕照
- **過期預訂處理**：自動檢查並恢復過期預訂為「待出租」狀態
- **時區配置**：設置為 Asia/Taipei，預訂到期時間為當天 23:59:59

### 修改檔案
- `app/models/reservation.py`
- `app/models/motorcycle.py`
- `app/controllers/motorcycle_controller.py`
- `app/views/frontend.py`
- `app/utils/timezone_utils.py`
- `app/templates/frontend/store_detail.html`
- `migrations/versions/add_reservation_to_motorcycles.py`
- `migrations/versions/add_reservations_table.py`

---

## 2025-11-12 15:27 - 機車管理列表添加圖片欄位

### 修改內容
- **表格結構**：在機車管理列表的 ID 欄位後添加「圖片」欄位
- **圖片顯示**：顯示 60x60px 縮圖，可點擊放大查看
- **圖片 Modal**：使用 Bootstrap Modal 顯示大圖

### 修改檔案
- `app/templates/admin/motorcycles/index.html`

---

## 2025-11-12 15:27 - 圖片點擊放大功能

### 修改內容
- **前端商店詳情頁**：機車圖片可點擊放大查看
- **後端機車編輯頁**：機車圖片可點擊放大查看
- **後端商店列表頁**：商店圖片可點擊放大查看
- **後端商店編輯頁**：商店圖片可點擊放大查看
- **實現方式**：使用 Bootstrap Modal 顯示大圖

### 修改檔案
- `app/templates/frontend/store_detail.html`
- `app/templates/admin/motorcycles/edit.html`
- `app/templates/admin/stores/index.html`
- `app/templates/admin/stores/edit.html`

---

## 2025-01-XX - 文本更新（機車租賃）

### 修改內容
- **前端**：將 "RENT 機車租借" 更改為 "機車租賃"
- **後端**：將 "RENT 管理" 更改為 "機車租賃後臺"，"管理後台" 更改為 "管理系統"

### 修改檔案
- `app/templates/app.html`
- `app/templates/admin/base.html`

---

## 2025-01-XX - 前端移動端菜單功能

### 修改內容
- **響應式設計**：實現移動端漢堡菜單（hamburger menu）
- **菜單功能**：點擊漢堡圖標展開/收起菜單
- **菜單樣式**：移動端菜單項目置中顯示
- **交互優化**：點擊外部區域或菜單項目自動關閉菜單

### 修改檔案
- `app/templates/app.html`

---

## 2025-01-XX - 前端商店詳情頁面重設計

### 修改內容
- **Hero 區塊**：商店詳情頁頂部改為全寬英雄圖片
  - 桌面高度：350px
  - 移動端高度：250px
  - 半透明遮罩顯示商店資訊（名稱、電話、地址）
  - 「返回首頁」按鈕
- **響應式設計**：優化移動端顯示效果

### 修改檔案
- `app/templates/frontend/store_detail.html`

---

## 2025-01-XX - 安裝文檔和環境配置

### 修改內容
- **INSTALL.md**：創建詳細的安裝說明文檔
  - 系統需求
  - 安裝步驟
  - 配置說明
  - 資料庫初始化
  - 故障排除
- **.env.example**：創建環境變數範例文件
  - DATABASE_URL
  - SECRET_KEY

### 修改檔案
- `INSTALL.md`
- `.env.example`

---

## 2025-01-XX - WebSocket 即時通知功能

### 修改內容
- **WebSocket 集成**：使用 Flask-SocketIO 實現即時通知
- **狀態變更通知**：機車狀態變更時發送 Toast 通知
  - 出租中、歸還、送修等狀態變更
- **前端通知**：使用 Bootstrap Toast 顯示通知
- **重連機制**：自動重連和錯誤處理

### 修改檔案
- `app/__init__.py`
- `app/utils/websocket_events.py`
- `app/controllers/motorcycle_controller.py`
- `app/controllers/order_controller.py`
- `app/templates/admin/base.html`
- `run.py`
- `pyproject.toml`

---

## 2025-01-XX - 機車顏色選項更新

### 修改內容
- **顏色選項**：添加更多顏色選項
  - 綠色、黃色、紅色、銀色、牛奶色（原有：黑、白）

### 修改檔案
- `app/templates/admin/motorcycles/create.html`
- `app/templates/admin/motorcycles/edit.html`

---

## 2025-01-XX - 商店圖片功能

### 修改內容
- **資料庫模型**：在 `Store` 模型中添加 `image_path` 欄位
- **圖片上傳**：商店創建和編輯支持圖片上傳
- **圖片顯示**：前端和後端都顯示商店圖片
- **圖片處理**：轉換為 WebP 格式，使用 UUID7 命名

### 修改檔案
- `app/models/store.py`
- `app/controllers/store_controller.py`
- `app/views/admin/stores.py`
- `app/templates/admin/stores/index.html`
- `app/templates/admin/stores/create.html`
- `app/templates/admin/stores/edit.html`
- `app/templates/frontend/index.html`
- `app/templates/frontend/store_detail.html`
- `migrations/versions/c78860628ed7_add_image_path_to_stores.py`

---

## 2025-01-XX - 統一設計規範

### 修改內容
- **統一 Index 頁面設計**：所有列表頁面統一設計
  - 頁面標題和「新增內容」按鈕
  - 搜尋/篩選區塊（卡片樣式）
  - DataTables 集成
  - 狀態徽章和操作按鈕
- **統一 Create/Edit 頁面設計**：所有表單頁面統一設計
  - 頁面標題和返回按鈕
  - 卡片包裹的表單
  - Bootstrap 5 表單樣式
  - 統一的按鈕文字（儲存、取消）

### 修改檔案
- 所有 `app/templates/admin/*/index.html`
- 所有 `app/templates/admin/*/create.html`
- 所有 `app/templates/admin/*/edit.html`

---

## 2025-01-XX - 用戶管理系統

### 修改內容
- **用戶管理模組**：創建完整的用戶管理功能
  - 用戶列表（搜尋、角色/狀態篩選）
  - 創建用戶（用戶名、郵箱、密碼、用戶類型、商店選擇、狀態）
  - 編輯用戶
  - 刪除用戶
- **側邊欄集成**：添加「使用者管理」到後端側邊欄

### 修改檔案
- `app/controllers/user_controller.py`
- `app/views/admin/users.py`
- `app/templates/admin/users/index.html`
- `app/templates/admin/users/create.html`
- `app/templates/admin/users/edit.html`
- `app/templates/admin/base.html`

---

## 2025-01-XX - Banner 表單更新

### 修改內容
- **Banner 模型**：添加 `banner_name` 和 `subtitle` 欄位
- **Banner 表單**：更新創建和編輯表單
  - 標題和狀態切換在同一行
  - 添加副標題欄位
  - Bootstrap 5 form-switch 樣式
- **狀態切換**：添加狀態切換路由

### 修改檔案
- `app/models/banner.py`
- `app/controllers/banner_controller.py`
- `app/views/admin/banners.py`
- `app/templates/admin/banners/create.html`
- `app/templates/admin/banners/edit.html`
- `migrations/versions/678447775629_add_banner_name_and_subtitle_to_banners.py`

---

## 2025-01-XX - 前端商店頁面

### 修改內容
- **商店列表頁**：首頁顯示所有商店
  - Bootstrap 卡片樣式
  - 商店圖片、名稱、地址、電話
  - 「查看詳情」連結
- **商店詳情頁**：顯示商店資訊和機車列表
  - 商店詳細資訊
  - 該商店的所有機車（卡片樣式）
  - 機車圖片、型號、車款類型、顏色、狀態、車牌

### 修改檔案
- `app/views/frontend.py`
- `app/templates/frontend/index.html`
- `app/templates/frontend/store_detail.html`

---

## 2025-01-XX - 圖片上傳功能（UUID7）

### 修改內容
- **圖片處理**：實現圖片上傳和處理功能
  - 轉換為 WebP 格式
  - 使用 UUID7 命名（自定義實現）
  - 不保留原始檔名
- **編輯時刪除舊圖**：編輯時上傳新圖片自動刪除舊圖片
- **圖片工具**：創建 `image_processor.py` 工具模組

### 修改檔案
- `app/utils/image_processor.py`
- `app/views/admin/banners.py`
- `app/views/admin/motorcycles.py`
- `pyproject.toml`

---

## 2025-01-XX - Bootstrap 5 表單更新

### 修改內容
- **表單樣式**：所有創建和編輯表單更新為 Bootstrap 5 樣式
  - `form-label`、`form-control`、`form-select`
  - `form-check form-switch` 用於開關
  - 統一的間距和佈局

### 修改檔案
- 所有 `app/templates/admin/*/create.html`
- 所有 `app/templates/admin/*/edit.html`

---

## 2025-01-XX - DataTables 集成

### 修改內容
- **DataTables 集成**：所有後端列表頁面集成 DataTables
  - 搜尋、排序、分頁功能
  - 中文語言包
  - 響應式設計
- **空表格處理**：修復空表格的「Incorrect column count」錯誤
  - 移除 colspan 的空數據行
  - 使用 DataTables 的 emptyTable 選項

### 修改檔案
- `app/templates/admin/base.html`
- 所有 `app/templates/admin/*/index.html`

---

## 2025-01-XX - 後端佈局重構

### 修改內容
- **側邊欄設計**：固定左側深色側邊欄
  - 垂直菜單
  - 圖標和文字
  - 響應式設計（移動端漢堡菜單）
- **頂部導航欄**：固定頂部導航欄
  - 用戶資訊下拉菜單
  - 登出功能
- **主內容區**：使用 `col-12` 確保全寬顯示
- **CSS 分離**：創建 `backend.css` 存放後端樣式

### 修改檔案
- `app/templates/admin/base.html`
- `app/static/css/backend.css`

---

## 2025-01-XX - 錯誤頁面

### 修改內容
- **自定義錯誤頁面**：創建 403、404、500 錯誤頁面
- **錯誤處理器**：註冊錯誤處理器到 Flask 應用

### 修改檔案
- `app/utils/error_handlers.py`
- `app/templates/errors/404.html`
- `app/templates/errors/403.html`
- `app/templates/errors/500.html`
- `app/__init__.py`

---

## 2025-01-XX - 後端路由改為 /backend

### 修改內容
- **路由前綴**：所有後端路由從 `/admin` 改為 `/backend`
- **重定向**：添加 `/backend` 路由重定向到後台首頁

### 修改檔案
- `app/__init__.py`
- `app/views/backend.py`
- 所有後端路由文件

---

## 2025-01-XX - Banner 管理系統

### 修改內容
- **Banner 管理**：創建完整的 Banner 管理功能
  - Banner 列表
  - 創建 Banner
  - 編輯 Banner
  - 刪除 Banner
  - 圖片上傳

### 修改檔案
- `app/views/admin/banners.py`
- `app/templates/admin/banners/index.html`
- `app/templates/admin/banners/create.html`
- `app/templates/admin/banners/edit.html`

---

## 2025-01-XX - 訂單管理系統

### 修改內容
- **訂單管理**：創建完整的訂單管理功能
  - 訂單列表（搜尋、狀態篩選）
  - 創建訂單（多選機車、搜尋、型號統計）
  - 訂單詳情
  - 機車狀態自動更新

### 修改檔案
- `app/views/admin/orders.py`
- `app/templates/admin/orders/index.html`
- `app/templates/admin/orders/create.html`
- `app/templates/admin/orders/detail.html`

---

## 初始專案設置

### 修改內容
- **基礎模板**：創建 `app.html` 作為基礎模板
- **Flask 應用初始化**：設置 Flask、SQLAlchemy、Flask-Login
- **資料庫模型**：創建 User、Partner、Store、Motorcycle、Order、Banner 模型
- **認證系統**：實現登入、登出功能
- **基礎路由**：前端和後端基礎路由

### 修改檔案
- `app/__init__.py`
- `app/templates/app.html`
- `app/models/*.py`
- `app/views/auth.py`
- `app/views/frontend.py`
- `app/views/backend.py`

---

## 備註

- 所有日期格式為 YYYY-MM-DD
- 每次重要功能更新都應記錄在此文件中
- 修改檔案列表包含所有相關的檔案變更

