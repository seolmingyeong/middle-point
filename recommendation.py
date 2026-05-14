from map_utils import (
    search_nearby_places
)

from scoring import (
    calculate_place_score
)


def recommend_places(
    users,
    middle_lat,
    middle_lng
):

    places = search_nearby_places(
        middle_lat,
        middle_lng
    )

    results = []

    for place in places:

        score_data = (
            calculate_place_score(
                users,
                place
            )
        )

        place.update(score_data)

        results.append(place)

    results.sort(
        key=lambda x: x["score"]
    )

    return results