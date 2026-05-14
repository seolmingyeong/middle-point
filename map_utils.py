import requests
import streamlit as st


KAKAO_API_KEY = st.secrets[
    "KAKAO_REST_API_KEY"
]

headers = {
    "Authorization":
    f"KakaoAK {KAKAO_API_KEY}"
}


def search_location(query):

    url = (
        "https://dapi.kakao.com/"
        "v2/local/search/keyword.json"
    )

    params = {
        "query": query
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if len(
        data.get("documents", [])
    ) == 0:

        return None

    place = data["documents"][0]

    return {
        "name": place["place_name"],
        "lat": float(place["y"]),
        "lng": float(place["x"]),
        "address": place.get(
            "road_address_name",
            "주소 없음"
        )
    }


def get_middle_point(locations):

    avg_lat = sum(
        [loc["lat"] for loc in locations]
    ) / len(locations)

    avg_lng = sum(
        [loc["lng"] for loc in locations]
    ) / len(locations)

    return avg_lat, avg_lng


def search_nearby_places(lat, lng):

    url = (
        "https://dapi.kakao.com/"
        "v2/local/search/category.json"
    )

    params = {
        "category_group_code": "CE7",
        "x": lng,
        "y": lat,
        "radius": 2000,
        "sort": "distance"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    places = []

    for place in data["documents"][:10]:

        places.append({
            "name": place["place_name"],
            "lat": float(place["y"]),
            "lng": float(place["x"]),
            "distance": int(place["distance"]),
            "address": place.get(
                "road_address_name",
                "주소 없음"
            )
        })

    return places