"""Recommend fragrances using current weather and user-selected preferences.

Each matching temperature, occasion, season, vibe, or time of day adds one
point. The script displays every fragrance tied for the highest nonzero score.
"""

from fragrance_data import fragrances
from weather import get_current_temperature

def temperature(x):
    """Convert a Fahrenheit temperature into a weather category."""
    if x >= 80:
        return "hot"
    elif x >= 70:
        return "warm"
    elif x >= 60:
        return "mild"
    elif x >= 45:
        return "cool"
    else:
        return "cold"


def get_valid_choice(label, field):
    """Prompt until the user enters a category used by the fragrance catalog."""
    options = sorted({option for fragrance in fragrances for option in fragrance[field]})
    while True:
        value = input(f"Enter {label} ({', '.join(options)}): ").strip().lower()
        if value in options:
            return value
        print(f"Please choose one of these options: {', '.join(options)}")

input_temperature = get_current_temperature()

current_temp_category = temperature(input_temperature) 

occasion = get_valid_choice("the occasion", "occasions")
season = get_valid_choice("the season", "seasons")
vibe = get_valid_choice("the vibe", "vibes")
time_of_day = get_valid_choice("the time of day", "times")

def score_fragrance(fragrances, temp_category, occasion, season, vibe, time_of_day):
    """Return each fragrance's name, match score, and matched preferences."""
    scores = []
    for fragrance in fragrances:
        matches = []
        score = 0
        if temp_category in fragrance["temperature_categories"]:
            score += 1
            matches.append(temp_category)
        if occasion in fragrance["occasions"]:
            score += 1
            matches.append(occasion)
        if season in fragrance["seasons"]:
            score += 1
            matches.append(season)
        if vibe in fragrance["vibes"]:
            score += 1
            matches.append(vibe)
        if time_of_day in fragrance["times"]:
            score += 1
            matches.append(time_of_day)
        scores.append((score, matches))
    return [(fragrance['name'], score, matches) for fragrance, (score, matches) in zip(fragrances, scores)]

scored_fragrances = score_fragrance(fragrances, current_temp_category, occasion, season, vibe, time_of_day)
sorted_fragrances = sorted(scored_fragrances, key=lambda x: x[1], reverse=True)



top_pick_names = [sorted_fragrances[0][0]]
top_pick_score = sorted_fragrances[0][1]
top_pick_matches = [sorted_fragrances[0][2]]

if top_pick_score == 0:
    print("There are no suitable fragrances for the given conditions.")
else:
    for x in sorted_fragrances:
        if x[1] == top_pick_score:
            if x[0] not in top_pick_names:
                top_pick_names.append(x[0])
                top_pick_matches.append(x[2])


    print("Top picks with matching criteria:")
    for name, matches in zip(top_pick_names, top_pick_matches):
        print(f"{name}: {', '.join(matches)}")