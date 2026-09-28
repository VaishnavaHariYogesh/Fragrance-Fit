"""Retrieve the current Indianapolis temperature from the Open-Meteo API."""

import json
from urllib.request import urlopen

def get_current_temperature():
    """Fetch and return the current temperature in degrees Fahrenheit."""
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=39.7684&longitude=-86.158&current=temperature_2m&timezone=auto&temperature_unit=fahrenheit"
    )

    with urlopen(url, timeout=10) as response:
        data = json.load(response)

    return data["current"]["temperature_2m"]
