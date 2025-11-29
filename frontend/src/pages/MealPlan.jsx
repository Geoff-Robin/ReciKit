import React, { useState } from 'react';
import { LogOut } from 'lucide-react';
import MealCard from '../components/ui/MealCard';
import DayNavigation from '../components/ui/DayNavigation';
import DayIndicator from '../components/ui/DayIndicator';
import { sampleMealPlan } from '../components/ui/sampledata';

const MealPlanApp = () => {
  const [currentDay, setCurrentDay] = useState(0);
  
  const weeklyMealPlan = sampleMealPlan; 
  const days = Object.keys(weeklyMealPlan);
  const meals = ['Breakfast', 'Lunch', 'Dinner'];
  
  const nextDay = () => {
    setCurrentDay((prev) => (prev + 1) % days.length);
  };
  
  const prevDay = () => {
    setCurrentDay((prev) => (prev - 1 + days.length) % days.length);
  };

  const handleLogout = () => {
    // Add your logout logic here
    console.log('Logging out...');
    // Example: Clear token, redirect to login, etc.
    // localStorage.removeItem('token');
    // navigate('/login');
  };

  const currentDayName = days[currentDay];
  const currentDayPlan = weeklyMealPlan[currentDayName];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Logout Button - Top Right */}
        <div className="flex justify-end mb-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 bg-white text-red-600 rounded-lg shadow-md hover:shadow-lg hover:bg-red-50 transition-all font-semibold"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">
            Weekly Meal Plan
          </h1>
          <p className="text-gray-600">Swipe through your delicious week ahead</p>
        </div>

        {/* Day Navigation */}
        <DayNavigation 
          currentDay={currentDay}
          currentDayName={currentDayName}
          onPrev={prevDay}
          onNext={nextDay}
        />

        {/* Day Indicator Dots */}
        <DayIndicator 
          days={days}
          currentDay={currentDay}
          onDayClick={setCurrentDay}
        />

        {/* Meals Container */}
        <div className="space-y-6">
          {meals.map((mealType) => (
            <MealCard 
              key={mealType}
              mealType={mealType}
              meal={currentDayPlan[mealType]}
            />
          ))}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Use arrow buttons or dots to navigate between days</p>
        </div>
      </div>
    </div>
  );
};

export default MealPlanApp;