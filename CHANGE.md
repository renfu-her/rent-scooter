# 修改記錄 (Change Log)

本文檔記錄專案的所有重要修改和功能更新。

**最後更新時間：2025-11-12 16:23:27**

---

## 2025-11-12 16:23 - 訂單金額顯示改為整數格式

### 修改內容
- **金額顯示優化**：訂單管理中的金額顯示改為整數格式，不顯示小數點後的 `.00`
  - 訂單列表頁面：使用 `| int` 過濾器將金額轉換為整數顯示
  - 訂單詳情頁面：使用 `| int` 過濾器將金額轉換為整數顯示
  - 訂單創建表單：將 `step` 從 `0.01` 改為 `1`，添加 `min="0"` 限制
  - 訂單編輯表單：將 `step` 從 `0.01` 改為 `1`，添加 `min="0"` 限制，顯示值也轉換為整數

### 修改檔案
- `app/templates/admin/orders/index.html`
- `app/templates/admin/orders/detail.html`
- `app/templates/admin/orders/create.html`
- `app/templates/admin/orders/edit.html`

### 顯示效果
- 金額顯示為整數（例如：`NT$ 1000` 而不是 `NT$ 1000.00`）
- 輸入框只接受整數輸入（step=1）
- 更符合台灣貨幣使用習慣（通常不使用小數）

---

## 2025-11-12 16:20 - 訂單管理時間選擇器改用 Flatpickr（中文）

### 修改內容
- **時間選擇器升級**：將訂單管理中的日期時間輸入框改為使用 Flatpickr 日期選擇器
  - 添加 Flatpickr CSS 和 JavaScript 庫（CDN）
  - 添加中文語言包（`zh.js`）
  - 所有日期時間欄位使用 Flatpickr：
    - 預約日期：僅日期選擇（`dateFormat: "Y-m-d"`）
    - 租借開始時間、租借結束時間：日期時間選擇（`dateFormat: "Y-m-d H:i"`）
    - 船班出發時間、船班回程時間：日期時間選擇
    - 預計還車時間：日期時間選擇
  - 配置選項：
    - 中文介面（`locale: "zh"`）
    - 24 小時制（`time_24hr: true`）
    - 允許手動輸入（`allowInput: true`）
- **後端解析更新**：
  - 創建 `parse_datetime` 輔助函數，支持兩種格式：
    - Flatpickr 格式：`%Y-%m-%d %H:%M`（例如：`2025-11-12 14:30`）
    - 舊格式（向後兼容）：`%Y-%m-%dT%H:%M`（例如：`2025-11-12T14:30`）
  - 同時更新 `create` 和 `edit` 路由的日期時間解析邏輯

### 修改檔案
- `app/templates/admin/orders/create.html`
- `app/templates/admin/orders/edit.html`
- `app/views/admin/orders.py`

### 使用體驗
- 日期時間選擇更加直觀和友好
- 中文介面，符合本地化需求
- 支持點擊日曆圖標選擇，也支持手動輸入
- 24 小時制時間選擇，更符合台灣使用習慣

---

## 2025-11-12 16:11 - 訂單管理添加編輯功能

### 修改內容
- **訂單編輯功能**：為訂單管理添加完整的編輯功能
  - 訂單列表頁面：添加編輯按鈕（鉛筆圖標），與查看詳情按鈕並列
  - 編輯路由：創建 `/backend/orders/<order_id>/edit` 路由，支持 GET（顯示編輯表單）和 POST（更新訂單）
  - 編輯模板：創建 `edit.html`，基於 `create.html`，但預填所有現有訂單數據
  - 預填數據：所有表單欄位都會預填現有訂單的值，包括：
    - 合作商、承租人資訊（姓名、身份證號碼、是否有駕照）
    - 租借機車列表（顯示已選中的機車，可添加或移除）
    - 日期時間欄位（預約日期、租借時間、船班時間等）
    - 狀態、總金額、航運公司、付款方式、備註等
  - 機車管理：編輯時可以添加或移除機車，已選中的機車會自動顯示
  - 數據更新：使用 `OrderController.update` 方法更新訂單，支持所有欄位

### 修改檔案
- `app/views/admin/orders.py`
- `app/templates/admin/orders/index.html`
- `app/templates/admin/orders/edit.html`
- `app/controllers/order_controller.py`

### 功能特點
- 編輯表單與創建表單保持一致的外觀和功能
- 支持修改訂單的所有欄位
- 機車列表可以動態添加或移除
- 更新成功後會自動更新機車狀態（根據訂單狀態）
- 更新成功後會發送 WebSocket 通知

---

## 2025-11-12 16:07 - 側邊欄選單文字左對齊

### 修改內容
- **側邊欄樣式優化**：側邊欄選單文字統一左對齊
  - 移除所有選單項的 `justify-content: space-between`，改為預設左對齊
  - 對於有下拉選單的項目（如「商店與合作商」），文字部分靠左，箭頭圖標靠右
  - 普通選單項（無下拉選單）文字完全靠左對齊
  - 圖標添加 `flex-shrink: 0` 確保不會被壓縮

### 修改檔案
- `app/static/css/backend.css`

### 視覺效果
- 所有側邊欄選單項的文字現在都靠左對齊
- 下拉選單的箭頭圖標保持在右側
- 選單項的圖標和文字緊密排列在左側

---

## 2025-11-12 16:06 - 後台表格文字全部左對齊

### 修改內容
- **表格對齊優化**：所有後台管理頁面的表格文字統一左對齊
  - 商店管理頁面：表格和表頭添加 `text-start` 類別
  - DataTables 初始化：為所有 `th` 和 `td` 元素添加 `text-start` 類別
  - DataTables 配置：在 `columnDefs` 中添加 `className: 'text-start'`，確保所有列左對齊
  - 空數據提示行：從 `text-center` 改為 `text-start`

### 修改檔案
- `app/templates/admin/stores/index.html`
- `app/templates/admin/base.html`

### 影響範圍
- 所有使用 `data-table` 類別的後台管理頁面表格都會自動左對齊
- 包括：商店管理、合作商管理、機車管理、訂單管理、Banner管理、使用者管理等

---

## 2025-11-12 16:04 - 後台側邊欄合併商店與合作商管理

### 修改內容
- **側邊欄選單優化**：將「商店管理」和「合作商管理」合併為一個下拉選單項「商店與合作商」
  - 主選單項顯示「商店與合作商」，點擊可展開/收合子選單
  - 子選單包含「商店管理」和「合作商管理」兩個選項
  - 當訪問商店或合作商相關頁面時，主選單項會自動展開並高亮顯示
  - 添加箭頭圖標，展開時會旋轉 180 度
- **CSS 樣式增強**：
  - 子選單項有適當的縮排（padding-left: 2.5rem）
  - 子選單項字體稍小（0.9rem）
  - 箭頭圖標有平滑的旋轉動畫效果

### 修改檔案
- `app/templates/admin/base.html`
- `app/static/css/backend.css`

### 使用體驗
- 側邊欄更加簡潔，減少選單項數量
- 相關功能分組在一起，更符合邏輯
- 展開/收合動畫流暢，提升用戶體驗

---

## 2025-11-12 15:54 - 商店管理添加合作商關聯

### 修改內容
- **資料庫模型更新**：在 `Store` 模型中添加 `partner_id` 欄位
  - 添加外鍵關聯到 `partners` 表
  - 建立 `partner` 關聯關係（一對多：一個合作商可以有多個商店）
- **商店管理功能增強**：
  - 商店列表頁面新增「合作商」欄位，顯示商店所屬的合作商（以藍色徽章顯示）
  - 商店創建表單添加合作商選擇下拉選單（選填）
  - 商店編輯表單添加合作商選擇下拉選單，並預設選中當前合作商
- **控制器更新**：`StoreController` 的 `create` 和 `update` 方法支持 `partner_id` 參數
- **資料庫遷移**：創建遷移文件添加 `partner_id` 欄位和外鍵約束

### 修改檔案
- `app/models/store.py`
- `app/controllers/store_controller.py`
- `app/views/admin/stores.py`
- `app/templates/admin/stores/index.html`
- `app/templates/admin/stores/create.html`
- `app/templates/admin/stores/edit.html`
- `migrations/versions/8e8f12ad5f5e_add_partner_id_to_stores.py`

### 業務邏輯
- 商店可以選擇性地關聯到一個合作商
- 如果商店沒有關聯合作商，列表頁面顯示 "-"
- 合作商欄位為選填，不影響現有商店資料

---

## 2025-11-12 15:52 - 預訂完成時自動創建訂單記錄

### 修改內容
- **預訂流程增強**：當前端完成預訂時，系統會同時創建 Reservation 和 Order 記錄
  - 創建 `Reservation` 記錄：用於追蹤預訂狀態、到期時間等預訂相關資訊
  - 創建 `Order` 記錄：用於後台訂單管理，狀態為 '待處理'，金額為 0（後續可在後台更新）
  - Order 記錄包含承租人資訊（姓名、身份證號碼、是否有駕照）、聯絡電話、備註等
  - Order 記錄與預訂的機車建立關聯（透過 `OrderMotorcycle`）
- **狀態管理**：預訂時機車狀態設為 '預訂'，不會被改為 '出租中'（避免與 OrderController 的邏輯衝突）

### 修改檔案
- `app/controllers/motorcycle_controller.py`

### 業務邏輯
- 預訂完成後，後台可以在「訂單管理」中看到該訂單
- 訂單狀態為 '待處理'，管理員可以在後台更新訂單狀態、金額等資訊
- 當訂單狀態改為 '進行中' 或 '已完成' 時，機車狀態會自動更新（由 OrderController 處理）

---

## 2025-11-12 15:41 - 修正預訂表單 NoneType 錯誤

### 修改內容
- **錯誤修正**：修正預訂表單提交時的 `'NoneType' object has no attribute 'strip'` 錯誤
  - 當 JSON 數據中字段值為 `null` 時，`data.get()` 會返回 `None`
  - 使用 `or` 運算符確保在調用 `.strip()` 前將 `None` 轉換為空字串
  - 修正所有相關字段的處理邏輯（`renter_name`, `renter_id_number`, `contact_phone`, `remarks`）

### 修改檔案
- `app/views/frontend.py`

### 問題原因
當前端發送 JSON 數據時，如果某個字段的值是 `null`（例如 `contact_phone: null`），Python 的 `data.get('key', '')` 會返回 `None` 而不是預設值 `''`，導致對 `None` 調用 `.strip()` 時出錯。

### 解決方案
使用 `(data.get('key') or '')` 來確保即使值為 `None`，也會轉換為空字串，然後再調用 `.strip()`。

---

## 2025-11-12 15:41 - 修正臺灣身份證號碼檢查碼驗證邏輯

### 修改內容
- **後端驗證邏輯修正**：修正 `id_validator.py` 中檢查碼計算的索引錯誤
  - 正確計算字母代碼的十位數和個位數
  - 正確處理 9 位數字的權重計算（id_number[1] 到 id_number[9]）
  - 確保檢查碼驗證符合臺灣身份證標準算法
- **前端驗證邏輯同步**：更新 JavaScript 驗證函數，與後端邏輯保持一致
  - 修正檢查碼計算的索引映射
  - 確保前端和後端驗證結果一致

### 修改檔案
- `app/utils/id_validator.py`
- `app/templates/frontend/store_detail.html`

### 測試結果
- `A123456789`：驗證通過 ✓
- 無效身份證號碼：正確拒絕並顯示錯誤訊息

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

