# 🎓 同學聚會意願調查

一個使用 Streamlit 建立的同學聚會調查表單，資料會自動同步到 Google Sheets。

## 🚀 快速開始

### 1. 設定 Google Sheets

1. 建立新的 Google Sheets，命名為 `Reunion_Data`
2. 在第一行 (A1:D1) 填入欄位名稱：
   - `name`
   - `time`
   - `location`
   - `food_type`
3. 點擊右上角「共用」→ 選擇「知道連結的人皆可編輯」
4. 複製試算表的 URL

### 2. 設定 Secrets

編輯 `.streamlit/secrets.toml`，將 Google Sheets URL 貼上：

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/你的試算表ID/edit"
worksheet = "Sheet1"
```

### 3. 本地執行

```bash
# 安裝套件
pip install -r requirements.txt

# 執行應用程式
streamlit run app.py
```

開啟瀏覽器訪問 `http://localhost:8501`

---

## ☁️ 部署到 Streamlit Cloud

### 步驟 1：上傳到 GitHub

1. 建立一個新的 GitHub Repository
2. 上傳以下檔案：
   - `app.py`
   - `requirements.txt`
   - `.gitignore`（建議加入 `.streamlit/secrets.toml`）

### 步驟 2：連接 Streamlit Cloud

1. 前往 [share.streamlit.io](https://share.streamlit.io)
2. 使用 GitHub 帳號登入
3. 點擊「New app」
4. 選擇你的 Repository 和 `app.py`

### 步驟 3：設定 Secrets

1. 在 Streamlit Cloud 的 App Settings 中
2. 找到「Secrets」區塊
3. 貼上以下內容：

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/你的試算表ID/edit"
worksheet = "Sheet1"
```

### 步驟 4：部署

點擊「Deploy」，等待幾分鐘後，你會得到一個公開網址！

---

## 📱 功能特色

- ✅ 手機友善介面
- ✅ 資料即時同步到 Google Sheets
- ✅ 地點偏好統計圖表
- ✅ 表單驗證
- ✅ 慶祝動畫效果

---

## 📂 專案結構

```
.
├── app.py                # 主程式
├── requirements.txt      # 套件依賴
├── .streamlit/
│   └── secrets.toml      # 連線設定（不要上傳到 GitHub！）
└── README.md             # 說明文件
```

---

Made with ❤️ using Streamlit
