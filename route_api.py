import requests
import streamlit as st


# =========================
# 카카오 API 키
# =========================

KAKAO_REST_API_KEY = st.secrets[
    "KAKAO_REST_API_KEY"
]


# =========================
# 자동차 이동시간 계산
# =========================

def get_car_travel_time(

    start_lat,
    start_lng,

    end_lat,
    end_lng
):

    url = (
        "https://apis-navi.kakaomobility.com/v1/directions"
    )

    headers = {
        "Authorization": (
            f"KakaoAK {KAKAO_REST_API_KEY}"
        )
    }

    params = {

        # 경도,위도 순서 주의

        "origin":
        f"{start_lng},{start_lat}",

        "destination":
        f"{end_lng},{end_lat}"
    }

    response = requests.get(

        url,

        headers=headers,

        params=params
    )

    data = response.json()

    routes = data.get("routes")

    if not routes:

        return None

    summary = routes[0]["summary"]

    duration = summary["duration"]

    # 초 → 분

    minutes = int(duration / 60)

    return minutes