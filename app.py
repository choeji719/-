import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from urllib.parse import quote


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
# 세션 스테이트 초기화
# =========================================================

if "selected_font" not in st.session_state:
    st.session_state.selected_font = "CookieRun (발랄하고 둥글둥글)"

if "log_data" not in st.session_state:
    st.session_state.log_data = [
        {
            "id": 1,
            "날짜": datetime.now().strftime("%Y-%m-%d"),
            "항목": "☕ 커피 마신 잔수",
            "횟수": 2,
            "메모": "아아 마심",
            "시간": datetime.now().strftime("%H:%M:%S")
        },
        {
            "id": 2,
            "날짜": datetime.now().strftime("%Y-%m-%d"),
            "항목": "💪 운동 횟수",
            "횟수": 50,
            "메모": "스쿼트",
            "시간": datetime.now().strftime("%H:%M:%S")
        }
    ]

if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

if "is_editing" not in st.session_state:
    st.session_state.is_editing = False

if "current_count" not in st.session_state:
    st.session_state.current_count = 1


# =========================================================
# URL로 전달된 폰트 선택 처리
#
# 커스텀 폰트 목록의 항목을 클릭하면
# ?font=... 형태로 페이지가 다시 열리고,
# 아래에서 선택된 폰트를 세션에 반영한다.
# =========================================================

font_from_url = st.query_params.get("font")

if font_from_url in font_mapping:
    st.session_state.selected_font = font_from_url
    st.query_params.clear()


# =========================================================
# 현재 선택된 폰트
# =========================================================

current_font_css = font_mapping.get(
    st.session_state.selected_font,
    "-apple-system, sans-serif"
)


# =========================================================
# Google Fonts + CookieRun
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       Google Fonts
       ===================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Do+Hyeon&family=Gaegu&family=Gowun+Batang&family=Gowun+Dodum&family=Gugi&family=IBM+Plex+Sans+KR:wght@300;400;600&family=Jua&family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@400;700&family=Nanum+Square:wght@400;700&family=Poor+Story&family=Sunflower:wght@300&display=swap'
    );


    /* =====================================================
       CookieRun
       ===================================================== */

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
# 현재 선택된 폰트를 전체 앱에 적용
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
    [data-baseweb="select"] * {{
        font-family: {current_font_css} !important;
    }}


    /* =====================================================
       사이드바 제거
       ===================================================== */

    [data-testid="stSidebar"] {{
        display: none;
    }}


    /* =====================================================
       메인 제목
       ===================================================== */

    .main-title {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 0px;
    }}


    /* =====================================================
       설명
       ===================================================== */

    .sub-desc {{
        color: gray;
        font-size: 13px;
        margin-bottom: 15px;
    }}


    /* =====================================================
       오늘 날짜 배너
       ===================================================== */

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


    /* =====================================================
       캘린더 기록 팝업 박스
       ===================================================== */

    .popup-box {{
        background-color: rgba(128, 128, 128, 0.08);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-top: 15px;
    }}


    /* =====================================================
       설정 Popover의 expand_more 아이콘 제거
       ===================================================== */

    [data-testid="stPopover"] > button svg {{
        display: none !important;
    }}

    [data-testid="stPopover"] > button [data-testid="stIconMaterial"] {{
        display: none !important;
    }}

    [data-testid="stPopover"] > button .material-symbols-rounded {{
        display: none !important;
    }}

    [data-testid="stPopover"] > button .material-symbols-outlined {{
        display: none !important;
    }}


    /* =====================================================
       설정 버튼 정렬
       ===================================================== */

    [data-testid="stPopover"] > button {{
        justify-content: center !important;
    }}


    /* =====================================================
       커스텀 폰트 선택 영역
       ===================================================== */

    .font-picker {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 5px;
    }}


    /* =====================================================
       폰트 선택 항목
       ===================================================== */

    .font-choice {{
        display: block;

        width: 100%;
        box-sizing: border-box;

        padding: 10px 12px;

        border-radius: 10px;

        text-decoration: none !important;

        color: inherit !important;

        background: transparent;

        border: 1px solid transparent;

        font-size: 16px;

        line-height: 1.35;

        transition:
            background-color 0.15s ease,
            border-color 0.15s ease;
    }}


    /* =====================================================
       폰트 항목 Hover
       ===================================================== */

    .font-choice:hover {{
        background: rgba(128, 128, 128, 0.12);

        border-color:
            rgba(128, 128, 128, 0.18);
    }}


    /* =====================================================
       현재 선택된 폰트
       ===================================================== */

    .font-choice.selected {{
        background:
            rgba(33, 150, 243, 0.12);

        border-color:
            rgba(33, 150, 243, 0.28);

        font-weight: 600;
    }}


    /* =====================================================
       현재 폰트 표시
       ===================================================== */

    .font-current {{
        margin-top: 4px;

        margin-bottom: 14px;

        padding: 10px 12px;

        border-radius: 10px;

        background:
            rgba(128, 128, 128, 0.08);

        font-size: 14px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 상단 레이아웃
# =========================================================

top_col1, top_col2 = st.columns([3, 1])


# =========================================================
# 화면 이동
# =========================================================

with top_col1:

    nav = st.radio(
        "화면 이동",
        [
            "⚡ 바로 기록하기",
            "📅 캘린더 (월간 보기)"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )


# =========================================================
# 설정
# =========================================================

with top_col2:

    with st.popover(
        "⚙️ 설정",
        use_container_width=True
    ):

        st.markdown("#### 🎨 앱 설정")


        # -------------------------------------------------
        # 현재 선택된 폰트
        # -------------------------------------------------

        st.markdown(
            f"""
            <div
                class="font-current"
                style="font-family: {current_font_css} !important;"
            >
                현재 폰트:
                <strong>
                    {st.session_state.selected_font}
                </strong>
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown("폰트 선택 (15종)")


        # -------------------------------------------------
        # 커스텀 폰트 선택 메뉴
        #
        # 중요:
        # Streamlit selectbox를 사용하지 않고
        # 각각의 HTML 요소에 직접 font-family를 지정한다.
        # -------------------------------------------------

        font_html = '<div class="font-picker">'


        for font_name, font_css in font_mapping.items():

            selected_class = (
                " selected"
                if font_name == st.session_state.selected_font
                else ""
            )


            encoded_name = quote(
                font_name,
                safe=""
            )


            font_html += f"""
            <a
                class="font-choice{selected_class}"
                href="?font={encoded_name}"
                style="font-family: {font_css} !important;"
            >
                {font_name}
            </a>
            """


        font_html += "</div>"


        st.markdown(
            font_html,
            unsafe_allow_html=True
        )


# =========================================================
# 구분선
# =========================================================

st.markdown("---")


# =========================================================
# 1. 바로 기록하기 화면
# =========================================================

if nav == "⚡ 바로 기록하기":

    st.markdown(
        '<p class="main-title">⚡ 무엇을 기록할까요?</p>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<p class="sub-desc">접속하자마자 1초 만에 기록하세요.</p>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # 오늘 날짜
    # -----------------------------------------------------

    today_str = datetime.now().strftime(
        "%Y년 %m월 %d일 (%a)"
    )


    st.markdown(
        f"""
        <div class="today-banner">
            📅 오늘 날짜: {today_str}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # 빠른 기록 입력
    # -----------------------------------------------------

    with st.form(
        "quick_log_form",
        clear_on_submit=False
    ):

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


        # -------------------------------------------------
        # 직접 입력
        # -------------------------------------------------

        if category == "✨ 직접 입력":

            category = st.text_input(
                "어떤 행동인가요?"
            )


        st.write("📊 횟수 / 양 선택")


        # -------------------------------------------------
        # 횟수
        # -------------------------------------------------

        count_input = st.number_input(
            "직접 입력",
            min_value=1,
            value=int(
                st.session_state.current_count
            ),
            step=1,
            label_visibility="collapsed"
        )


        st.session_state.current_count = count_input


        # -------------------------------------------------
        # 빠른 증감 버튼
        # -------------------------------------------------

        c1, c2, c3, c4, c5 = st.columns(5)


        if c1.form_submit_button(
            "-10",
            use_container_width=True
        ):

            st.session_state.current_count = max(
                1,
                st.session_state.current_count - 10
            )

            st.rerun()


        if c2.form_submit_button(
            "-5",
            use_container_width=True
        ):

            st.session_state.current_count = max(
                1,
                st.session_state.current_count - 5
            )

            st.rerun()


        if c3.form_submit_button(
            "-1",
            use_container_width=True
        ):

            st.session_state.current_count = max(
                1,
                st.session_state.current_count - 1
            )

            st.rerun()


        if c4.form_submit_button(
            "+5",
            use_container_width=True
        ):

            st.session_state.current_count += 5

            st.rerun()


        if c5.form_submit_button(
            "+10",
            use_container_width=True
        ):

            st.session_state.current_count += 10

            st.rerun()


        # -------------------------------------------------
        # 메모
        # -------------------------------------------------

        memo = st.text_input(
            "메모 (선택)",
            placeholder="특이사항 입력"
        )


        # -------------------------------------------------
        # 저장
        # -------------------------------------------------

        submitted = st.form_submit_button(
            "🚀 지금 바로 기록 저장",
            use_container_width=True
        )


        if submitted:

            now_time = datetime.now().strftime(
                "%H:%M:%S"
            )


            new_entry = {
                "id": len(
                    st.session_state.log_data
                ) + 1,

                "날짜": datetime.now().strftime(
                    "%Y-%m-%d"
                ),

                "항목": category,

                "횟수": st.session_state.current_count,

                "메모": memo,

                "시간": now_time
            }


            st.session_state.log_data.append(
                new_entry
            )


            st.success(
                f"✅ 저장 완료! ({now_time})"
            )


            st.session_state.current_count = 1


    # =====================================================
    # 오늘의 실시간 기록
    # =====================================================

    st.markdown(
        "### 📋 오늘의 실시간 기록"
    )


    if st.session_state.log_data:

        df = pd.DataFrame(
            st.session_state.log_data
        )


        today_date_str = datetime.now().strftime(
            "%Y-%m-%d"
        )


        df_today = df[
            df["날짜"] == today_date_str
        ]


        if not df_today.empty:

            display_df = df_today[
                [
                    "시간",
                    "항목",
                    "횟수",
                    "메모"
                ]
            ].reset_index(drop=True)


            st.dataframe(
                display_df,
                use_container_width=True
            )


        else:

            st.info(
                "오늘 아직 기록된 내역이 없습니다."
            )


    else:

        st.info(
            "첫 기록을 남겨보세요!"
        )


# =========================================================
# 2. 애플 캘린더 스타일 화면
# =========================================================

elif nav == "📅 캘린더 (월간 보기)":

    st.markdown(
        '<p class="main-title">📅 월간 캘린더</p>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<p class="sub-desc">날짜를 클릭하여 해당 날의 기록을 확인하고 편집하세요.</p>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # 연도 / 월 선택
    # -----------------------------------------------------

    col_y, col_m = st.columns(2)


    with col_y:

        selected_year = st.selectbox(
            "연도",
            [
                2026,
                2025,
                2024
            ],
            index=0
        )


    with col_m:

        selected_month = st.selectbox(
            "월",
            list(range(1, 13)),
            index=datetime.now().month - 1
        )


    st.markdown("---")


    # -----------------------------------------------------
    # 캘린더 생성
    # -----------------------------------------------------

    cal = calendar.monthcalendar(
        selected_year,
        selected_month
    )


    weekdays = [
        "월",
        "화",
        "수",
        "목",
        "금",
        "토",
        "일"
    ]


    # -----------------------------------------------------
    # 요일
    # -----------------------------------------------------

    cols = st.columns(7)


    for i, day_name in enumerate(weekdays):

        cols[i].markdown(
            f"""
            <div style="
                text-align: center;
                font-weight: bold;
                color: #868e96;
            ">
                {day_name}
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # 전체 데이터
    # -----------------------------------------------------

    if st.session_state.log_data:

        df_all = pd.DataFrame(
            st.session_state.log_data
        )

    else:

        df_all = pd.DataFrame(
            columns=[
                "날짜",
                "항목",
                "횟수",
                "메모",
                "시간"
            ]
        )


    # -----------------------------------------------------
    # 날짜 버튼
    # -----------------------------------------------------

    for week in cal:

        cols = st.columns(7)


        for i, day in enumerate(week):

            if day == 0:

                cols[i].markdown("")

            else:

                current_date_str = (
                    f"{selected_year}-"
                    f"{selected_month:02d}-"
                    f"{day:02d}"
                )


                has_log = False


                if (
                    not df_all.empty
                    and "날짜" in df_all.columns
                ):

                    has_log = not df_all[
                        df_all["날짜"]
                        == current_date_str
                    ].empty


                # 기록이 있으면 • 표시
                btn_label = (
                    f"{day} •"
                    if has_log
                    else f"{day}"
                )


                if cols[i].button(
                    btn_label,
                    key=f"date_{current_date_str}",
                    use_container_width=True
                ):

                    st.session_state.selected_date = date(
                        selected_year,
                        selected_month,
                        day
                    )


                    st.session_state.is_editing = False


                    st.rerun()


    st.markdown("---")


    # =====================================================
    # 선택한 날짜
    # =====================================================

    sel_date_str = (
        st.session_state.selected_date.strftime(
            "%Y-%m-%d"
        )
    )


    st.markdown(
        f"### 📌 선택한 날짜: {sel_date_str}"
    )


    # =====================================================
    # 선택 날짜 기록 영역
    # =====================================================

    with st.container():

        st.markdown(
            '<div class="popup-box">',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 해당 날짜의 기록
        # -------------------------------------------------

        if (
            not df_all.empty
            and "날짜" in df_all.columns
        ):

            df_target = df_all[
                df_all["날짜"] == sel_date_str
            ]

        else:

            df_target = pd.DataFrame()


        # -------------------------------------------------
        # 기록 출력
        # -------------------------------------------------

        if not df_target.empty:

            st.write(
                "📋 **이날의 기록 목록**"
            )


            for _, row in df_target.iterrows():

                time_str = row.get(
                    "시간",
                    "시간 미상"
                )


                memo_str = row.get(
                    "메모",
                    "없음"
                )


                st.text(
                    f"[{time_str}] "
                    f"{row['항목']}: "
                    f"{row['횟수']}회 "
                    f"(메모: {memo_str})"
                )


        else:

            st.info(
                "이 날짜에는 아직 기록이 없습니다."
            )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        # =================================================
        # 기록 추가 버튼
        # =================================================

        if not st.session_state.is_editing:

            if st.button(
                "✏️ 이 날짜에 기록 추가하기",
                use_container_width=True
            ):

                st.session_state.is_editing = True

                st.rerun()


        # =================================================
        # 과거 날짜 기록 추가
        # =================================================

        else:

            st.markdown(
                "#### ➕ 과거 날짜 기록 추가"
            )


            with st.form(
                f"edit_form_{sel_date_str}",
                clear_on_submit=True
            ):

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

                    add_category = st.text_input(
                        "직접 입력"
                    )


                add_count = st.number_input(
                    "횟수 / 양",
                    min_value=1,
                    value=1
                )


                add_memo = st.text_input(
                    "메모"
                )


                col_sub1, col_sub2 = st.columns(2)


                submit_added = col_sub1.form_submit_button(
                    "저장하기",
                    use_container_width=True
                )


                cancel_edit = col_sub2.form_submit_button(
                    "닫기",
                    use_container_width=True
                )


                # -----------------------------------------
                # 저장
                # -----------------------------------------

                if submit_added:

                    now_time = datetime.now().strftime(
                        "%H:%M:%S"
                    )


                    new_entry = {
                        "id": len(
                            st.session_state.log_data
                        ) + 1,

                        "날짜": sel_date_str,

                        "항목": add_category,

                        "횟수": add_count,

                        "메모": add_memo,

                        "시간": now_time
                    }


                    st.session_state.log_data.append(
                        new_entry
                    )


                    st.session_state.is_editing = False


                    st.success(
                        "추가되었습니다!"
                    )


                    st.rerun()


                # -----------------------------------------
                # 닫기
                # -----------------------------------------

                if cancel_edit:

                    st.session_state.is_editing = False

                    st.rerun()


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 하단 광고 영역
# =========================================================

html_ad = """
<div style="
    background-color: rgba(128, 128, 128, 0.08);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: #868e96;
    font-size: 13px;
    margin-top: 30px;
    border: 1px dashed rgba(128, 128, 128, 0.2);
">
    📢 [광고 영역] 구글 애드센스 배너가 들어갈 자리입니다.
</div>
"""


st.markdown(
    html_ad,
    unsafe_allow_html=True
)
