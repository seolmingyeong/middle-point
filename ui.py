import streamlit as st


# =========================
# 추천 장소 카드
# =========================

def render_place_card(place):

    # =========================
    # 현재 테마 확인
    # =========================

    base = st.get_option(
        "theme.base"
    )

    is_dark = (
        base == "dark"
    )

    # =========================
    # 다크모드 색상
    # =========================

    if is_dark:

        background = "#1e293b"

        border = "#334155"

        title_color = "#f8fafc"

        info_color = "#cbd5e1"

    # =========================
    # 라이트모드 색상
    # =========================

    else:

        background = "#ffffff"

        border = "#e2e8f0"

        title_color = "#334155"

        info_color = "#64748b"

    # =========================
    # 카드 출력
    # =========================

    st.markdown(
        f"""
<div style="
padding:28px;
border-radius:20px;
background:{background};
border:1px solid {border};
margin-top:30px;
margin-bottom:30px;
box-shadow:0 4px 14px rgba(0,0,0,0.04);
">

<div style="
font-size:28px;
font-weight:700;
color:#8b5cf6;
margin-bottom:18px;
">
추천 장소
</div>

<div style="
font-size:22px;
font-weight:600;
margin-bottom:14px;
color:{title_color};
">
{place["name"]}
</div>

<div style="
color:{info_color};
margin-bottom:8px;
">
평균 이동시간:
{place["avg_time"]}분
</div>

<div style="
color:{info_color};
">
최대 이동시간:
{place["max_time"]}분
</div>

</div>
""",
        unsafe_allow_html=True
    )