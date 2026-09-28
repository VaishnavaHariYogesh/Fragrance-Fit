"""Fragrance catalog used by the recommendation script.

Each fragrance is a dictionary with descriptive fields, preference categories,
and performance details. Category values are lists so one fragrance can match
multiple seasons, temperatures, occasions, vibes, or times of day.
"""

fragrances = [
    {
        "name": "The Most Wanted Parfum",
        "brand": "Azzaro",
        "seasons": ["fall", "winter"],
        "temperature_categories": ["cool", "cold"],
        "occasions": ["college", "date", "party", "casual"],
        "vibes": ["confident", "attractive", "bold"],
        "times": ["day", "night"],
        "projection": 4,
        "longevity_hours": 8
    },
    {
        "name": "Eros EDT",
        "brand": "Versace",
        "seasons": ["fall", "winter", "spring"],
        "temperature_categories": ["mild", "cool", "cold"],
        "occasions": ["party"],
        "vibes": ["bold", "attractive", "energetic"],
        "times": ["night"],
        "projection": 3,
        "longevity_hours": 6
    },
    {
        "name": "Liquid Brun",
        "brand": "French Avenue",
        "seasons": ["fall", "winter", "spring"],
        "temperature_categories": ["mild", "cool", "cold"],
        "occasions": ["college", "date", "casual"],
        "vibes": ["relaxed", "attractive", "confident"],
        "times": ["day", "night"],
        "projection": 4,
        "longevity_hours": 8
    },
    {
        "name": "9PM Night Out",
        "brand": "Afnan",
        "seasons": ["fall", "winter", "spring"],
        "temperature_categories": ["mild", "cool", "cold"],
        "occasions": ["party", "date"],
        "vibes": ["confident", "attractive", "bold", "energetic"],
        "times": ["night"],
        "projection": 5,
        "longevity_hours": 9
    },
    {
        "name": "Late Night Drive",
        "brand": "Hollister",
        "seasons": ["spring", "summer", "fall"],
        "temperature_categories": ["warm", "mild", "cool"],
        "occasions": ["casual", "gym", "date"],
        "vibes": ["relaxed", "attractive", "fresh"],
        "times": ["day", "night"],
        "projection": 2,
        "longevity_hours": 5
    },
    {
        "name": "Explorer EDP",
        "brand": "Montblanc",
        "seasons": ["spring", "summer", "fall"],
        "temperature_categories": ["hot", "warm", "mild", "cool"],
        "occasions": ["college", "work", "formal", "casual"],
        "vibes": ["fresh", "confident", "professional"],
        "times": ["day", "night"],
        "projection": 3,
        "longevity_hours": 7
    },
    {
        "name": "MYSLF EDP",
        "brand": "Yves Saint Laurent",
        "seasons": ["spring", "summer", "fall"],
        "temperature_categories": ["hot", "warm", "mild", "cool"],
        "occasions": ["college", "work", "date", "formal", "casual"],
        "vibes": ["fresh", "confident", "attractive", "professional"],
        "times": ["day", "night"],
        "projection": 3,
        "longevity_hours": 7
    },
    {
        "name": "Ralph's Club New York EDP",
        "brand": "Ralph Lauren",
        "seasons": ["spring", "summer", "fall", "winter"],
        "temperature_categories": ["warm", "mild", "cool", "cold"],
        "occasions": ["formal", "date", "party", "work"],
        "vibes": ["confident", "professional", "attractive", "bold"],
        "times": ["night"],
        "projection": 4,
        "longevity_hours": 8
    },
    {
        "name": "Stronger With You Intensely",
        "brand": "Emporio Armani",
        "seasons": ["fall", "winter", "spring"],
        "temperature_categories": ["mild", "cool", "cold"],
        "occasions": ["date", "party", "casual"],
        "vibes": ["attractive", "confident", "bold", "relaxed"],
        "times": ["night"],
        "projection": 4,
        "longevity_hours": 9
    },
    {
        "name": "Pacific Cliff",
        "brand": "Hollister",
        "seasons": ["spring", "summer"],
        "temperature_categories": ["hot", "warm", "mild"],
        "occasions": ["college", "casual", "gym"],
        "vibes": ["fresh", "relaxed", "energetic"],
        "times": ["day"],
        "projection": 2,
        "longevity_hours": 4
    }
]