import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 페이지 설정
st.set_page_config(page_title="모두의 기록 - 1초 간편 기록", page_icon="⚡", layout="centered")

# 세션 스테이트 초기화
if 'selected_font' not in st.session_state:
    st.session_state.selected_font = "CookieRun (발랄하고 둥글둥글)"

if 'log_data' not in st.session_state:
    st.session_state.log_data = [
        {"id": 1, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "☕ 커피 마신 잔수", "횟수": 2, "메모": "아아 마심", "시간": datetime.now().strftime("%H:%M:%S")},
        {"id": 2, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "💪 운동 횟수", "횟수": 50, "메모": "스쿼트", "시간": datetime.now().strftime("%H:%M:%S")}
    ]

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

if 'is_editing' not in st.session_state:
    st.session_state.is_editing = False

if 'current_count' not in st.session_state:
    st.session_state.current_count = 1

# 15가지 폰트 매핑
font_mapping = {
    "CookieRun (발랄하고 둥글둥글)": "'CookieRun-Regular', sans-serif",
    "Jua (귀여운 둥근고딕)": "'Jua', sans-serif",
    "Do Hyeon (레트로 둥근고딕)": "'Do Hyeon', sans-serif",
    "Sunflower (부드러운 손글씨)": "'Sunflower', sans-serif",
    "Poor Story (동화책 손글씨)": "'Poor Story', cursive",
    "Gaegu (귀여운 손글씨)": "'Gaegu', cursive",
    "IBM Plex Sans KR (부드러운 고딕)": "'IBM Plex Sans KR', sans-serif",
    "Pretendard (기본 모던)": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "NanumSquare (깔끔하고 단정함)": "'NanumSquare', sans-serif",
    "Nanum Gothic (나눔고딕)": "'Nanum Gothic', sans-serif",
    "Nanum Myeongjo (나눔명조)": "'Nanum Myeongjo', serif",
    "Black Han Sans (굵고 강렬함)": "'Black Han Sans', sans-serif",
    "Gowun Dodum (부드러운 돋움)": "'Gowun Dodum', sans-serif",
    "Gowun Batang (부드러운 바탕)": "'Gowun Batang', serif",
    "Gugi (독특한 픽셀/레트로)": "'Gugi', cursive"
}

current_font_css = font_mapping.get(st.session_state.selected_font, "-apple-system, sans-serif")

# 드롭다운(포털 메뉴) 내부 각 항목별 개별 폰트 실시간 적용 CSS 생성
dropdown_font_css = ""
for idx, (f_name, f_css) in enumerate(font_mapping.items(), 1):
    dropdown_font_css += f"""
    div[data-baseweb="menu"] li[role="option"]:nth-child({idx}),
    div[data-baseweb="menu"] li[role="option"]:nth-child({idx}) * {{
        font-family: {f_css} !important;
        font-size: 15px !important;
    }}
    """

# CSS 주입
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Do+Hyeon&family=Gaegu&family=Gowun+Batang&family=Gowun+Dodum&family=Gugi&family=IBM+Plex+Sans+KR:wght@300;400;600&family=Jua&family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@400;700&family=Nanum+Square:wght@400;700&family=Poor+Story&family=Sunflower:wght@300&display=swap');
    @import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2209-2@1.0/CookieRun-Regular.woff2');

    @font-face {{
        font-family: 'CookieRun-Regular';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2209-2@1.0/CookieRun-Regular.woff2') format('woff2');
        font-weight: normal;
        font-style: normal;
    }}

    /* 앱 전체 주요 텍스트에 선택된 폰트 적용 (아이콘 태그 제외) */
    .stApp p, .stApp span:not([class*="material"]):not([data-testid="stIcon"]), .stApp div, .stApp label, .stApp input, .stApp textarea, .stApp select, .stApp button, .stMarkdown {{
        font-family: {current_font_css} !important;
    }}

    /* ⭐ 'expand_more' 및 Streamlit 내부 아이콘 깨짐(글자 노출) 방지 완벽 보호 */
    .material-icons, 
    .material-symbols-rounded, 
    [data-testid="stIcon"], 
    span[class*="material"], 
    i[class*="icon"],
    svg {{
        font-family: inherit !important;
    }}

    /* ⭐ 드롭다운 목록 개별 폰트 스타일 매핑 */
    {dropdown_font_css}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    .main-title {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 0px;
    }}
    .sub-desc {{
        color: gray;
        font-size: 13px;
        margin-bottom: 15px;
    }}
    .today-banner {{
        background-color: rgba(33, 150, 243, 0.12);
        color: inherit;
        padding: 12px 15px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid rgba(33, 150, 243, 0.2);
    }}
    .popup-box {{
        background-color: rgba(128, 128, 128, 0.08);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-top: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# 상단 레이아웃: 왼쪽은 화면 이동 탭, 오른쪽은 ⚙️ 설정 팝오버 버튼
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    nav = st.radio("화면 이동", ["⚡ 바로 기록하기", "📅 캘린더 (월간 보기)"], horizontal=True, label_visibility="collapsed")

with top_col2:
    with st.popover("⚙️ 설정", use_container_width=True):
        st.markdown("#### 🎨 앱 설정")
        selected = st.selectbox(
            "폰트 선택 (15종)", 
            list(font_mapping.keys()), 
            index=list(font_mapping.keys()).index(st.session_state.selected_font)
        )

        if selected != st.session_state.selected_font:
            st.session_state.selected_font = selected
            st.rerun()

st.markdown("---")

# 1. 바로 기록하기 화면
if nav == "⚡ 바로 기록하기":
    st.markdown('<p class="main-title">⚡ 무엇을 기록할까요?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">접속하자마자 1초 만에 기록하세요.</p>', unsafe_allow_html=True)

    today_str = datetime.now().strftime("%Y년 %m월 %d일 (%a)")
    st.markdown(f'<div class="today-banner">📅 오늘 날짜: {today_str}</div>', unsafe_allow_html=True)

    category = st.selectbox(
        "기록 항목", 
        ["☕ 커피 마신 잔수", "💪 운동 횟수", "💊 영양제 뽀개기", "💧 물 마신 컵", "📚 책 읽은 페이지", "✨ 직접 입력"]
    )
    if category == "✨ 직접 입력":
        category = st.text_input("어떤 행동인가요?")
        
    st.write("📊 횟수 / 양 선택")
    count_input = st.number_input("직접 입력", min_value=1, value=int(st.session_state.current_count), step=1, label_visibility="collapsed")
    st.session_state.current_count = count_input

    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("-10", use_container_width=True):
        st.session_state.current_count = max(1, st.session_state.current_count - 10)
        st.rerun()
    if c2.button("-5", use_container_width=True):
        st.session_state.current_count = max(1, st.session_state.current_count - 5)
        st.rerun()
    if c3.button("-1", use_container_width=True):
        st.session_state.current_count = max(1, st.session_state.current_count - 1)
        st.rerun()
    if c4.button("+5", use_container_width=True):
        st.session_state.current_count += 5
        st.rerun()
    if c5.button("+10", use_container_width=True):
        st.session_state.current_count += 10
        st.rerun()

    with st.form("quick_log_form", clear_on_submit=False):
        memo = st.text_input("메모 (선택)", placeholder="특이사항 입력")
        submitted = st.form_submit_button("🚀 지금 바로 기록 저장", use_container_width=True)
        
        if submitted:
            now_time = datetime.now().strftime("%H:%M:%S")
            new_entry = {
                "id": len(st.session_state.log_data) + 1,
                "날짜": datetime.now().strftime("%Y-%m-%d"),
                "항목": category,
                "횟수": st.session_state.current_count,
                "메모": memo,
                "시간": now_time
            }
            st.session_state.log_data.append(new_entry)
            st.success(f"✅ 저장 완료! ({now_time})")
            st.session_state.current_count = 1

    st.markdown("### 📋 오늘의 실시간 기록")
    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        today_date_str = datetime.now().strftime("%Y-%m-%d")
        df_today = df[df["날짜"] == today_date_str]
        
        if not df_today.empty:
            display_df = df_today[["시간", "항목", "횟수", "메모"]].reset_index(drop=True)
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("오늘 아직 기록된 내역이 없습니다.")
    else:
        st.info("첫 기록을 남겨보세요!")

# 2. 애플 캘린더 스타일 화면
elif nav == "📅 캘린더 (월간 보기)":
    st.markdown('<p class="main-title">📅 월간 캘린더</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">날짜를 클릭하여 해당 날의 기록을 확인하고 편집하세요.</p>', unsafe_allow_html=True)

    col_y, col_m = st.columns(2)
    with col_y:
        selected_year = st.selectbox("연도", [2026, 2025, 2024], index=0)
    with col_m:
        selected_month = st.selectbox("월", list(range(1, 13)), index=datetime.now().month - 1)

    st.markdown("---")

    cal = calendar.monthcalendar(selected_year, selected_month)
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    
    cols = st.columns(7)
    for i, day_name in enumerate(weekdays):
        cols[i].markdown(f"<div style='text-align: center; font-weight: bold; color: #868e96;'>{day_name}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    df_all = pd.DataFrame(st.session_state.log_data) if st.session_state.log_data else pd.DataFrame(columns=["날짜", "항목", "횟수", "메모", "시간"])

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].markdown("")
            else:
                current_date_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
                has_log = False
                if not df_all.empty and "날짜" in df_all.columns:
                    has_log = not df_all[df_all["날짜"] == current_date_str].empty
                
                btn_label = f"{day} •" if has_log else f"{day}"
                
                if cols[i].button(btn_label, key=f"date_{current_date_str}", use_container_width=True):
                    st.session_state.selected_date = date(selected_year, selected_month, day)
                    st.session_state.is_editing = False

    st.markdown("---")

    sel_date_str = st.session_state.selected_date.strftime("%Y-%m-%d")
    st.markdown(f"### 📌 선택한 날짜: {sel_date_str}")

    with st.container():
        st.markdown('<div class="popup-box">', unsafe_allow_html=True)
        
        df_target = df_all[df_all["날짜"] == sel_date_str] if not df_all.empty and "날짜" in df_all.columns else pd.DataFrame()

        if not df_target.empty:
            st.write("📋 **이날의 기록 목록**")
            for idx, row in df_target.iterrows():
                time_str = row.get('시간', '시간 미상')
                st.text(f"[{time_str}] {row['항목']}: {row['횟수']}회 (메모: {row.get('메모', '없음')})")
        else:
            st.info("이 날짜에는 아직 기록이 없습니다.")

        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.is_editing:
            if st.button("✏️ 이 날짜에 기록 추가하기", use_container_width=True):
                st.session_state.is_editing = True
                st.rerun()
        else:
            st.markdown("#### ➕ 과거 날짜 기록 추가")
            with st.form(f"edit_form_{sel_date_str}", clear_on_submit=True):
                add_category = st.selectbox("항목", ["☕ 커피 마신 잔수", "💪 운동 횟수", "💊 영양제 뽀개기", "💧 물 마신 컵", "📚 책 읽은 페이지", "✨ 직접 입력"])
                if add_category == "✨ 직접 입력":
                    add_category = st.text_input("직접 입력")
                add_count = st.number_input("횟수 / 양", min_value=1, value=1)
                add_memo = st.text_input("메모")
                
                col_sub1, col_sub2 = st.columns(2)
                submit_added = col_sub1.form_submit_button("저장하기", use_container_width=True)
                cancel_edit = col_sub2.form_submit_button("닫기", use_container_width=True)
                
                if submit_added:
                    now_time = datetime.now().strftime("%H:%M:%S")
                    new_entry = {
                        "id": len(st.session_state.log_data) + 1,
                        "날짜": sel_date_str,
                        "항목": add_category,
                        "횟수": add_count,
                        "메모": add_memo,
                        "시간": now_time
                    }
                    st.session_state.log_data.append(new_entry)
                    st.session_state.is_editing = False
                    st.success("추가되었습니다!")
                    st.rerun()
                    
                if cancel_edit:
                    st.session_state.is_editing = False
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# 하단 광고 영역
html_ad = """
<div style="background-color: rgba(128, 128, 128, 0.08); padding: 15px; border-radius: 12px; text-align: center; color: #868e96; font-size: 13px; margin-top: 30px; border: 1px dashed rgba(128, 128, 128, 0.2);">
    📢 [광고 영역] 구글 애드센스 배너가 들어갈 자리입니다.
</div>
"""
st.markdown(html_ad, unsafe_allow_html=True)
