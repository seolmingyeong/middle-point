import requests
import streamlit as st


# =========================
# Google API Key
# =========================

GOOGLE_MAPS_API_KEY = st.secrets[
    "GOOGLE_MAPS_API_KEY"
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
        "https://routes.googleapis.com/directions/v2:computeRoutes"
    )

    headers = {

        "Content-Type":
        "application/json",

        "X-Goog-Api-Key":
        GOOGLE_MAPS_API_KEY,

        "X-Goog-FieldMask":
        "routes.duration"
    }

    body = {

        "origin": {

            "location": {

                "latLng": {

                    "latitude":
                    start_lat,

                    "longitude":
                    start_lng
                }
            }
        },

        "destination": {

            "location": {

                "latLng": {

                    "latitude":
                    end_lat,

                    "longitude":
                    end_lng
                }
            }
        },

        "travelMode":
        "DRIVE"
    }

    try:

        response = requests.post(

            url,

            headers=headers,

            json=body
        )

        # =========================
        # 응답 출력
        # =========================

        print(
            "Google Routes Response:"
        )

        print(
            response.status_code
        )

        print(
            response.text
        )

        data = response.json()

        routes = data.get(
            "routes"
        )

        if not routes:

            return None

        duration = routes[0][
            "duration"
        ]

        # 예:
        # "1320s"

        seconds = int(

            duration.replace(
                "s",
                ""
            )
        )

        minutes = int(
            seconds / 60
        )

        return minutes

    except Exception as e:

        print(
            "Google Routes Error:"
        )

        print(e)

        return None