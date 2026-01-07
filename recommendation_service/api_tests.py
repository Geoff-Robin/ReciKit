import os
from dotenv import load_dotenv
import requests
from recommendation.models import MealItem
from typing import Literal

load_dotenv()
BASE_URL = os.environ["TEST_BASE_URL"]
ENDPOINT = "/mealplan/"


def assert_meal_item(mi: MealItem):
    assert isinstance(mi, dict)
    for field in ("title", "directions", "ingredients", "reason"):
        if field == "ingredients":
            assert isinstance(mi[field], list)
            print(mi)
            ingredients = mi["ingredients"]
            for ingredient in ingredients:
                assert isinstance(ingredient, dict)
                assert isinstance(ingredient["name"], str)
                assert isinstance(ingredient["quantity"], str) or isinstance(
                    ingredient["quantity"], int
                )
                assert isinstance(ingredient["metric"], str)
            continue
        assert field in mi
        assert isinstance(mi[field], str)


def assert_day_plan(dp):
    assert isinstance(dp, dict)
    for meal in ("Breakfast", "Lunch", "Dinner"):
        assert meal in dp
        assert isinstance(dp[meal], list)
        for mi in dp[meal]:
            assert_meal_item(mi)


def test_weekly_meal_plan():
    url = f"{BASE_URL}{ENDPOINT}"
    r = requests.get(
        url,
        params={
            "inventory": "chicken onion tomato garlic spring onions rice noodles green beans rice flour",
            "likes": "chicken",
            "allergies": "tomato",
        },
    )
    assert r.status_code == 200
    data = r.json()
    print(data)
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

    # new: validate InventoryNeeded at root
    assert "InventoryNeeded" in data
    assert isinstance(data["InventoryNeeded"], list)
    for item in data["InventoryNeeded"]:
        assert isinstance(item, dict)
        assert isinstance(item["name"], str)
        assert isinstance(item["quantity"], str) or isinstance(item["quantity"], int)
        assert isinstance(item["metric"], str)
