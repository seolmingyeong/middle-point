# =========================
# app.py
# =========================

import random
import string

import streamlit as st

from database import *

from recommendation import *

from route_api import *

from map_utils import *

from ui import *

from theme import apply_theme


# =========================
# 페이지 설정
# =========================

st.set_page_config(

    page_title="스페이스타임",

    layout="wide"
)


# =========================
# 테마 적용
# =========================

apply_theme()


# =========================
# DB 초기화
# =========================

init_db()


# =========================
# session_state
# =========================

if "current_room" not in st.session_state:

    st.session_state.current_room = None


if "recommendations" not in st.session_state:

    st.session_state.recommendations = None


if "nickname" not in st.session_state:

    st.session_state.nickname = ""


if "selected_dates" not in st.session_state:

    st.session_state.selected_dates = []


# =========================
# 제목
# =========================

st.markdown(
    """
<h1 style="
text-align:center;
font-size:58px;
font-weight:800;
background: linear-gradient(
    90deg,
    #8b5cf6,
    #60a5fa
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:10px;
">
스페이스타임
</h1>

<p style="
text-align:center;
font-size:18px;
margin-bottom:35px;
opacity:0.8;
">
모두의 시간과 공간을 연결하는 약속 플랫폼
</p>
""",
    unsafe_allow_html=True
)


# =========================
# 방 입장 전
# =========================

if not st.session_state.current_room:

    col1, col2 = st.columns(2)

    # =========================
    # 방 만들기
    # =========================

    with col1:

        st.markdown(
            """
<div class="card">

<h3>
✨ 새 방 만들기
</h3>

<p>
새로운 약속 공간 생성
</p>

</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            "방 만들기",
            key="create_room"
        ):

            room_id = "".join(

                random.choices(

                    string.ascii_uppercase
                    + string.digits,

                    k=6
                )
            )

            st.session_state.current_room = (
                room_id
            )

            st.rerun()

    # =========================
    # 방 입장
    # =========================

    with col2:

        st.markdown(
            """
<div class="card">

<h3>
🚪 방 입장
</h3>

<p>
기존 약속 공간 참여
</p>

</div>
""",
            unsafe_allow_html=True
        )

        join_room = st.text_input(
            "방 코드 입력"
        )

        if st.button(
            "입장하기",
            key="join_room"
        ):

            st.session_state.current_room = (
                join_room
            )

            st.rerun()


# =========================
# 방 입장 후
# =========================

if st.session_state.current_room:

    st.markdown(
        f"""
<div class="card">

<h2>
🌌 방 코드:
{st.session_state.current_room}
</h2>

</div>
""",
        unsafe_allow_html=True
    )

    # =========================
    # 사용자 정보 입력
    # =========================

    st.markdown(
        """
<h3 style="
margin-top:20px;
margin-bottom:20px;
">
🙋 내 정보 입력
</h3>
""",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        nickname = st.text_input(

            "닉네임",

            value=st.session_state.nickname
        )

        location_name = st.text_input(
            "출발 위치"
        )

    with col2:

        transport = st.selectbox(

            "이동수단",

            [
                "도보",
                "대중교통",
                "자동차"
            ]
        )
    # =========================
    # 가능한 날짜 선택
    # 기존 달력 코드 전체 삭제 후 교체
    # =========================

    import calendar
    from datetime import datetime


    st.markdown(
        """
    <h3 style="
    margin-top:25px;
    margin-bottom:18px;
    ">
    📅 가능한 날짜
    </h3>
    """,
        unsafe_allow_html=True
    )

    today = datetime.today()

    year = today.year

    month = today.month

    cal = calendar.monthcalendar(
        year,
        month
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

    # =========================
    # 요일 헤더
    # =========================

    header_cols = st.columns(7)

    for idx, day_name in enumerate(
        weekdays
    ):

        header_cols[idx].markdown(
            f"""
    <div style="
    text-align:center;
    font-weight:700;
    font-size:17px;
    margin-bottom:12px;
    opacity:0.75;
    ">
    {day_name}
    </div>
    """,
            unsafe_allow_html=True
        )
    # =========================
    # 가능한 날짜 선택
    # =========================

    import calendar
    from datetime import datetime

    st.markdown(
        """
    <h3 style="
    margin-top:30px;
    margin-bottom:20px;
    font-size:24px;
    font-weight:700;
    color:#334155;
    ">
    📅 가능한 날짜
    </h3>
    """,
        unsafe_allow_html=True
    )

    # =========================
    # session state
    # =========================

    if "selected_dates" not in st.session_state:

        st.session_state.selected_dates = []

    # =========================
    # 달력 데이터
    # =========================

    today = datetime.today()

    year = today.year

    month = today.month

    cal = calendar.monthcalendar(
        year,
        month
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

    # =========================
    # CSS
    # =========================

    st.markdown(
        """
    <style>

    /* 달력 전체 */

    .calendar-wrapper {

        border:1px solid rgba(148,163,184,0.15);

        overflow:hidden;

        margin-bottom:30px;
    }


    /* 요일 */

    .calendar-header {

        background:#f8fafc;

        border-right:1px solid rgba(148,163,184,0.1);

        border-bottom:1px solid rgba(148,163,184,0.1);

        text-align:center;

        padding:14px 0;

        font-weight:700;

        color:#64748b;
    }


    /* 날짜칸 */

    .calendar-cell {

        position:relative;

        height:92px;

        display:flex;

        align-items:center;

        justify-content:center;

        background:#f8fafc;

        border-right:1px solid rgba(148,163,184,0.08);

        border-bottom:1px solid rgba(148,163,184,0.08);

        font-size:22px;

        font-weight:700;

        color:#334155;

        cursor:pointer;

        transition:0.15s;
    }


    /* hover */

    .calendar-cell:hover {

        background:#eef2ff;
    }


    /* 선택됨 */

    .calendar-selected {

        background:
        linear-gradient(
            135deg,
            #8b5cf6,
            #60a5fa
        ) !important;

        color:white !important;
    }


    /* 빈칸 */

    .calendar-empty {

        height:92px;

        background:white;

        border-right:1px solid rgba(148,163,184,0.06);

        border-bottom:1px solid rgba(148,163,184,0.06);
    }


    /* 버튼 */

    .calendar-button button {

        position:absolute !important;

        top:0 !important;

        left:0 !important;

        width:100% !important;

        height:100% !important;

        opacity:0 !important;

        z-index:20 !important;

        border-radius:0px !important;

        padding:0px !important;

        margin:0px !important;

        min-height:100% !important;
    }

    </style>
    """,
        unsafe_allow_html=True
    )

    # =========================
    # 달력 시작
    # =========================

    st.markdown(
        '<div class="calendar-wrapper">',
        unsafe_allow_html=True
    )

    # =========================
    # 요일 헤더
    # =========================

    header_cols = st.columns(7)

    for idx, weekday in enumerate(
        weekdays
    ):

        header_cols[idx].markdown(
            f"""
    <div class="calendar-header">
    {weekday}
    </div>
    """,
            unsafe_allow_html=True
        )

    # =========================
    # 날짜 출력
    # =========================

    for week_idx, week in enumerate(cal):

        cols = st.columns(7)

        for day_idx, day in enumerate(week):

            # 빈칸

            if day == 0:

                cols[day_idx].markdown(
                    """
    <div class="calendar-empty"></div>
    """,
                    unsafe_allow_html=True
                )

            # 실제 날짜

            else:

                date_str = (
                    f"{year}-{month:02d}-{day:02d}"
                )

                selected = (
                    date_str
                    in
                    st.session_state.selected_dates
                )

                class_name = (
                    "calendar-cell calendar-selected"
                    if selected
                    else "calendar-cell"
                )

                cols[day_idx].markdown(
                    f"""
    <div class="{class_name}">
    {day}
    <div class="calendar-button">
    """,
                    unsafe_allow_html=True
                )

                if cols[day_idx].button(

                    label="",

                    key=f"calendar_{date_str}",

                    use_container_width=True
                ):

                    # 선택 해제

                    if selected:

                        st.session_state.selected_dates.remove(
                            date_str
                        )

                    # 선택

                    else:

                        st.session_state.selected_dates.append(
                            date_str
                        )

                    st.rerun()

                cols[day_idx].markdown(
                    """
    </div>
    </div>
    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
                    
# =========================
# 정보 저장 버튼 수정
# =========================

    if st.button(
        "정보 저장",
        key=f"save_user_button_{st.session_state.current_room}"
    ):
        
        st.session_state.nickname = (
            nickname
        )

        save_user(

            st.session_state.current_room,

            nickname,

            ",".join(
                st.session_state.selected_dates
            ),

            location_name,

            37.5665,

            126.9780,

            transport
        )

        st.success(
            "정보 저장 완료!"
        )

        st.rerun()

# =========================
# 참가자 목록
# =========================

if st.session_state.current_room:

    users_data = get_room_users(

        st.session_state.current_room
    )

    st.markdown(
        """
<h2 style="
margin-top:40px;
margin-bottom:20px;
">
👥 참가자
</h2>
""",
        unsafe_allow_html=True
    )

    for user in users_data:

        st.markdown(
            f"""
<div class="card">

<div style="
font-size:22px;
font-weight:700;
color:#8b5cf6;
margin-bottom:10px;
">
👤 {user[2]}
</div>

<div style="
margin-bottom:6px;
opacity:0.85;
">
📍 {user[4]}
</div>

<div style="
margin-bottom:6px;
opacity:0.85;
">
🚗 {user[7]}
</div>

<div style="
opacity:0.85;
">
📅 {user[3]}
</div>

</div>
""",
            unsafe_allow_html=True
        )
        
    # =========================
    # 추천 장소
    # =========================

    if len(users_data) >= 2:

        if st.button(
            "✨ 추천 장소 찾기",
            key="recommend_button"
        ):

            users = []

            for user in users_data:

                users.append({

                    "nickname": user[2],

                    "lat": user[5],

                    "lng": user[6],

                    "transport": user[7]
                })

            middle_lat, middle_lng = (
                get_middle_point(users)
            )

            recommendations = (
                recommend_places(

                    users,

                    middle_lat,

                    middle_lng
                )
            )

            st.session_state.recommendations = (
                recommendations
            )

            st.session_state.middle_lat = (
                middle_lat
            )

            st.session_state.middle_lng = (
                middle_lng
            )

    # =========================
    # 추천 결과
    # =========================

    if st.session_state.recommendations:

        recommendations = (
            st.session_state.recommendations
        )

        best_place = recommendations[0]

        render_place_card(
            best_place
        )

        users = []

        for user in users_data:

            users.append({

                "nickname": user[2],

                "lat": user[5],

                "lng": user[6],

                "transport": user[7]
            })

        st.markdown(
            """
<h2 style="
margin-top:40px;
margin-bottom:20px;
">
🗺 추천 지도
</h2>
""",
            unsafe_allow_html=True
        )

        render_map(

            users,

            recommendations,

            st.session_state.middle_lat,

            st.session_state.middle_lng
        )