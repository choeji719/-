import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 페이지 설정
st.set_page_config(page_title="모두의 기록 - 애플 스타일 캘린더", page_icon="📅", layout="centered")

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
        # 테스트용 초기 데이터 예시
        {"id": 1, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "☕ 커피 마신 잔수", "횟수": 2, "메모": "아아 마심"},
        {"id": 2, "날짜": datetime.now().strftime("%Y-%m-%d"), "항목": "💪 운동 횟수", "횟수": 50, "메모": "스쿼트"}
    ]

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

if 'is_editing' not in st.session_state:
    st.session_state.is_editing = False

# 상단 네비게이션
nav = st.radio("화면 이동", ["⚡ 바로 기록하기", "📅 캘린더 (월간 보기)"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

# 1. 바로 기록하기 화면
if nav == "⚡ 바로 기록하기":
    st.markdown('<p class="main-title">⚡ 무엇을 기록할까요?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">접속하자마자 1초 만에 기록하세요.</p>', unsafe_allow_html=True)

    with st.form("quick_log_form", clear_on_submit=True):
        date_input = st.date_input("기록 날짜", value=datetime.now())
        category = st.selectbox(
            "기록 항목", 
            ["☕ 커피 마신 잔수", "💪 운동 횟수", "💊 영양제 뽀개기", "💧 물 마신 컵", "📚 책 읽은 페이지", "✨ 직접 입력"]
        )
        if category == "✨ 직접 입력":
            category = st.text_input("어떤 행동인가요?")
            
        count = st.number_input("횟수 / 양", min_value=1, value=1, step=1)
        memo = st.text_input("메모 (선택)", placeholder="특이사항 입력")
        
        submitted = st.form_submit_button("🚀 기록 저장", use_container_width=True)
        
        if submitted:
            new_entry = {
                "id": len(st.session_state.log_data) + 1,
                "날짜": date_input.strftime("%Y-%m-%d"),
                "항목": category,
                "횟수": count,
                "메모": memo
            }
            st.session_state.log_data.append(new_entry)
            st.success("✅ 저장되었습니다!")

    st.markdown("### 📋 오늘의 실시간 기록")
    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        today_str = datetime.now().strftime("%Y-%m-%d")
        df_today = df[df["날짜"] == today_str]
        if not df_today.empty:
            st.dataframe(df_today[["항목", "횟수", "메모"]], use_container_width=True)
        else:
            st.info("오늘 기록이 없습니다.")

# 2. 애플 캘린더 스타일 화면
elif nav == "📅 캘린더 (월간 보기)":
    st.markdown('<p class="main-title">📅 월간 캘린더</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">날짜를 클릭하여 해당 날의 기록을 확인하고 편집하세요.</p>', unsafe_allow_html=True)

    # 연도 및 월 선택 컨트롤
    col_y, col_m = st.columns(2)
    with col_y:
        selected_year = st.selectbox("연도", [2026, 2025, 2024], index=0)
    with col_m:
        selected_month = st.selectbox("월", list(range(1, 13)), index=datetime.now().month - 1)

    st.markdown("---")

    # 애플 캘린더 스타일의 월간 그리드 출력
    cal = calendar.monthcalendar(selected_year, selected_month)
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    
    # 요일 헤더 표시
    cols = st.columns(7)
    for i, day_name in enumerate(weekdays):
        cols[i].markdown(f"<div style='text-align: center; font-weight: bold; color: #6c757d;'>{day_name}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 날짜별 기록 데이터 준비
    df_all = pd.DataFrame(st.session_state.log_data) if st.session_state.log_data else pd.DataFrame(columns=["날짜", "항목", "횟수", "메모"])

    # 날짜 버튼 그리드 생성
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].markdown("") # 빈 날짜
            else:
                current_date_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
                
                # 해당 날짜에 기록이 있는지 확인
                has_log = False
                if not df_all.empty and "날짜" in df_all.columns:
                    has_log = not df_all[df_all["날짜"] == current_date_str].empty
                
                # 버튼 레이블 (기록이 있으면 이모지 표시)
                btn_label = f"{day} •" if has_log else f"{day}"
                
                # 날짜 버튼 클릭 시
                if cols[i].button(btn_label, key=f"date_{current_date_str}", use_container_width=True):
                    st.session_state.selected_date = date(selected_year, selected_month, day)
                    st.session_state.is_editing = False # 날짜를 바르면 편집 모드 초기화

    st.markdown("---")

    # ==========================================
    # 선택한 날짜의 상세 팝업 영역 (하단 카드)
    # ==========================================
    sel_date_str = st.session_state.selected_date.strftime("%Y-%m-%d")
    st.markdown(f"### 📌 선택한 날짜: {sel_date_str}")

    with st.container():
        st.markdown('<div class="popup-box">', unsafe_allow_html=True)
        
        # 해당 날짜 데이터 필터링
        df_target = df_all[df_all["날짜"] == sel_date_str] if not df_all.empty and "날짜" in df_all.columns else pd.DataFrame()

        if not df_target.empty:
            st.write("📋 **이날의 기록 목록**")
            for idx, row in df_target.iterrows():
                col_info1, col_info2 = st.columns([3, 1])
                col_info1.text(f"• {row['항목']}: {row['횟수']}회 (메모: {row.get('memo', row.get('메모', '없음'))})")
                
                # 삭제 버튼 등 추가 가능
        else:
            st.info("이 날짜에는 아직 기록이 없습니다.")

        st.markdown("<br>", unsafe_allow_html=True)

        # '편집/추가' 토글 버튼
        if not st.session_state.is_editing:
            if st.button("✏️ 이 날짜에 기록 추가 / 편집하기", use_container_width=True):
                st.session_state.is_editing = True
                st.rerun()
        else:
            st.markdown("#### ➕ 항목 추가하기")
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
                    new_entry = {
                        "id": len(st.session_state.log_data) + 1,
                        "날짜": sel_date_str,
                        "항목": add_category,
                        "횟수": add_count,
                        "메모": add_memo
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
