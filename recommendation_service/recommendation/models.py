from pydantic import BaseModel
from typing import List

class MealItem(BaseModel):
    title: str
    directions: str
    ingredients: str
    reason: str


class DayPlan(BaseModel):
    Breakfast: List[MealItem]
    Lunch: List[MealItem]
    Dinner: List[MealItem]


class WeeklyMealPlan(BaseModel):
    Monday: DayPlan
    Tuesday: DayPlan
    Wednesday: DayPlan
    Thursday: DayPlan
    Friday: DayPlan
    Saturday: DayPlan
    Sunday: DayPlan
    InventoryNeeded: List[str]