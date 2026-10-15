"""Tests for the fragrance recommendation API.

These tests check that the Lambda handler behaves correctly for valid input,
missing or invalid preferences, and weather-related failures.
"""

import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

from lambda_function import lambda_handler


class APITests(unittest.TestCase):
    """Simple API tests for the fragrance recommendation endpoint."""

    def setUp(self):
        """Create a valid request payload used by most tests."""
        self.event = {
            "queryStringParameters": {
                "occasion": "college",
                "season": "summer",
                "vibe": "fresh",
                "time_of_day": "day"
            }
        }

    @patch("lambda_function.get_current_temperature", return_value=72)
    def test_valid_request_returns_top_matches(self, mock_weather):
        """A valid request should return a 200 response with top recommendations."""
        response = lambda_handler(self.event, None)
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["temperature_f"], 72)
        self.assertEqual(body["temperature_category"], "warm")

        names = {
            item["name"] for item in body["recommendations"]
        }
        self.assertEqual(names, {
            "Explorer EDP", "MYSLF EDP", "Pacific Cliff"
        })
        self.assertTrue(all(
            item["score"] == 5
            for item in body["recommendations"]
        ))
        mock_weather.assert_called_once_with()

    @patch("lambda_function.get_current_temperature")
    def test_missing_preference_returns_400(self, mock_weather):
        """If a required preference is missing, return a 400 error."""
        for field in ["occasion", "season", "vibe", "time_of_day"]:
            with self.subTest(field=field):
                params = self.event["queryStringParameters"].copy()
                del params[field]
                event = {"queryStringParameters": params}

                response = lambda_handler(event, None)
                body = json.loads(response["body"])

                self.assertEqual(response["statusCode"], 400)
                self.assertEqual(body["missing_fields"], [field])
                mock_weather.assert_not_called()

    @patch("lambda_function.get_current_temperature")
    def test_invalid_preference_returns_400(self, mock_weather):
        """If a preference value is invalid, return a clear 400 response."""
        for field in ["occasion", "season", "vibe", "time_of_day"]:
            with self.subTest(field=field):
                params = self.event["queryStringParameters"].copy()
                params[field] = "not_a_valid_option"
                event = {"queryStringParameters": params}

                response = lambda_handler(event, None)
                body = json.loads(response["body"])

                self.assertEqual(response["statusCode"], 400)
                self.assertEqual(
                    body["error"], f"Invalid value for {field}."
                )
                self.assertIn(
                    self.event["queryStringParameters"][field],
                    body["allowed_values"]
                )
                mock_weather.assert_not_called()

    @patch("lambda_function.get_current_temperature")
    def test_weather_failure_returns_502(self, mock_weather):
        """If the weather API fails, the service should return a 502 error."""
        mock_weather.side_effect = URLError(
            "Simulated weather outage"
        )

        response = lambda_handler(self.event, None)
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 502)
        self.assertIn("error", body)
        self.assertNotIn("recommendations", body)


if __name__ == "__main__":
    unittest.main()