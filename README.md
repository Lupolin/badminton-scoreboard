# 羽毛球賽程安排系統 🏸

一個基於 Flask + HTMX 的羽毛球賽程自動安排與計分系統，可以智慧分配參賽者，確保每個人都有平等的上場機會和搭檔機會。

## 🌟 功能特色

- **智慧賽程安排**: 使用演算法確保每位參賽者的上場次數平衡
- **搭檔平衡**: 自動分配搭檔，避免固定組合
- **資料庫整合**: 支援 MySQL 資料庫，可以從歷史資料中讀取參賽者名單
- **即時計分**: 提供直觀的計分介面，支援比分調整
- **場次切換**: 輕鬆瀏覽不同場次的賽程
- **響應式設計**: 使用 HTMX 實現無頁面刷新的流暢體驗

## 🚀 快速開始

### 系統需求

- Python 3.8+
- MySQL 資料庫 (可選)

### 安裝步驟

1. **複製專案**

   ```bash
   git clone <repository-url>
   cd badminton-scheduler-flask
   ```

2. **建立虛擬環境**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **安裝相依套件**

   ```bash
   pip install -r requirements.txt
   ```

4. **環境設定**

   ```bash
   # 複製環境變數範例檔案
   cp .env.example .env

   # 編輯 .env 檔案，設定資料庫連線資訊
   ```

5. **啟動應用程式**

   ```bash
   python main.py
   ```

6. **開啟瀏覽器**

   前往 http://127.0.0.1:5000 開始使用

## ⚙️ 環境變數設定

在 `.env` 檔案中設定以下變數：

```env
# 資料庫設定 (MySQL)
RDS_HOST=localhost
RDS_USER=your_username
RDS_PASSWORD=your_password
RDS_DATABASE=badminton_db
RDS_PORT=3306

# Flask 設定
SECRET_KEY=your-secret-key-here
APP_TIMEZONE=Asia/Taipei

# 預設參賽者名單 (用逗號分隔)
DEFAULT_PLAYERS=Judy,Jesha,Lucas,Doris,Iris,Luna,Mars,Solomon
```

## 🗄️ 資料庫設定 (可選)

如果要使用資料庫功能，請建立以下資料表：

```sql
-- 參賽者資料表
CREATE TABLE players (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL UNIQUE,
  is_active TINYINT(1) DEFAULT 1
);

-- 出席記錄資料表
CREATE TABLE attendance (
  id INT PRIMARY KEY AUTO_INCREMENT,
  player_id INT NOT NULL,
  date DATE NOT NULL,
  present TINYINT(1) DEFAULT 1,
  INDEX (date),
  FOREIGN KEY (player_id) REFERENCES players(id)
);

-- 羽球回覆資料表 (用於讀取當日參與者)
CREATE TABLE badminton_reply (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_name VARCHAR(64) NOT NULL,
  reply_text VARCHAR(16) NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 📱 使用方法

### 1. 選擇參賽者

- 在首頁勾選今日參賽的球友
- 系統會自動從資料庫讀取回覆「要」的參賽者
- 也可以手動調整參賽者名單

### 2. 產生賽程

- 點擊「產生賽程」按鈕
- 系統會根據參賽人數自動計算最佳場次數
- 演算法確保每個人的上場機會平衡

### 3. 進行比賽

- 切換到「賽程清單」檢視所有場次
- 切換到「計分模式」進行比分記錄
- 使用「上一場」/「下一場」按鈕瀏覽不同場次

### 4. 計分功能

- 點擊「+」/「-」按鈽調整比分
- 支援比分重置功能
- 可以交換左右隊伍位置

## 🎯 賽程安排演算法

系統使用智慧演算法安排賽程，確保：

- **上場平衡**: 每位參賽者的上場次數盡可能相等
- **休息輪替**: 優先安排休息較久的球友上場
- **搭檔多樣化**: 避免固定搭檔組合，增加交流機會
- **隨機化**: 加入適度隨機性，避免過於規律的分組

根據參賽人數自動決定場次數：

- 4 人: 12 場
- 5 人: 20 場
- 6 人: 18 場
- 7 人: 21 場
- 8 人: 20 場

## 🏗️ 專案結構

```
badminton-scheduler-flask/
├── main.py                 # 應用程式入口點
├── requirements.txt        # Python 相依套件
├── .env                   # 環境變數設定
├── .gitignore            # Git 忽略檔案
├── README.md             # 專案說明文件
└── app/
    ├── __init__.py       # Flask 應用程式初始化
    ├── config.py         # 設定檔載入
    ├── routes/
    │   ├── web.py        # 網頁路由
    │   └── api.py        # API 路由
    ├── services/
    │   ├── generator.py  # 賽程產生演算法
    │   └── roster.py     # 名單管理服務
    ├── templates/        # HTML 模板
    │   ├── base.html
    │   ├── index.html
    │   └── _stage.html
    └── static/           # 靜態檔案
        └── styles.css
```

## 🔧 自訂賽程演算法

如果您想使用自己的賽程安排演算法，只需要：

1. 修改 `app/services/generator.py` 中的 `generate_schedule()` 函數
2. 確保函數回傳格式為：
   ```python
   [
       {"left": ["球員A", "球員B"], "right": ["球員C", "球員D"]},
       # ... 更多場次
   ]
   ```
3. 其他檔案無需修改

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案！

## 📄 授權

此專案採用 MIT 授權條款。

## 🆘 常見問題

**Q: 為什麼無法連接資料庫？**
A: 請檢查 `.env` 檔案中的資料庫設定是否正確，確保 MySQL 服務正在運行。

**Q: 可以在沒有資料庫的情況下使用嗎？**
A: 可以！系統會使用 `DEFAULT_PLAYERS` 環境變數中設定的預設參賽者名單。

**Q: 如何修改預設參賽者名單？**
A: 在 `.env` 檔案中修改 `DEFAULT_PLAYERS` 變數，使用逗號分隔球友姓名。

**Q: 支援幾人同時比賽？**
A: 目前支援 4-8 人的賽程安排，少於 4 人無法產生賽程。
