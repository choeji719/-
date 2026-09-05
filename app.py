import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 페이지 설정
st.set_page_config(page_title="모두의 기록 - 1초 간편 기록", page_icon="⚡", layout="centered")

# 깔끔한 모바일 앱 감성 CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-desc {
        color: gray;
        font-size: 13px;
        margin-bottom: 15px;
    }
    .today-banner {
        background-color: #e7f5ff;
        color: #1971c2;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    .popup-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 스테이트 초기화 (데이터 저장용)
if 'log_data' not in st.session_state:
    st.session_state.log_data = [
        {"id": 1, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "☕ 커피 마신 잔수", "횟수": 2, "메모": "아아 마심", "시간": datetime.now().strftime("%H:%M:%S")},
        {"id": 2, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "💪 운동 횟수", "횟수": 50, "메모": "스쿼트", "시간": datetime.now().strftime("%H:%M:%S")}
    ]

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

if 'is_editing' not in st.session_state:
    st.session_state.is_editing = False

# 상단 네비게이션
nav = st.radio("화면 이동", ["⚡ 바로 기록하기", "📅 캘린더 (월간 보기)"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

# 1. 바로 기록하기 화면 (오늘 날짜 고정 및 퀵 조절 버튼 적용)
if nav == "⚡ 바로 기록하기":
    st.markdown('<p class="main-title">⚡ 무엇을 기록할까요?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">접속하자마자 1초 만에 기록하세요.</p>', unsafe_allow_html=True)

    # 오늘 날짜 안내 배너
    today_str = datetime.now().strftime("%Y년 %m월 %d일 (%a)")
    st.markdown(f'<div class="today-banner">📅 오늘 날짜: {today_str}</div>', unsafe_allow_html=True)

    if 'current_count' not in st.session_state:
        st.session_state.current_count = 1

    with st.form("quick_log_form", clear_on_submit=False):
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
            # 먼저 기록한 것이 위로 오도록 정렬 (역순 정렬 제거)
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
        cols[i].markdown(f"<div style='text-align: center; font-weight: bold; color: #6c757d;'>{day_name}</div>", unsafe_allow_html=True)

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
<div style="background-color: #f1f3f5; padding: 15px; border-radius: 8px; text-align: center; color: #868e96; font-size: 13px; margin-top: 30px;">
    📢 [광고 영역] 구글 애드센스 배너가 들어갈 자리입니다.
</div>
"""
st.markdown(html_ad, unsafe_allow_html=True)
