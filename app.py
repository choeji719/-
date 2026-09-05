import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="홈트 기록장", page_icon="💪", layout="centered")

# 세션 스테이트 초기화 (데이터 저장용)
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

# 상단 네비게이션 (페이지 전환용 라디오 버튼 또는 탭)
menu = st.radio("메뉴 선택", ["오늘의 운동 기록", "캘린더 및 과거 기록"], horizontal=True, label_visibility="collapsed")

st.divider()

if menu == "오늘의 운동 기록":
    st.title("💪 오늘의 홈트 기록")
    st.write("오늘 어떤 운동을 몇 번 했는지 편하게 기록해 보세요!")

    with st.form("homet_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("날짜", value=datetime.now())
            exercise_name = st.selectbox(
                "운동 종목", 
                ["푸시업", "스쿼트", "플랭크 (초)", "런지", "윗몸일으키기", "버피", "기타 직접 입력"]
            )
            if exercise_name == "기타 직접 입력":
                exercise_name = st.text_input("운동 이름 입력")
                
        with col2:
            target_count = st.number_input("목표 횟수 (또는 시간)", min_value=1, value=10, step=1)
            actual_count = st.number_input("실제 한 횟수", min_value=1, value=10, step=1)
            
        memo = st.text_input("간단 메모 (선택사항)", placeholder="컨디션 좋음, 자세 깔끔 등")
        submitted = st.form_submit_button("기록 저장하기 ✨", use_container_width=True)
        
        if submitted:
            is_challenge = actual_count > target_count
            new_entry = {
                "날짜": date_input.strftime("%Y-%m-%d"),
                "운동": exercise_name,
                "목표": target_count,
                "달성": actual_count,
                "상태": "🔥 도전 성공!" if is_challenge else "완료",
                "메모": memo
            }
            st.session_state.log_data.append(new_entry)
            st.success(f"'{exercise_name}' 기록이 저장되었습니다!")

    # 오늘 한 기록 바로 보기
    st.subheader("📋 오늘의 실시간 기록 리스트")
    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        today_str = datetime.now().strftime("%Y-%m-%d")
        df_today = df[df["날짜"] == today_str]
        
        if not df_today.empty:
            st.dataframe(df_today.iloc[::-1].reset_index(drop=True), use_container_width=True)
        else:
            st.info("오늘 아직 기록된 운동이 없습니다.")
    else:
        st.info("기록된 운동이 없습니다.")

elif menu == "캘린더 및 과거 기록":
    st.title("📅 캘린더 및 과거 기록")
    st.write("날짜를 선택하여 과거에 어떤 운동을 했는지 확인해 보세요.")

    if st.session_state.log_data:
        df = pd.DataFrame(st.session_state.log_data)
        
        # 기록이 있는 날짜 목록 추출 (중복 제거, 최신순)
        available_dates = sorted(df["날짜"].unique(), reverse=True)
        
        selected_date = st.selectbox("조회할 날짜 선택", available_dates)
        
        # 선택한 날짜의 기록 필터링
        df_selected = df[df["날짜"] == selected_date]
        
        st.subheader(f"📌 {selected_date} 운동 내역")
        st.dataframe(df_selected.reset_index(drop=True), use_container_width=True)
        
        # 요약 통계
        total_exercises = len(df_selected)
        challenge_count = len(df_selected[df_selected["상태"] == "🔥 도전 성공!"])
        
        col1, col2 = st.columns(2)
        col1.metric("총 운동 종목 수", f"{total_exercises}개")
        col2.metric("도전 성공 횟수", f"{challenge_count}번")
        
        if st.button("전체 데이터 초기화"):
            st.session_state.log_data = []
            st.rerun()
    else:
        st.info("아직 저장된 과거 기록이 없습니다. 먼저 운동을 기록해 보세요!")
