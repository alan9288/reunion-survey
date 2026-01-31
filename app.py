import streamlit as st
import pandas as pd
import requests

# 頁面配置
st.set_page_config(page_title="同學聚會統計", page_icon="🍴", layout="centered")

# 自訂樣式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
    }
    .stForm {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 同學聚會意願調查")
st.write("請填寫以下資訊，資料會直接同步到雲端表格中！")

# Google Sheets 設定
SPREADSHEET_ID = st.secrets.get("gsheets", {}).get("spreadsheet_id", "1DeHUbX7J_D9kpLrK3jZzgWj_0bm3-K4av42k0YM063Y")
APPS_SCRIPT_URL = st.secrets.get("gsheets", {}).get("apps_script_url", "")

# 讀取現有資料的函數
@st.cache_data(ttl=30)  # 快取 30 秒
def load_data():
    try:
        # 使用公開 CSV 匯出 URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
        df = pd.read_csv(csv_url)
        df = df.dropna(how="all")
        return df
    except Exception as e:
        return pd.DataFrame(columns=["name", "time", "location", "food_type"])

# 寫入資料的函數
def append_data(new_row):
    if APPS_SCRIPT_URL:
        try:
            response = requests.post(APPS_SCRIPT_URL, json=new_row, timeout=10)
            if response.status_code == 200:
                return True, "資料已成功送出！"
            else:
                return False, f"伺服器回應錯誤：{response.status_code}"
        except Exception as e:
            return False, str(e)
    else:
        # 如果沒有設定 Apps Script，使用本地儲存
        if 'local_data' not in st.session_state:
            st.session_state.local_data = []
        st.session_state.local_data.append(new_row)
        return True, "資料已暫存（需設定 Apps Script 才能永久儲存）"

# 建立表單
with st.form("reunion_form", clear_on_submit=True):
    st.subheader("📝 填寫資料")
    
    name = st.text_input("你的姓名 *", placeholder="請輸入你的姓名")
    time = st.text_input("可以出席的時間 *", placeholder="例如: 2/14 晚上、週末都可以")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox(
            "偏好地點", 
            ["台北車站", "信義區", "公館", "板橋", "中山區", "西門町", "其他"]
        )
    with col2:
        food_type = st.multiselect(
            "餐點類型（可複選）", 
            ["火鍋", "燒肉", "義式", "日料", "美式", "泰式", "韓式", "港式", "其他"]
        )
    
    st.divider()
    submit = st.form_submit_button("🚀 送出資料", use_container_width=True)

if submit:
    if name and time:
        new_row = {
            "name": name,
            "time": time,
            "location": location,
            "food_type": ", ".join(food_type) if food_type else "未選擇"
        }
        
        success, message = append_data(new_row)
        
        if success:
            st.success(f"太棒了 {name}！{message} 🎉")
            st.balloons()
            # 清除快取以顯示新資料
            load_data.clear()
        else:
            st.error(f"發生錯誤：{message}")
    else:
        st.error("請填寫姓名與時間喔！這兩個欄位是必填的。")

# 分隔線
st.divider()

# 統計圖表區塊
if st.checkbox("📊 查看目前統計狀況"):
    existing_data = load_data()
    
    # 合併本地暫存的資料
    if 'local_data' in st.session_state and st.session_state.local_data:
        local_df = pd.DataFrame(st.session_state.local_data)
        existing_data = pd.concat([existing_data, local_df], ignore_index=True)
    
    if existing_data.empty:
        st.info("目前還沒有人填寫喔！你可以當第一個 😊")
    else:
        st.subheader(f"已收到 {len(existing_data)} 筆回覆")
        
        # 顯示資料表
        st.dataframe(existing_data, use_container_width=True, hide_index=True)
        
        # 地點統計
        if 'location' in existing_data.columns and not existing_data['location'].isna().all():
            st.subheader("📍 地點偏好統計")
            location_counts = existing_data['location'].value_counts()
            st.bar_chart(location_counts)

# 頁尾
st.divider()
st.caption("Made with ❤️ using Streamlit")
