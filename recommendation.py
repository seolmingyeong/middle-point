from route_api import (
    get_car_travel_time
)


# =========================
# 평균 좌표 계산
# =========================

def get_middle_point(users):

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
# 후보 위치 생성
# =========================

def generate_candidates(

    middle_lat,
    middle_lng
):

    offset = 0.005

    return [

        (
            middle_lat,
            middle_lng
        ),

        (
            middle_lat + offset,
            middle_lng
        ),

        (
            middle_lat - offset,
            middle_lng
        ),

        (
            middle_lat,
            middle_lng + offset
        ),

        (
            middle_lat,
            middle_lng - offset
        )
    ]


# =========================
# 추천 장소 생성
# =========================

def recommend_places(

    users,

    middle_lat,
    middle_lng
):

    candidates = generate_candidates(

        middle_lat,
        middle_lng
    )

    best_place = None

    best_score = float("inf")

    # =========================
    # 후보 위치 평가
    # =========================

    for lat, lng in candidates:

        times = []

        for user in users:

            travel_time = (

                get_car_travel_time(

                    user["lat"],
                    user["lng"],

                    lat,
                    lng
                )
            )

            if travel_time is not None:

                times.append(
                    travel_time
                )

        if not times:
            continue

        avg_time = int(
            sum(times)
            / len(times)
        )

        max_time = max(times)

        # =========================
        # 점수 계산
        # =========================

        score = (
            avg_time
            + max_time
        )

        if score < best_score:

            best_score = score

            best_place = {

                "name":
                "최적 약속 장소",

                "lat":
                lat,

                "lng":
                lng,

                "address":
                "이동시간 기반 추천",

                "avg_time":
                avg_time,

                "max_time":
                max_time
            }

    return [best_place]