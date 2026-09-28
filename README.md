# Fragrance Fit

Fragrance Fit is a Python project that recommends fragrances from a personal collection based on the current temperature and the user's occasion, season, vibe, and time of day. It shows the highest-scoring fragrances and the inputs each one matched.

**Status:** Work in progress. The command-line recommender runs with live weather for Indianapolis. The location selector and web interface are planned and are not part of the current version.

## What works now

- Fetches the current temperature in Fahrenheit for Indianapolis using the [Open-Meteo Forecast API](https://open-meteo.com/en/docs).
- Converts the temperature to a category: hot (80°F+), warm (70–79°F), mild (60–69°F), cool (45–59°F), or cold (below 45°F).
- Prompts for occasion, season, vibe, and time of day. Each prompt offers values found in the fragrance data and asks again if the input is invalid.
- Gives each fragrance one point for each matching category, up to five points total, and displays all fragrances tied for the highest score with their matching values. If the highest score is zero, it reports that no match was found.

The recommendations use **explicit rules**, not a trained machine-learning model. Several fragrances can tie when they match the same inputs.

## Run the command-line version

You need Python 3 and an internet connection. The current code uses only Python's standard library; no package installation or API key is required for Open-Meteo's noncommercial API access.

Keep these files in the same folder:

```text
fragrance-fit/
├── fragrance_data.py   # Fragrance collection and its tags
├── recommender.py      # Inputs, scoring, ranking, and output
└── weather.py          # Current temperature request
```

From that folder, run:

```bash
python3 recommender.py
```

Choose an occasion, season, vibe, and time of day when prompted. The program gets the Indianapolis temperature automatically and prints the top picks and their matching criteria. The temperature is currently fixed to Indianapolis in `weather.py`.

## How it works

1. `weather.py` requests `current=temperature_2m` in Fahrenheit from Open-Meteo and returns the number in the API's JSON response.
2. `recommender.py` places that number into one of five temperature categories.
3. Each fragrance in `fragrance_data.py` has lists of suitable temperatures, occasions, seasons, vibes, and times. A match in each list adds one point.
4. The results are sorted by score. All fragrances with the highest score are shown alongside the values that matched.

The current scoring gives all five criteria equal weight. It does not yet use the `projection` or `longevity_hours` data in its ranking.

## Planned improvements

- Let the user search for a city and use its coordinates for live weather.
- Handle weather-service errors and offer a manual-temperature fallback.
- Separate the scoring logic from terminal prompts so it can be reused in a Streamlit web interface.
- Review the scoring rules and optional projection/longevity preferences; test more combinations and document the results.
- Add a Streamlit interface, screenshots, and instructions for running or sharing it.

## Weather data

Weather data is provided by [Open-Meteo](https://open-meteo.com/). Location search, when added, will use its [Geocoding API](https://open-meteo.com/en/docs/geocoding-api). Open-Meteo requires attribution for its data; see its [licence and usage information](https://open-meteo.com/).
