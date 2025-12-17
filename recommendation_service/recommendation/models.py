from pydantic import BaseModel
from typing import List, Literal

class Ingredient(BaseModel):
    name: str
    quantity: int
    metric: Literal['gram', 'kilogram', 'milimeter', 'liter']

class MealItem(BaseModel):
    title: str
    directions: str
    ingredients: List[Ingredient]
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
    InventoryNeeded: List[Ingredient]