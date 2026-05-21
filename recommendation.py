import math


# =========================
# 사용자 중간 좌표 계산
# =========================

def get_middle_point(users):

    if not users:
        return None, None

    avg_lat = sum(
        user["lat"]
        for user in users
    ) / len(users)

    avg_lng = sum(
        user["lng"]
        for user in users
    ) / len(users)

    return avg_lat, avg_lng


# =========================
# 추천 장소 생성
# =========================

def recommend_places(
    users,
    middle_lat,
    middle_lng
):

    if middle_lat is None:
        return []

    return [

        {
            "name": "중간 약속 장소",

            "lat": middle_lat,

            "lng": middle_lng,

            "address": "중간 위치 기반 추천",

            "avg_time": 25,

            "max_time": 40
        }

    ]