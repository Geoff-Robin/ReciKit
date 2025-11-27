import os
from dotenv import load_dotenv
import requests
import pytest

load_dotenv()
BASE_URL = os.environ["TEST_BASE_URL"]
ENDPOINT = "/mealplan/"  # replace if different
def assert_meal_item(mi):
    assert isinstance(mi, dict)
    for field in ("title", "directions", "ingredients", "reason"):
        assert field in mi
        assert isinstance(mi[field], str)
def assert_day_plan(dp):
    assert isinstance(dp, dict)
    for meal in ("Breakfast", "Lunch", "Dinner"):
        assert meal in dp
        assert_meal_item(dp[meal])

def test_weekly_meal_plan():
    url = f"{BASE_URL}{ENDPOINT}"
    r = requests.get(url, params={"likes": "chicken", "dislikes": "tomato"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)


    for day in (
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ):
        assert day in data
        assert_day_plan(data[day])


