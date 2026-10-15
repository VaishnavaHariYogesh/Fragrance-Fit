# Fragrance Fit

I built Fragrance Fit to help choose a fragrance based on the weather and what I'm choosing it for. I wanted to turn that idea into a program that could use live weather, take a few preferences, and explain why a fragrance matched.

I implemented the project with ChatGPT/Codex guidance, starting with a Python command-line program and extending it with an AWS Lambda backend connected to an AWS Amplify website.

The recommendations come from a tagged fragrance collection and a simple scoring system. This version uses rules rather than a trained machine-learning model.

## What it does

The program gets the current Indianapolis temperature and combines it with four choices:

- Occasion
- Season
- Vibe
- Time of day

Each fragrance can earn one point for matching each of those choices, plus one point for matching the temperature category. The highest possible score is five.

It returns every fragrance tied for the highest nonzero score, along with the values each one matched. If no fragrance scores above zero, it returns no recommendations.

## How it works

1. `weather.py` requests the current temperature in Fahrenheit from Open-Meteo.
2. `recommender.py` converts that temperature into a category.
3. The scoring function compares the five criteria with each fragrance's tags.
4. The program finds the highest score and returns all fragrances with that score.
5. The command-line version prints the results. The Lambda handler returns them as JSON for the website.

All five criteria have equal weight. The catalog also stores projection and longevity information, but those fields aren't used in the current scoring.

### Temperature categories

| Category | Temperature in Fahrenheit |
| --- | --- |
| Hot | 80 or above |
| Warm | 70 up to, but below, 80 |
| Mild | 60 up to, but below, 70 |
| Cool | 45 up to, but below, 60 |
| Cold | Below 45 |

The weather location is currently fixed to Indianapolis in `weather.py`.

## The API and website

I deployed the backend to AWS Lambda and connected it to a website hosted through AWS Amplify. This repository currently contains the Python backend and its tests; the website's HTML source hasn't been added here yet.

The Lambda handler receives `occasion`, `season`, `vibe`, and `time_of_day` as query-string parameters. It checks them before requesting weather or running the recommender. Accepted values come from the fragrance catalog, and text inputs are trimmed and converted to lowercase.

| Request or service condition | Response |
| --- | --- |
| All preferences are valid and weather is available | `200` with temperature information and recommendations |
| A required preference is missing | `400` identifying the missing fields |
| A preference isn't an allowed option | `400` identifying the invalid field and listing allowed values |
| Weather retrieval fails with a handled network or data error | `502` with an error message |

The weather request has a ten-second timeout. The API reports a weather error instead of returning recommendations based on an assumed temperature.

## My work and AI assistance

I implemented Fragrance Fit with ChatGPT/Codex guidance. I chose the project idea and worked through the scoring, weather integration, backend, deployment, and testing as I developed it.

The goal was to build something I could use while learning how to connect a Python program to an external API and make it available through a website. I used assistance with technical decisions, code examples, unfamiliar concepts, and debugging throughout the process.

| My work | ChatGPT/Codex's guidance |
| --- | --- |
| Defined the recommendation idea, the inputs, and how the fragrance tags would be used. | Helped work through the scoring approach and organize the program into functions and modules. |
| Implemented the scoring and weather integration with guidance, including returning all top-scoring ties. | Explained API requests and JSON responses, provided code examples, and helped with refactoring and debugging. |
| Implemented the Lambda handler and connected the backend to the Amplify website with guidance. | Helped explain the AWS integration, request handling, validation, and error handling. |
| Implemented and ran the API tests, then expanded validation checks to cover all four preferences. | Provided test examples and explained mocking, subtests, and how to check expected behavior. |
| Configured GitHub Actions to run the tests automatically, with guidance. | Provided workflow examples and setup explanations. |

Some code and test examples were AI-generated and incorporated into the project. I used that guidance while implementing, testing, and extending the program. This README was also written and edited with AI assistance.

## Running it locally

Use Python 3.10 or newer. The Python backend and tests use the standard library, so they don't need additional packages. The command-line version needs an internet connection for live weather; the offline tests don't.

Open a terminal in the project folder and run:

```bash
python3 recommender.py
```

Choose an occasion, season, vibe, and time of day when prompted. The choices shown in the terminal come from the catalog. The program gets the current Indianapolis temperature automatically and prints the top recommendations with their matching values.

### Example Lambda test event

This is the event format the handler expects. It can be used for a test in the Lambda console:

```json
{
  "queryStringParameters": {
    "occasion": "college",
    "season": "summer",
    "vibe": "fresh",
    "time_of_day": "day"
  }
}
```

The response body is a JSON string. A successful response includes `temperature_f`, `temperature_category`, `weather_source`, and a `recommendations` list. Each recommendation includes its name, score, and matching values.

## Testing

Run the tests from the project folder:

```bash
python3 -m unittest discover -v
```

There are currently **four test methods covering ten scenarios**:

| Test | What it checks | Scenarios |
| --- | --- | --- |
| Valid request | At a simulated 72 F, college/summer/fresh/day returns Explorer EDP, MYSLF EDP, and Pacific Cliff, each with five points. | 1 |
| Missing preferences | Each of occasion, season, vibe, and time of day is removed individually. The handler returns `400`, names the missing field, and doesn't request weather. | 4 |
| Invalid preferences | Each field is given an invalid option individually. The handler returns `400`, identifies that field, includes a known valid option, and doesn't request weather. | 4 |
| Weather failure | A simulated network failure produces `502` and an error message without recommendations. | 1 |

The weather function is mocked so results don't depend on the current forecast or an internet connection. The test runner still reports `Ran 4 tests` because the field checks use subtests inside two methods.

The printed `Simulated weather outage` message is expected during the failure test.

GitHub Actions runs the offline tests on pushes and pull requests. The workflow can also be started manually, and it currently uses Python 3.12.

These tests check the Python handler and scoring behavior exercised by the requests. Testing the deployed website also involves checking the browser, request routing, and the connection to Lambda.

## Files

| File | What it's for |
| --- | --- |
| `fragrance_data.py` | Fragrance names, brands, tags, and performance details |
| `weather.py` | Fetching the current Indianapolis temperature |
| `recommender.py` | Temperature categories, preference prompts, scoring, and top matches |
| `lambda_function.py` | API request validation, weather error handling, and JSON responses |
| `test_api.py` | Offline tests for recommendations, preference validation, and weather failures |
| `.github/workflows/tests.yml` | Automatic test runs on GitHub |

## What I want to work on next

- Add the website source and a live-demo link to this repository.
- Let users choose a city for the weather lookup.
- Explore a manual-temperature option when live weather isn't available.
- Add focused tests for temperature boundaries, empty catalogs, and zero-score results.
- Review whether projection or longevity should affect the recommendations.

## Weather data

Weather data comes from [Open-Meteo](https://open-meteo.com/). The request uses its [Forecast API](https://open-meteo.com/en/docs) for Indianapolis, with the current temperature returned in Fahrenheit.
