import requests


def get_route_time(
    start_lat,
    start_lng,
    end_lat,
    end_lng,
    transport
):

    profile_map = {
        "도보": "walking",
        "자전거": "cycling",
        "자동차": "driving"
    }

    # =========================
    # 대중교통 임시 처리
    # =========================

    if transport == "대중교통":

        profile = "driving"

    else:

        profile = profile_map.get(
            transport,
            "walking"
        )

    url = (
        f"https://router.project-osrm.org/"
        f"route/v1/"
        f"{profile}/"
        f"{start_lng},{start_lat};"
        f"{end_lng},{end_lat}"
        f"?overview=false"
    )

    print("현재 이동수단:", transport)
    print("사용 profile:", profile)
    print("요청 URL:", url)

    response = requests.get(url)

    data = response.json()

    print("응답:", data)

    routes = data.get("routes")

    if not routes:

        return 9999

    duration_sec = (
        routes[0]["duration"]
    )

    duration_min = (
        duration_sec / 60
    )

    # =========================
    # 대중교통 보정
    # =========================

    if transport == "대중교통":

        duration_min = (
            duration_min * 1.4 + 10
        )

    return round(duration_min, 1)


def calculate_place_score(
    users,
    place
):

    total_time = 0

    max_time = 0

    for user in users:

        time = get_route_time(
            user["lat"],
            user["lng"],
            place["lat"],
            place["lng"],
            user["transport"]
        )

        total_time += time

        if time > max_time:

            max_time = time

    avg_time = (
        total_time / len(users)
    )

    score = (
        avg_time * 0.7 +
        max_time * 0.3
    )

    return {
        "score": score,
        "avg_time": round(avg_time, 1),
        "max_time": round(max_time, 1)
    }