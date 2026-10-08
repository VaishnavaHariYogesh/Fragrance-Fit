"""AWS Lambda entry point for the fragrance recommendation API.

This function receives a request from API Gateway, validates the user's scent
preferences, checks the current weather, and returns the best fragrance matches.
The logic is intentionally simple:
1. read the query parameters
2. verify required values are present
3. confirm values are valid options
4. fetch the current temperature
5. get the top fragrance recommendations
"""

import json

from recommender import temperature, get_top_picks
from weather import get_current_temperature
from fragrance_data import fragrances
from urllib.error import URLError


def lambda_handler(event, context):
    """Handle a fragrance recommendation request.

    The event should include query-string parameters like:
    occasion, season, vibe, and time_of_day.

    Returns a JSON response with either:
    - an error message when data is missing or invalid
    - a 200 response with weather and recommendation results
    """
    params = event.get("queryStringParameters") or {}

    # Required user preferences for the recommendation engine.
    required_fields = ["occasion", "season", "vibe", "time_of_day"]
    missing_fields = [
        field for field in required_fields
        if not params.get(field)
    ]

    # Stop early if the request is incomplete.
    if missing_fields:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Please provide all required preferences.",
                "missing_fields": missing_fields
            })
        }

    # Match each incoming value against the allowed values stored in fragrance_data.
    fields = {
        "occasion": "occasions",
        "season": "seasons",
        "vibe": "vibes",
        "time_of_day": "times"
    }

    for parameter, catalog_field in fields.items():
        value = params[parameter]
        options = sorted({
            option
            for fragrance in fragrances
            for option in fragrance[catalog_field]
        })

        if not isinstance(value, str) or value.strip().lower() not in options:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": f"Invalid value for {parameter}.",
                    "allowed_values": options
                })
            }

        params[parameter] = value.strip().lower()

    # Cleaned preference values passed to the recommender.
    occasion = params["occasion"]
    season = params["season"]
    vibe = params["vibe"]
    time_of_day = params["time_of_day"]

    try:
        # Get the live temperature and convert it into a general category such as
        # cold, mild, warm, or hot.
        current_temperature = get_current_temperature()
        temp_category = temperature(current_temperature)
    except (URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
        print(f"Weather lookup failed: {error}")
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Could not retrieve the weather. Please try again later."
            })
        }

    # Ask the recommender for the best fragrance suggestions for the user's
    # chosen conditions.
    top_picks = get_top_picks(
        temp_category,
        occasion,
        season,
        vibe,
        time_of_day
    )

    # Return a clean JSON payload for the frontend or API client.
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "temperature_f": current_temperature,
            "temperature_category": temp_category,
            "weather_source": "https://open-meteo.com/",
            "recommendations": [
                {"name": name, "score": score, "matches": matches}
                for name, score, matches in top_picks
            ]
        })
    }