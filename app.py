import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (馬立雲部落專屬配置)
# ==========================================
st.set_page_config(
    page_title="馬立雲部落 Maibul | 撒奇萊雅族文化與舞鶴茶香",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (撒奇萊雅暗紅 x 土地金黃 x 茶園翠綠)
# ==========================================
st.markdown("""
    <style>
    /* 全站背景：象徵舞鶴台地的溫潤大地色 */
    .stApp {
        background-color: #FAFAED;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #3E2723 !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #3E2723 !important;
    }

    /* 深色模式防禦：強制輸入框白底黑字 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important; 
        border: 1px solid #D7CCC8 !important;
        color: #3E2723 !important; 
    }
    input { color: #3E2723 !important; }
    div[data-baseweb="select"] span { color: #3E2723 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #3E2723 !important; }
    svg { fill: #3E2723 !important; color: #3E2723 !important; }

    /* 日期選單高亮 (撒奇萊雅暗紅) */
    div[data-testid="stDateInput"] > label {
        color: #8B0000 !important; 
        font-size: 20px !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 2px solid #8B0000 !important; 
        background-color: #FFF0F5 !important;
        border-radius: 10px !important;
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區：撒奇萊雅族 凝血暗紅 到 土地金黃的漸層 */
    .header-box {
        background: linear-gradient(135deg, #7A0000 0%, #B8860B 100%);
        padding: 35px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(122, 0, 0, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 30px; font-weight: bold; letter-spacing: 2px; margin-bottom: 5px;}
    .header-subtitle { font-size: 15px; color: #F5F5DC !important; font-style: italic; }
    
    /* 卡片模組 */
    .section-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border-top: 4px solid #B8860B;
        margin-bottom: 20px;
    }
    
    /* 轉換率按鈕 (土地金，吸引點擊) */
    .stButton>button {
        width: 100%;
        background-color: #DAA520; 
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(218, 165, 32, 0.3);
    }
    .stButton>button:hover { background-color: #B8860B; transform: translateY(-2px); }
    
    /* 導覽時間軸 */
    .tour-item {
        border-left: 4px solid #8B0000;
        padding-left: 15px;
        margin-bottom: 18px;
        position: relative;
    }
    .tour-item::before {
        content: '🔥';
        position: absolute;
        left: -15px;
        top: 0;
        background: #FAFAED;
    }
    .tour-title { font-weight: bold; color: #7A0000 !important; font-size: 19px; }
    .tour-tag { font-size: 12px; background: #FFF5EE; color: #8B0000 !important; padding: 3px 10px; border-radius: 12px; margin-right: 6px; font-weight: bold;}
    
    /* 商品網格卡片 */
    .product-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .product-card:hover { border-color: #2E8B57; box-shadow: 0 8px 15px rgba(46,139,87,0.15); transform: translateY(-3px);}
    .product-price { font-size: 20px; color: #8B0000 !important; font-weight: 900; margin: 8px 0; }
    .product-tag { font-size: 11px; background: #E8F5E9; color: #2E8B57 !important; padding: 3px 8px; border-radius: 8px; font-weight: bold;}
    .badge { position: absolute; top: 10px; right: -25px; background: #D32F2F; color: white !important; font-size: 10px; font-weight: bold; padding: 3px 30px; transform: rotate(45deg); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (馬立雲部落導覽與農創)
# ==========================================
tours_db = [
    {"name": "撒奇萊雅族文化與火神祭尋根", "type": "文化深度", "duration": "2小時", "fee": "$400", "desc": "走進馬立雲部落，聆聽加禮宛戰役的歷史，認識撒奇萊雅族獨特的服飾色彩與火神祭(Palamal)文化。"},
    {"name": "舞鶴台地：蜜香紅茶採茶體驗", "type": "食農教育", "duration": "2.5小時", "fee": "$600", "desc": "戴上斗笠化身採茶小農，尋找小綠葉蟬的蹤跡，親手揉捻並品嚐世界級的冠軍蜜香紅茶。"},
    {"name": "掃叭石柱傳說與部落廚房", "type": "神話與美食", "duration": "3小時", "fee": "$850", "desc": "探訪瑞穗神秘的掃叭石柱，隨後返回部落廚房享用由刺蔥、野菜與放山雞製作的原民風味大餐。"},
    {"name": "馬立雲莊園咖啡烘焙 DIY", "type": "手作活動", "duration": "1.5小時", "fee": "$500", "desc": "舞鶴不只有茶！體驗在地阿拉比卡咖啡豆的挑豆、手工烘焙，帶回專屬自己的部落咖啡香。"}
]

products_db = [
    {"name": "頂級舞鶴蜜香紅茶 (立體茶包)", "category": "茶葉飲品", "price": 450, "icon": "🍵", "desc": "經小綠葉蟬吸食，散發天然天然蜜香與果香，冷泡熱泡皆回甘，瑞穗最具代表性特產。", "hot": True},
    {"name": "馬立雲莊園水洗咖啡豆", "category": "茶葉飲品", "price": 580, "icon": "☕", "desc": "種植於舞鶴台地，純淨水源灌溉，帶有微酸果香與堅果尾韻的中淺焙精品豆。", "hot": False},
    {"name": "撒奇萊雅族圖騰編織零錢包", "category": "文創工藝", "price": 350, "icon": "🧵", "desc": "部落婦女手工編織，融入象徵土地與祖靈的「凝血暗紅」與「土金」圖騰，獨一無二。", "hot": True},
    {"name": "部落秘製刺蔥海鹽", "category": "在地風味", "price": 250, "icon": "🌿", "desc": "嚴選部落野生刺蔥與純淨海鹽調配，是煎烤肉類或海鮮的最佳提味靈魂。", "hot": False},
    {"name": "老欉舞鶴文旦柚 (中秋限定)", "category": "時令鮮果", "price": 600, "icon": "🍋", "desc": "傳承數十年的老樹文旦，果肉細緻多汁、甜中帶微酸，花東縱谷秋季的恩賜。", "hot": True},
    {"name": "火神祭(Palamal)紀念明信片套組", "category": "文創工藝", "price": 150, "icon": "✉️", "desc": "收錄部落火神祭儀式的震撼瞬間與美麗的服飾特寫，寄託來自奇萊平原的祝福。", "hot": False}
]

# ==========================================
# 4. 邏輯核心：精準推薦系統
# ==========================================
def recommend_tours(group):
    if group == "品茗嗜啡 (熱愛茶與咖啡)":
        return [t for t in tours_db if t['name'] in ["舞鶴台地：蜜香紅茶採茶體驗", "馬立雲莊園咖啡烘焙 DIY"]]
    elif group == "文化尋根 (歷史與文史客)":
        return [t for t in tours_db if t['type'] in ["文化深度", "神話與美食"]]
    elif group == "親子踏青 (帶小孩)":
        return [t for t in tours_db if t['name'] in ["舞鶴台地：蜜香紅茶採茶體驗", "掃叭石柱傳說與部落廚房"]]
    else:
        return tours_db[:3]

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🔥 馬立雲部落 Maibul</div>
        <div class="header-subtitle">撒奇萊雅族文化傳承 • 舞鶴台地茶香秘境</div>
    </div>
""", unsafe_allow_html=True)

# --- 區塊 1：導覽預約模組 ---
st.markdown("### ⛰️ 預約部落與茶園體驗")
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        visit_date = st.date_input("📅 預計到訪瑞穗日期", value=date.today())
    with col2:
        group = st.selectbox("👥 您的同行旅伴", ["文化尋根 (歷史與文史客)", "品茗嗜啡 (熱愛茶與咖啡)", "親子踏青 (帶小孩)", "一人漫遊"])
    
    if st.button("🔍 尋找適合的部落體驗"):
        st.session_state['show_tours'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('show_tours'):
    st.markdown(f"**為「{group}」推薦的專屬導覽：**")
    recs = recommend_tours(group)
    for tour in recs:
        st.markdown(f"""
        <div class="tour-item">
            <div class="tour-title">{tour['name']}</div>
            <div style="margin: 6px 0;">
                <span class="tour-tag">⏱️ {tour['duration']}</span>
                <span class="tour-tag">💰 {tour['fee']}/人</span>
                <span class="tour-tag" style="background:#FFF0F5; color:#8B0000!important;">{tour['type']}</span>
            </div>
            <div style="font-size: 14px; color: #555; line-height: 1.5;">{tour['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 區塊 2：部落農創與茶香市集 ---
st.markdown("---")
st.markdown("### 🛍️ 舞鶴農創與撒奇萊雅市集")
st.markdown("<p style='font-size:14px; color:#5D4037;'>帶走世界級的蜜香紅茶，與撒奇萊雅族的文化記憶。</p>", unsafe_allow_html=True)

category_filter = st.radio("商品分類", ["全部", "🍵 茶葉與咖啡飲品", "🧵 文創與在地風味"], horizontal=True)

filtered_products = products_db
if category_filter == "🍵 茶葉與咖啡飲品":
    filtered_products = [p for p in products_db if p['category'] in ["茶葉飲品", "時令鮮果"]]
elif category_filter == "🧵 文創與在地風味":
    filtered_products = [p for p in products_db if p['category'] in ["文創工藝", "在地風味"]]

# 雙欄網格顯示 (已修復 Markdown 斷行 Bug，標籤同一行顯示)
cols = st.columns(2)
for i, product in enumerate(filtered_products):
    with cols[i % 2]:
        badge_html = '<div class="badge">熱銷</div>' if product.get('hot') else ''
        st.markdown(f"""
        <div class="product-card">
            {badge_html}<div style="font-size: 35px; margin-bottom:10px;">{product['icon']}</div>
            <span class="product-tag">{product['category']}</span>
            <div style="font-weight: 900; color: #3E2723; margin-top: 10px; font-size:16px;">{product['name']}</div>
            <div class="product-price">NT$ {product['price']}</div>
            <div style="font-size: 13px; color: #757575; margin-top: 8px; line-height:1.4;">{product['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 頁尾：導引購買與聯絡 ---
# ⚠️ 請將 href 裡的網址換成馬立雲部落或舞鶴在地協會的真實 LINE/粉專 連結
st.markdown("""
<div style="text-align:center; margin-top:40px; padding:25px; background: linear-gradient(180deg, #FAFAED 0%, #EFEBE9 100%); border-radius:15px; border: 1px solid #D7CCC8;">
    <h4 style="color:#7A0000 !important; font-weight:bold; margin-bottom:10px;">訂購特產 / 預約部落導覽</h4>
    <p style="font-size:14px; color:#5D4037; margin-bottom:25px;">支持原民部落創生，在地好茶與農產新鮮低溫宅配到府。</p>
    <a href="https://lin.ee/馬立雲專屬網址" target="_blank" style="text-decoration: none; display: inline-block; background-color:#DAA520; color:white; border:none; padding:12px 30px; border-radius:50px; font-weight:900; font-size: 16px; box-shadow: 0 4px 10px rgba(218, 165, 32, 0.4); cursor:pointer;">✉️ 聯繫部落官方 LINE</a>
</div>
""", unsafe_allow_html=True)
