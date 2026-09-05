import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from zoneinfo import ZoneInfo

# 한국 시간(KST) 기준 현재 시간 가져오기 함수
def get_kst_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="모두의 기록 - 1초 간편 기록",
    page_icon="⚡",
    layout="centered"
)


# =========================================================
# 폰트 매핑
# =========================================================

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


# =========================================================
# 세션 스테이트 초기화 (탭 유지 처리 포함)
# =========================================================

kst_now = get_kst_now()

if "selected_font" not in st.session_state:
    st.session_state.selected_font = "CookieRun (발랄하고 둥글둥글)"

if "log_data" not in st.session_state:
    st.session_state.log_data = [
        {
            "id": 1,
            "날짜": kst_now.strftime("%Y-%m-%d"),
            "항목": "☕ 커피 마신 잔수",
            "횟수": 2,
            "메모": "아아 마심",
            "시간": kst_now.strftime("%H:%M:%S")
        },
        {
            "id": 2,
            "날짜": kst_now.strftime("%Y-%m-%d"),
            "항목": "💪 운동 횟수",
            "횟수": 50,
            "메모": "스쿼트",
            "시간": kst_now.strftime("%H:%M:%S")
        }
    ]

if "selected_date" not in st.session_state:
    st.session_state.selected_date = kst_now.date()

if "is_editing" not in st.session_state:
    st.session_state.is_editing = False

if "current_count" not in st.session_state:
    st.session_state.current_count = 1

# 캘린더 날짜 클릭 시 메인 화면으로 튕기지 않고 캘린더 탭에 고정되도록 세션 상태 선제 설정
if "cal_date" in st.query_params or st.query_params.get("tab") == "cal":
    st.session_state.nav_selection = "📅 캘린더 (월간 보기)"

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "⚡ 바로 기록하기"


# =========================================================
# 현재 폰트
# =========================================================

current_font_css = font_mapping[
    st.session_state.selected_font
]


# =========================================================
# 폰트 로딩
# =========================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Do+Hyeon&family=Gaegu&family=Gowun+Batang&family=Gowun+Dodum&family=Gugi&family=IBM+Plex+Sans+KR:wght@300;400;600&family=Jua&family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@400;700&family=Nanum+Square:wght@400;700&family=Poor+Story&family=Sunflower:wght@300&display=swap'
    );

    @font-face {
        font-family: 'CookieRun-Regular';

        src: url(
            'https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2209-2@1.0/CookieRun-Regular.woff2'
        ) format('woff2');

        font-weight: normal;
        font-style: normal;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 전체 앱 스타일 및 모바일 최적화 CSS 적용
# =========================================================

st.markdown(
    f"""
    <style>

    html,
    body,
    p,
    span,
    div,
    label,
    input,
    textarea,
    select,
    button,
    option,
    [data-testid="stMarkdownContainer"],
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    [data-testid="stRadio"],
    [data-testid="stRadio"] * {{
        font-family: {current_font_css} !important;
    }}


    /* =====================================================
        모바일 화면 좌우 밀림/스크롤 완벽 차단
        ===================================================== */

    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        width: 100% !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }}

    .main .block-container {{
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 1rem !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }}


    /* =====================================================
        사이드바 제거
        ===================================================== */

    [data-testid="stSidebar"] {{
        display: none;
    }}


    /* =====================================================
        마크다운 제목 링크 차단
        ===================================================== */

    .stMarkdown a.header-anchor, 
    h3 a,
    h2 a,
    h1 a,
    a.anchor-link {{
        display: none !important;
        pointer-events: none !important;
    }}


    /* =====================================================
        제목 및 컨테이너 스타일
        ===================================================== */

    .main-title {{
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 0px;
    }}


    .sub-desc {{
        color: gray;
        font-size: 11px;
        margin-bottom: 12px;
    }}


    .today-banner {{
        background-color: rgba(33, 150, 243, 0.12);
        color: inherit;
        padding: 10px 10px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 12px;
        text-align: center;
        border: 1px solid rgba(33, 150, 243, 0.2);
    }}


    /* =====================================================
        Popover 내부 크기 및 아이콘 제거
        ===================================================== */

    [data-testid="stPopoverBody"] {{
        width: 300px !important;
        max-width: 90vw !important;
    }}

    [data-testid="stPopover"] button svg,
    [data-testid="stPopover"] button [data-testid="stIconMaterial"],
    [data-testid="stPopover"] button span[class*="material-symbols"] {{
        display: none !important;
    }}

    [data-testid="stPopover"] > button {{
        justify-content: center !important;
        gap: 0 !important;
    }}


    /* =====================================================
        폰트 선택 영역
        ===================================================== */

    .font-title {{
        font-size: 13px;
        font-weight: 600;
        margin-top: 6px;
        margin-bottom: 6px;
    }}


    .current-font {{
        background-color: rgba(128, 128, 128, 0.09);
        padding: 8px 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 13px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 상단 레이아웃
# =========================================================

top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    nav = st.radio(
        "화면 이동",
        [
            "⚡ 바로 기록하기",
            "📅 캘린더 (월간 보기)"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="nav_selection"
    )

with top_col2:
    with st.popover("⚙️ 설정", use_container_width=True):
        st.markdown("### 🎨 앱 설정")
        st.markdown(
            f"""
            <div class="current-font" style="font-family: {current_font_css} !important;">
                현재 폰트: <strong>{st.session_state.selected_font}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="font-title">폰트 선택 (15종)</div>', unsafe_allow_html=True)
        
        font_names = list(font_mapping.keys())
        selected_index = font_names.index(st.session_state.selected_font)
        selected_font = st.radio("폰트", font_names, index=selected_index, label_visibility="collapsed")

        if selected_font != st.session_state.selected_font:
            st.session_state.selected_font = selected_font
            st.rerun()


# 라디오 폰트 동적 적용
radio_font_css = ""
for i, font_css in enumerate(list(font_mapping.values())):
    radio_font_css += f'[data-testid="stPopoverBody"] [data-testid="stRadio"] > div > label:nth-child({i + 1}) div[data-testid="stMarkdownContainer"] {{ font-family: {font_css} !important; }}\n'

st.markdown(f"<style>{radio_font_css}</style>", unsafe_allow_html=True)
st.markdown("---")


# =========================================================
# 1. 바로 기록하기
# =========================================================

if nav == "⚡ 바로 기록하기":

    st.markdown('<p class="main-title">⚡ 무엇을 기록할까요?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">접속하자마자 1초 만에 기록하세요.</p>', unsafe_allow_html=True)

    current_kst = get_kst_now()
    today_str = current_kst.strftime("%Y년 %m월 %d일 (%a)")

    st.markdown(
        f"""
        <div class="today-banner">
            📅 오늘 날짜: {today_str}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("quick_log_form", clear_on_submit=False):
        category = st.selectbox(
            "기록 항목",
            [
                "☕ 커피 마신 잔수",
                "💪 운동 횟수",
                "💊 영양제 뽀개기",
                "💧 물 마신 컵",
                "📚 책 읽은 페이지",
                "✨ 직접 입력"
            ]
        )

        if category == "✨ 직접 입력":
            category = st.text_input("어떤 행동인가요?")

        st.write("📊 횟수 / 양 선택")

        count_input = st.number_input(
            "직접 입력",
            min_value=1,
            value=int(st.session_state.current_count),
            step=1,
            label_visibility="collapsed"
        )
        st.session_state.current_count = count_input

        c1, c2, c3, c4, c5 = st.columns(5)

        if c1.form_submit_button("-10", use_container_width=True):
            st.session_state.current_count = max(1, st.session_state.current_count - 10)
            st.rerun()
        if c2.form_submit_button("-5", use_container_width=True):
            st.session_state.current_count = max(1, st.session_state.current_count - 5)
            st.rerun()
        if c3.form_submit_button("-1", use_container_width=True):
            st.session_state.current_count = max(1, st.session_state.current_count - 1)
            st.rerun()
        if c4.form_submit_button("+5", use_container_width=True):
            st.session_state.current_count += 5
            st.rerun()
        if c5.form_submit_button("+10", use_container_width=True):
            st.session_state.current_count += 10
            st.rerun()

        memo = st.text_input("메모 (선택)", placeholder="특이사항 입력")
        submitted = st.form_submit_button("🚀 지금 바로 기록 저장", use_container_width=True)

        if submitted:
            save_kst = get_kst_now()
            now_time = save_kst.strftime("%H:%M:%S")
            new_id = max([item["id"] for item in st.session_state.log_data]) + 1 if st.session_state.log_data else 1

            new_entry = {
                "id": new_id,
                "날짜": save_kst.strftime("%Y-%m-%d"),
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
        today_date_str = get_kst_now().strftime("%Y-%m-%d")
        df_today = df[df["날짜"] == today_date_str]

        if not df_today.empty:
            display_df = df_today[["시간", "항목", "횟수", "메모"]].reset_index(drop=True)
            
            table_html = "<style>.log-table{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:5px;margin-bottom:10px;font-size:13px;}.log-table th{background-color:rgba(128,128,128,0.12);padding:8px 4px;text-align:center;border-bottom:2px solid rgba(128,128,128,0.2);font-weight:bold;}.log-table td{padding:8px 4px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.1);word-break:break-all;}</style><table class='log-table'><thead><tr><th>시간</th><th>항목</th><th>횟수</th><th>메모</th></tr></thead><tbody>"
            for _, row in display_df.iterrows():
                memo_val = row['메모'] if row['메모'] else '-'
                table_html += f"<tr><td>{row['시간']}</td><td>{row['항목']}</td><td>{row['횟수']}회</td><td>{memo_val}</td></tr>"
            table_html += "</tbody></table>"
            
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("오늘 아직 기록된 내역이 없습니다.")
    else:
        st.info("첫 기록을 남겨보세요!")


# =========================================================
# 2. 캘린더 (아이폰 스타일 표 캘린더 & 탭 유지)
# =========================================================

elif nav == "📅 캘린더 (월간 보기)":

    st.markdown('<p class="main-title">📅 월간 캘린더</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">날짜를 클릭하여 해당 날의 기록을 확인하고 편집하세요.</p>', unsafe_allow_html=True)

    col_y, col_m = st.columns(2)

    with col_y:
        selected_year = st.selectbox("연도", [2026, 2025, 2024], index=0)
    with col_m:
        selected_month = st.selectbox("월", list(range(1, 13)), index=get_kst_now().month - 1)

    st.markdown("---")

    if st.session_state.log_data:
        df_all = pd.DataFrame(st.session_state.log_data)
    else:
        df_all = pd.DataFrame(columns=["id", "날짜", "항목", "횟수", "메모", "시간"])

    # URL 쿼리 파라미터로 날짜 클릭 감지 (tab=cal 파라미터로 탭 이탈 방지)
    query_params = st.query_params
    if "cal_date" in query_params:
        try:
            clicked_date_str = query_params["cal_date"]
            if isinstance(clicked_date_str, list):
                clicked_date_str = clicked_date_str[0]
            st.session_state.selected_date = datetime.strptime(clicked_date_str, "%Y-%m-%d").date()
            st.session_state.is_editing = False
        except Exception:
            pass

    cal_obj = calendar.TextCalendar(firstweekday=6)
    cal = cal_obj.monthdayscalendar(selected_year, selected_month)
    weekdays = ["일", "월", "화", "수", "목", "금", "토"]
    sel_date_str = st.session_state.selected_date.strftime("%Y-%m-%d")

    # 아이폰 스타일 캘린더 CSS 및 링크 표시 보장 (tab=cal 추가)
    cal_html = """
    <style>
    .iphone-table {
        width: 100% !important;
        border-collapse: collapse !important;
        table-layout: fixed !important;
        margin-bottom: 15px !important;
        background: transparent !important;
        border: none !important;
    }
    .iphone-table th {
        text-align: center !important;
        font-weight: 500 !important;
        padding: 6px 0 10px 0 !important;
        font-size: 12px !important;
        border: none !important;
        background: transparent !important;
    }
    .iphone-table th:nth-child(1) { color: #ff3b30 !important; }
    .iphone-table th:nth-child(7) { color: #007aff !important; }
    .iphone-table th:not(:nth-child(1)):not(:nth-child(7)) { color: #8e8e93 !important; }

    .iphone-table td {
        text-align: center !important;
        padding: 6px 0 !important;
        vertical-align: middle !important;
        border: none !important;
        background: transparent !important;
    }

    .iphone-cell {
        display: inline-flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 34px !important;
        height: 34px !important;
        background-color: transparent !important;
        border-radius: 50% !important;
        color: inherit !important;
        text-decoration: none !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        margin: 0 auto !important;
        pointer-events: auto !important;
    }
    .iphone-cell:hover {
        background-color: rgba(128, 128, 128, 0.2) !important;
    }
    .iphone-cell.selected {
        background-color: #ff3b30 !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    .ios-sun { color: #ff3b30 !important; }
    .ios-sat { color: #007aff !important; }
    
    .ios-dot {
        width: 3px !important;
        height: 3px !important;
        background-color: #ff3b30 !important;
        border-radius: 50% !important;
        margin-top: 1px !important;
    }
    .iphone-cell.selected .ios-dot {
        background-color: #ffffff !important;
    }
    </style>

    <table class='iphone-table'>
        <thead>
            <tr>
    """
    for w in weekdays:
        cal_html += f"<th>{w}</th>"
    cal_html += "</tr></thead><tbody>"

    for week in cal:
        cal_html += "<tr>"
        for day_idx, day in enumerate(week):
            if day == 0:
                cal_html += "<td></td>"
            else:
                cur_d_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
                has_log = False
                if not df_all.empty and "날짜" in df_all.columns:
                    has_log = not df_all[df_all["날짜"] == cur_d_str].empty
                
                dot_html = "<div class='ios-dot'></div>" if has_log else "<div style='height: 3px; margin-top: 1px; visibility: hidden;'>•</div>"
                btn_cls = "iphone-cell selected" if cur_d_str == sel_date_str else "iphone-cell"
                
                day_cls = ""
                if day_idx == 0:
                    day_cls = " ios-sun"
                elif day_idx == 6:
                    day_cls = " ios-sat"

                cal_html += f"<td><a href='?cal_date={cur_d_str}&tab=cal' target='_self' class='{btn_cls}'><span class='{day_cls}'>{day}</span>{dot_html}</a></td>"
        cal_html += "</tr>"
    cal_html += "</tbody></table>"

    st.markdown(cal_html, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"### 📌 선택한 날짜: {sel_date_str}")

    if not df_all.empty and "날짜" in df_all.columns:
        df_target = df_all[df_all["날짜"] == sel_date_str]
    else:
        df_target = pd.DataFrame()

    if not df_target.empty:
        st.write("📋 **이날의 기록 목록** (삭제할 항목을 선택하세요)")
        selected_ids_to_delete = []

        for _, row in df_target.iterrows():
            time_str = row.get("시간", "시간 미상")
            memo_str = row.get("메모", "없음")
            row_id = row.get("id")
            item_label = f"[{time_str}] {row['항목']}: {row['횟수']}회 (메모: {memo_str})"

            if st.checkbox(item_label, key=f"chk_{row_id}"):
                selected_ids_to_delete.append(row_id)

        st.markdown("<br>", unsafe_allow_html=True)

        if selected_ids_to_delete:
            if st.button("🗑️ 선택한 기록 삭제", use_container_width=True):
                st.session_state.log_data = [
                    item for item in st.session_state.log_data if item["id"] not in selected_ids_to_delete
                ]
                st.success("선택한 기록이 삭제되었습니다.")
                st.rerun()
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
            add_category = st.selectbox(
                "항목",
                [
                    "☕ 커피 마신 잔수",
                    "💪 운동 횟수",
                    "💊 영양제 뽀개기",
                    "💧 물 마신 컵",
                    "📚 책 읽은 페이지",
                    "✨ 직접 입력"
                ]
            )
            if add_category == "✨ 직접 입력":
                add_category = st.text_input("직접 입력")

            add_count = st.number_input("횟수 / 양", min_value=1, value=1)
            add_memo = st.text_input("메모")

            col_sub1, col_sub2 = st.columns(2)
            submit_added = col_sub1.form_submit_button("저장하기", use_container_width=True)
            cancel_edit = col_sub2.form_submit_button("닫기", use_container_width=True)

            if submit_added:
                save_kst = get_kst_now()
                now_time = save_kst.strftime("%H:%M:%S")
                new_id = max([item["id"] for item in st.session_state.log_data]) + 1 if st.session_state.log_data else 1

                new_entry = {
                    "id": new_id,
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


# =========================================================
# 광고 영역
# =========================================================

html_ad = """
<div style="
    background-color: rgba(128, 128, 128, 0.08);
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    color: #868e96;
    font-size: 11px;
    margin-top: 20px;
    border: 1px dashed rgba(128, 128, 128, 0.2);
">
    📢 [광고 영역] 구글 애드센스 배너가 들어갈 자리입니다.
</div>
"""
st.markdown(html_ad, unsafe_allow_html=True)
