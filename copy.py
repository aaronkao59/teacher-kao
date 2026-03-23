import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 (符合 UIUX-CRF v9.0 認知架構) ---
st.set_page_config(
    page_title="Kaolahan - Sawmah 旓瑪赫赫", 
    page_icon="💖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (導入預測性熱圖優化與霓虹高對比) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&family=Noto+Sans+TC:wght@300;500;700&display=swap');

    .stApp { 
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(255, 0, 128, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        font-family: 'Noto Sans TC', sans-serif;
        color: #FFFFFF;
    }
    
    /* Header 強化：Sawmah 專屬識別碼 */
    .header-container {
        background: rgba(10, 10, 10, 0.95);
        border: 2px solid #FF0080;
        box-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #FF0080, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 900;
        text-shadow: 0 0 15px rgba(255, 0, 128, 0.6);
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 8px 20px; 
        background: rgba(0, 229, 255, 0.1); 
        color: #00E5FF;
        border: 1px solid #00E5FF;
        font-weight: bold;
        clip-path: polygon(10% 0, 100% 0, 90% 100%, 0 100%);
    }

    /* 卡片設計優化：降低認知摩擦 */
    .word-card {
        background: rgba(25, 25, 25, 0.9);
        border: 1px solid #444;
        border-left: 5px solid #FF0080; 
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        border-radius: 4px;
    }

    .word-card:hover { 
        border-color: #00E5FF;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
    }

    .sentence-box {
        background: #0f0f0f;
        padding: 20px;
        border-right: 3px solid #00E5FF;
        border-left: 3px solid #FF0080;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料封裝 ---
VOCABULARY = [
    {"amis": "kaolahan",  "zh": "所喜歡的",   "emoji": "💖", "file": "v_kaolahan"},
    {"amis": "facidol",   "zh": "麵包樹果",   "emoji": "🍈", "file": "v_facidol"},
    {"amis": "haca",      "zh": "也",         "emoji": "➕", "file": "v_haca"},
    {"amis": "maemin",    "zh": "全部",       "emoji": "👐", "file": "v_maemin"},
    {"amis": "sikaen",    "zh": "菜餚",       "emoji": "🍱", "file": "v_sikaen"},
    {"amis": "dateng",    "zh": "菜",         "emoji": "🥬", "file": "v_dateng"},
    {"amis": "kohaw",     "zh": "湯",         "emoji": "🥣", "file": "v_kohaw"},
    {"amis": "mato'asay", "zh": "老人",       "emoji": "👵", "file": "v_matoasay"},
]

SENTENCES = [
    {"amis": "O maan ko kaolahan iso a sikaen?", "zh": "你喜歡什麼樣的菜呢？", "file": "s_o_maan_ko_kaolahan"},
    {"amis": "O foting ko kaolahan ako a dateng.", "zh": "魚是我最喜歡的菜。", "file": "s_o_foting_ko_kaolahan"},
    {"amis": "Kaolahan no wama konini a kohaw.", "zh": "這碗是爸爸最喜歡的湯。", "file": "s_kaolahan_no_wama"},
    {"amis": "Tadakaolahan no mato'asay kona dateng.", "zh": "這些是老人家最喜歡的菜。", "file": "s_tadakaolahan_no_matoasay"},
    {"amis": "Kaolahan ako a maemin konini a sikaen.", "zh": "這些都是我最喜歡的菜餚。", "file": "s_kaolahan_ako_a_maemin"},
    {"amis": "O facidol i, o tadakaolahan haca no 'Amis.", "zh": "麵包樹果也是阿美族人最愛。", "file": "s_o_facidol_i"},
]

QUIZ_DATA = [
    {"q": "O maan ko ______ iso a sikaen?", "ans": "kaolahan", "opts": ["kaolahan", "facidol", "haca"]},
    {"q": "______ no wama konini a kohaw", "ans": "Kaolahan", "opts": ["Kaolahan", "Maemin", "Dateng"]},
    {"q": "O ______ i, o tadakaolahan haca", "ans": "facidol", "opts": ["facidol", "kohaw", "sikaen"]},
]

# --- 2. 核心邏輯 (防禦性解析) ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['m4a', 'mp3', 'wav']:
            path = os.path.join('audio', f"{filename_base}.{ext}")
            if os.path.exists(path):
                st.audio(path)
                return 
    try:
        tts = gTTS(text=text.split('/')[0], lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except:
        st.warning("⚠️ 語音系統離線")

def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    st.session_state.quiz_pool = random.sample(QUIZ_DATA, len(QUIZ_DATA))

if 'score' not in st.session_state:
    init_quiz()

# --- 3. 介面渲染 ---
def main():
    # Header - 講師資訊更新
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">KAOLAHAN</h1>
        <div style="color:#00E5FF; letter-spacing:5px;">SAWMAH EDITION</div>
        <div class="teacher-tag">講師：Sawmah 旓瑪赫赫</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📚 智慧學習", "⚡ 模擬測驗"])
    
    with tab1:
        st.markdown("### // 單字庫系統")
        cols = st.columns(2)
        for idx, item in enumerate(VOCABULARY):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="word-card">
                    <div style="font-size:30px;">{item['emoji']}</div>
                    <h3 style="color:#00E5FF;">{item['amis']}</h3>
                    <p style="color:#AAA;">{item['zh']}</p>
                </div>
                """, unsafe_allow_html=True)
                play_audio(item['amis'], item['file'])
        
        st.markdown("---")
        st.markdown("### // 語境解析")
        for s in SENTENCES:
            st.markdown(f"""
            <div class="sentence-box">
                <div style="color:#FF0080; font-weight:bold;">{s['amis']}</div>
                <div style="color:#EEE; font-size:14px;">{s['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(s['amis'], s['file'])

    with tab2:
        if st.session_state.current_q < len(st.session_state.quiz_pool):
            q = st.session_state.quiz_pool[st.session_state.current_q]
            st.markdown(f"#### 問題 {st.session_state.current_q + 1}:")
            st.info(q['q'])
            
            cols = st.columns(3)
            for i, opt in enumerate(q['opts']):
                if cols[i].button(opt):
                    if opt.lower() == q['ans'].lower():
                        st.success("✅ 數據匹配成功")
                        st.session_state.score += 1
                    else:
                        st.error("❌ 存取被拒")
                    time.sleep(0.5)
                    st.session_state.current_q += 1
                    st.rerun()
        else:
            st.markdown(f"## 任務完成！得分: {st.session_state.score}")
            if st.button("重啟系統"):
                init_quiz()
                st.rerun()

if __name__ == "__main__":
    main()
