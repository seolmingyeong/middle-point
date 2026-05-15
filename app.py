# =========================
# app.py
# =========================

import streamlit as st

from database import *

from recommendation import *

from route_api import *

from map_utils import *

from ui import *


# =========================
# 페이지 설정
# =========================

st.set_page_config(

    page_title="스페이스타임",

    layout="wide"
)


# =========================
# 전체 CSS
# =========================

st.markdown(
    """
<style>

/* =========================
   공통
========================= */

.stApp {

    transition:0.3s;
}

.block-container {

    max-width:1200px;

    padding-top:2rem;
}


/* =========================
   라이트 모드
========================= */

@media (prefers-color-scheme: light) {

    .stApp {

        background:
        linear-gradient(
            180deg,
            #fffdf7 0%,
            #f8fafc 35%,
            #f5f3ff 70%,
            #eef2ff 100%
        );
    }

    html,
    body,
    p,
    span,
    label,
    div {

        color:#334155 !important;
    }

    .spacetime-card,
    .participant-card {

        background:white;

        border:1px solid #e9d5ff;
    }

    .participant-card {

        border-left:6px solid #8b5cf6;
    }

    .stTextInput input {

        background:white !important;

        color:#334155 !important;

        border:2px solid #ddd6fe !important;

        border-radius:16px;
    }

    .stSelectbox div[data-baseweb="select"] {

        background:white !important;

        border-radius:16px;

        border:2px solid #ddd6fe !important;
    }
}


/* =========================
   다크 모드
========================= */

@media (prefers-color-scheme: dark) {

    .stApp {

        background:
        linear-gradient(
            180deg,
            #0f172a 0%,
            #111827 50%,
            #1e1b4b 100%
        );
    }

    html,
    body,
    p,
    span,
    label,
    div {

        color:#f8fafc !important;
    }

    .spacetime-card,
    .participant-card {

        background:
        rgba(
            30,
            41,
            59,
            0.92
        );

        border:1px solid #312e81;
    }

    .participant-card {

        border-left:6px solid #8b5cf6;
    }

    .stTextInput input {

        background:#1e293b !important;

        color:white !important;

        border:2px solid #4338ca !important;

        border-radius:16px;
    }

    .stSelectbox div[data-baseweb="select"] {

        background:#1e293b !important;

        border-radius:16px;

        border:2px solid #4338ca !important;
    }

    .stSelectbox * {

        color:white !important;
    }
}


/* =========================
   공통 버튼
========================= */

.stButton > button {

    width:100%;

    background:
    linear-gradient(
        90deg,
        #8b5cf6,
        #60a5fa
    ) !important;

    color:white !important;

    border:none;

    border-radius:18px;

    padding:14px;

    font-size:16px;

    font-weight:700;

    transition:0.2s;

    box-shadow:
        0 8px 24px rgba(
            139,
            92,
            246,
            0.25
        );
}

.stButton > button:hover {

    transform:translateY(-2px);

    opacity:0.95;
}


/* =========================
   공통 카드
========================= */

.spacetime-card {

    border-radius:24px;

    padding:24px;

    margin-bottom:20px;

    transition:0.3s;
}

.participant-card {

    border-radius:20px;

    padding:18px;

    margin-bottom:14px;

    transition:0.3s;
}


/* =========================
   지도
========================= */

iframe {

    border-radius:24px;
}

</style>
""",
    unsafe_allow_html=True
)


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
🌌 스페이스타임
</h1>

<p style="
text-align:center;
font-size:18px;
color:#64748b !important;
margin-bottom:35px;
">
모두의 시간과 공간을 연결하는 약속 플랫폼
</p>
""",
    unsafe_allow_html=True
)


# =========================
# 입력 영역
# =========================

st.markdown(
    """
<div class="spacetime-card">
""",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    room_id = st.text_input(
        "방 코드"
    )

    nickname = st.text_input(
        "닉네임"
    )

with col2:

    location_name = st.text_input(
        "출발 위치"
    )

    transport = st.selectbox(

        "이동수단",

        [
            "도보",
            "대중교통",
            "자동차"
        ]
    )

if st.button(
    "✨ 참여하기",
    key="join_button"
):

    save_user(

        room_id,

        nickname,

        "2026-05-15",

        location_name,

        37.5665,

        126.9780,

        transport
    )

    st.session_state.current_room = (
        room_id
    )

    st.success(
        "참여 완료!"
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================
# 참가자 목록
# =========================

users_data = []

if st.session_state.current_room:

    users_data = get_room_users(

        st.session_state.current_room
    )

    st.markdown(
        """
<h2 style="
color:#8b5cf6 !important;
margin-top:30px;
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
<div class="participant-card">

<div style="
font-size:22px;
font-weight:700;
color:#8b5cf6 !important;
margin-bottom:10px;
">
👤 {user[2]}
</div>

<div style="
color:#64748b !important;
margin-bottom:6px;
">
📍 {user[4]}
</div>

<div style="
color:#64748b !important;
">
🚗 {user[7]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================
# 추천 장소 계산
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
color:#8b5cf6 !important;
margin-top:30px;
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