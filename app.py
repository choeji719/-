import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정 (와이드 모드 대신 깔끔한 중앙 정렬 폼)
st.set_page_config(page_title="모두의 기록 - 1초 만에 남기는 일상 횟수", page_icon="⚡", layout="centered")

# 커스텀 CSS로 UI를 더 직관적이고 앱처럼 보이게 꾸미기
st.markdown("""
    <style>
    .main-title {
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-desc {
        color: gray;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 스테이트 초기화 (데이터 저장용)
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

# 상단 네비게이션 (뒤로가기/전환을 직관적으로 구현)
nav = st.radio("화면 이동", ["⚡ 바로 기록하기", "📅 캘린더 (날짜별 모아보기)"], horizontal=True, label_visibility="collapsed")

st.markdown("---")

# 1. 접속하자마자 보이는 '바로 기록하기' 화면
if nav == "⚡ 바로 기록하기":
    st.markdown('<p class="main-title">⚡ 무엇을 기록할까요?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">복잡한 메뉴 없이, 들어오자마자 바로 남기세요.</p>', unsafe_allow_html=True)

    with st.form("quick_log_form", clear_on_submit=True):
        # 날짜 기본값은 오늘
        date_input = st.date_input("기록 날짜", value=datetime.now())
        
        # 기록할 항목 (커피, 운동, 영양제 등 자유 입력 또는 선택)
        category = st.selectbox(
            "기록 항목", 
            ["☕ 커피 마신 잔수", "💪 운동 횟수", "💊 영양제 뽀개기", "💧 물 마신 컵", "📚 책 읽은 페이지", "✨ 직접 입력"]
        )
        if category == "✨ 직접 입력":
            category = st.text_input("어떤 행동인가요?", placeholder="예: 스쿼트, 영양제 등")
            
        count = st.number_input("횟수 / 양", min_value=1, value=1, step=1)
        memo = st.text_input("메모 (선택)", placeholder="특이사항이나 간단한 메모")
        
        submitted = st.form_submit_button("🚀 1초 만에 기록 저장", use_container_width=True)
        
        if submitted:
            new_entry = {
                "날짜": date_input.strftime("%Y-%m-%d"),
                "항목": category,
                "횟수": count,
                "메모": memo,
                "시간": datetime.now().strftime("%H:%M")
            }
            st.session_state.log_data.append(new_entry)
            st.success("✅ 저장 완료! 아래에서 바로 확인할 수 있어요.")

    st.markdown("### 📋 오늘의 실시간 기록")
    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        today_str = datetime.now().strftime("%Y-%m-%d")
        df_today = df[df["날짜"] == today_str]
        
        if not df_today.empty:
            st.dataframe(df_today.iloc[::-1].reset_index(drop=True), use_container_width=True)
        else:
            st.info("오늘 아직 기록된 내역이 없습니다.")
    else:
        st.info("첫 기록을 남겨보세요!")

# 2. 달력 및 과거 기록 조회 화면
elif nav == "📅 캘린더 (날짜별 모아보기)":
    st.markdown('<p class="main-title">📅 날짜별 기록 캘린더</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-desc">과거의 오늘, 어떤 기록을 남겼는지 확인해보세요.</p>', unsafe_allow_html=True)

    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        
        # 날짜 목록 추출 (최신순)
        available_dates = sorted(df["날짜"].unique(), reverse=True)
        
        selected_date = st.selectbox("조회할 날짜를 선택하세요", available_dates)
        
        # 선택한 날짜의 데이터 필터링
        df_selected = df[df["날짜"] == selected_date]
        
        st.markdown(f"### 📌 {selected_date}의 기록 모음")
        st.dataframe(df_selected.reset_index(drop=True), use_container_width=True)
        
        # 간단 통계
        total_logs = len(df_selected)
        st.metric("이 날의 총 기록 횟수", f"{total_logs}건")
        
        if st.button("전체 데이터 초기화"):
            st.session_state.log_data = []
            st.rerun()
    else:
        st.info("아직 저장된 과거 기록이 없습니다.")

# ==========================================
# 3. 미래의 수익화를 위한 하단 광고 영역 (플레이스홀더)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
# 광고 영역 시각화 박스 (나중에 구글 애드센스 HTML 코드로 대체할 수 있는 공간)
st.markdown(
    """
    <div style="background-color: #f1f3f5; padding: 15px; border-radius: 8px; text-align: center; color: #868e96; font-size: 13px;">
        📢 [광고 영역] 구글 애드센스 배너가 들어갈 자리입니다.<br>
        (트래픽이 모이면 광고를 붙여 수익을 창출할 수 있습니다.)
    </div>
    """, 
    unsafe_allow_html=True
)
