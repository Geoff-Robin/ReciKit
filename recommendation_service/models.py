from pydantic import BaseModel


class MealItem(BaseModel):
    title: str
    directions: str
    ingredients: str
    reason: str


class DayPlan(BaseModel):
    Breakfast: MealItem
    Lunch: MealItem
    Dinner: MealItem


class WeeklyMealPlan(BaseModel):
    Monday: DayPlan
    Tuesday: DayPlan
    Wednesday: DayPlan
    Thursday: DayPlan
    Friday: DayPlan
    Saturday: DayPlan
    Sunday: DayPlan
