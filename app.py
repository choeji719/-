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
# 세션 스테이트
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
# 전체 앱에 현재 폰트 및 불필요 요소 제거 CSS 적용
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
       사이드바 제거
       ===================================================== */

    [data-testid="stSidebar"] {{
        display: none;
    }}


    /* =====================================================
       데이터프레임 우측 상단 (...) 툴바 버튼 및 오버레이 완벽 제거
       ===================================================== */

    [data-testid="stDataFrameToolbar"],
    div[data-testid="stElementToolbar"],
    [data-testid="stElementToolbarButton"],
    button[kind="headerButton"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}


    /* =====================================================
       마크다운 제목 링크 차단
       ===================================================== */

    .stMarkdown a.header-anchor, 
    [data-testid="stMarkdownContainer"] a,
    h3 a,
    h2 a,
    h1 a,
    a.anchor-link {{
        display: none !important;
        pointer-events: none !important;
    }}


    /* =====================================================
       제목
       ===================================================== */

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


    /* =====================================================
       오늘 날짜
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
       Popover 내부 크기
       ===================================================== */

    [data-testid="stPopoverBody"] {{
        width: 360px !important;
        max-width: 360px !important;
    }}


    /* =====================================================
       Popover의 expand_more / expand_less 아이콘 제거
       ===================================================== */

    [data-testid="stPopover"] button svg {{
        display: none !important;
    }}

    [data-testid="stPopover"] button [data-testid="stIconMaterial"] {{
        display: none !important;
    }}

    [data-testid="stPopover"] button span[class*="material-symbols"] {{
        display: none !important;
    }}


    /* =====================================================
       설정 버튼
       ===================================================== */

    [data-testid="stPopover"] > button {{
        justify-content: center !important;
        gap: 0 !important;
    }}


    /* =====================================================
       폰트 선택 영역
       ===================================================== */

    .font-title {{
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 8px;
    }}


    /* =====================================================
       현재 선택된 폰트
       ===================================================== */

    .current-font {{
        background-color: rgba(128, 128, 128, 0.09);

        padding: 9px 12px;

        border-radius: 9px;

        margin-bottom: 12px;

        font-size: 14px;
    }}


    /* =====================================================
       폰트 미리보기 라디오 영역
       ===================================================== */

    [data-testid="stPopoverBody"] [data-testid="stRadio"] > div {{
        gap: 3px !important;
    }}


    [data-testid="stPopoverBody"] [data-testid="stRadio"] label {{
        padding: 5px 8px !important;
        border-radius: 8px !important;
    }}


    /* =====================================================
       라디오 버튼 크기
       ===================================================== */

    [data-testid="stPopoverBody"] [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] {{
        font-size: 15px !important;
    }}


    /* =====================================================
       캘린더 기록 박스
       ===================================================== */

    .popup-box {{
        background-color: rgba(128, 128, 128, 0.08);

        padding: 20px;

        border-radius: 15px;

        border: 1px solid rgba(128, 128, 128, 0.15);

        margin-top: 15px;
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
# 설정 Popover
# =========================================================

with top_col2:

    with st.popover(
        "⚙️ 설정",
        use_container_width=True
    ):

        st.markdown(
            "### 🎨 앱 설정"
        )


        # -------------------------------------------------
        # 현재 폰트
        # -------------------------------------------------

        st.markdown(
            f"""
            <div
                class="current-font"
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


        st.markdown(
            '<div class="font-title">폰트 선택 (15종)</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 폰트 선택
        # -------------------------------------------------

        font_names = list(font_mapping.keys())


        selected_index = font_names.index(
            st.session_state.selected_font
        )


        selected_font = st.radio(
            "폰트",
            font_names,
            index=selected_index,
            label_visibility="collapsed"
        )


        # -------------------------------------------------
        # 선택이 변경되었으면 즉시 적용
        # -------------------------------------------------

        if selected_font != st.session_state.selected_font:

            st.session_state.selected_font = selected_font

            st.rerun()


# =========================================================
# 라디오 각각에 자기 폰트 적용
# =========================================================

radio_font_css = ""

font_list = list(font_mapping.values())

for i, font_css in enumerate(font_list):

    radio_font_css += f"""
    [data-testid="stPopoverBody"]
    [data-testid="stRadio"]
    > div
    > label:nth-child({i + 1})
    div[data-testid="stMarkdownContainer"] {{
        font-family: {font_css} !important;
    }}
    """


st.markdown(
    f"""
    <style>
    {radio_font_css}
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 구분선
# =========================================================

st.markdown("---")


# =========================================================
# 1. 바로 기록하기
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
    # 오늘 날짜 (KST 기준)
    # -----------------------------------------------------

    current_kst = get_kst_now()
    today_str = current_kst.strftime(
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
    # 기록 폼
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


        if category == "✨ 직접 입력":

            category = st.text_input(
                "어떤 행동인가요?"
            )


        st.write(
            "📊 횟수 / 양 선택"
        )


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
        # 숫자 조절
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

            save_kst = get_kst_now()
            now_time = save_kst.strftime(
                "%H:%M:%S"
            )

            new_id = (
                max([item["id"] for item in st.session_state.log_data]) + 1
                if st.session_state.log_data
                else 1
            )

            new_entry = {
                "id": new_id,
                "날짜": save_kst.strftime(
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
    # 오늘의 기록 (깔끔한 기본 표 형태 복원 및 ... 툴바 제거)
    # =====================================================

    st.markdown(
        "### 📋 오늘의 실시간 기록"
    )


    if st.session_state.log_data:

        df = pd.DataFrame(
            st.session_state.log_data
        )


        today_date_str = get_kst_now().strftime(
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
                use_container_width=True,
                hide_index=True
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
# 2. 캘린더
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
    # 연도 / 월
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
            index=get_kst_now().month - 1
        )


    st.markdown("---")


    # -----------------------------------------------------
    # 캘린더
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
    # 데이터
    # -----------------------------------------------------

    if st.session_state.log_data:

        df_all = pd.DataFrame(
            st.session_state.log_data
        )

    else:

        df_all = pd.DataFrame(
            columns=[
                "id",
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


    # -----------------------------------------------------
    # 선택한 날짜
    # -----------------------------------------------------

    sel_date_str = (
        st.session_state.selected_date.strftime(
            "%Y-%m-%d"
        )
    )


    st.markdown(
        f"### 📌 선택한 날짜: {sel_date_str}"
    )


    # =====================================================
    # 선택 날짜 기록
    # =====================================================

    with st.container():

        st.markdown(
            '<div class="popup-box">',
            unsafe_allow_html=True
        )


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
        # 기록 목록 및 체크박스 선택 삭제 기능
        # -------------------------------------------------

        if not df_target.empty:

            st.write(
                "📋 **이날의 기록 목록** (삭제할 항목을 선택하세요)"
            )

            # 삭제할 id들을 담을 리스트
            selected_ids_to_delete = []

            for _, row in df_target.iterrows():

                time_str = row.get(
                    "시간",
                    "시간 미상"
                )

                memo_str = row.get(
                    "메모",
                    "없음"
                )

                row_id = row.get("id")
                item_label = f"[{time_str}] {row['항목']}: {row['횟수']}회 (메모: {memo_str})"

                # 체크박스로 선택하도록 구현
                if st.checkbox(item_label, key=f"chk_{row_id}"):
                    selected_ids_to_delete.append(row_id)

            st.markdown("<br>", unsafe_allow_html=True)

            # 선택된 항목이 있을 때만 삭제 버튼 활성화
            if selected_ids_to_delete:
                if st.button("🗑️ 선택한 기록 삭제", use_container_width=True):
                    # 선택되지 않은 항목들만 남기고 필터링
                    st.session_state.log_data = [
                        item for item in st.session_state.log_data if item["id"] not in selected_ids_to_delete
                    ]
                    st.success("선택한 기록이 삭제되었습니다.")
                    st.rerun()

        else:

            st.info(
                "이 날짜에는 아직 기록이 없습니다."
            )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 기록 추가
        # -------------------------------------------------

        if not st.session_state.is_editing:

            if st.button(
                "✏️ 이 날짜에 기록 추가하기",
                use_container_width=True
            ):

                st.session_state.is_editing = True

                st.rerun()


        # -------------------------------------------------
        # 과거 날짜 기록 추가
        # -------------------------------------------------

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

                    save_kst = get_kst_now()
                    now_time = save_kst.strftime(
                        "%H:%M:%S"
                    )

                    new_id = (
                        max([item["id"] for item in st.session_state.log_data]) + 1
                        if st.session_state.log_data
                        else 1
                    )

                    new_entry = {
                        "id": new_id,
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
# 광고 영역
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
