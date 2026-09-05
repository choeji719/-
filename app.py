import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="홈트 기록장", page_icon="💪")

st.title("💪 홈트레이닝 기록 앱")
st.write("오늘 어떤 운동을 몇 번 했는지 편하게 기록하고, 추가 도전(오버워크)을 달성해 보세요!")

if 'log_data' not in st.session_state:
    st.session_state.log_data = []

with st.form("homet_form", clear_on_submit=True):
    st.subheader("오늘의 운동 기록하기")
    
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
        
    memo = st.text_input("간단 메모 (선택사항)", placeholder="컨디션 좋음 등")
    submitted = st.form_submit_button("기록 저장하기 ✨")
    
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

st.divider()

st.subheader("📋 나의 운동 기록부")
if st.session_state.log_data:
    df = pd.DataFrame(st.session_state.log_data)
    df_sorted = df.iloc[::-1].reset_index(drop=True)
    st.dataframe(df_sorted, use_container_width=True)
    
    if st.button("전체 기록 초기화"):
        st.session_state.log_data = []
        st.rerun()
else:
    st.info("아직 기록된 운동이 없습니다. 위에서 첫 운동을 기록해 보세요!")
