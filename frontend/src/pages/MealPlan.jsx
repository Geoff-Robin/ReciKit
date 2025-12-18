import React, { useState } from 'react';
import { LogOut, MessageCircle } from 'lucide-react';
<<<<<<< HEAD
import { useNavigate } from 'react-router-dom';
=======
>>>>>>> main
import MealCard from '../components/ui/MealCard';
import DayNavigation from '../components/ui/DayNavigation';
import DayIndicator from '../components/ui/DayIndicator';
import { sampleMealPlan } from '../components/ui/sampledata';
import ChatWidget from '@/pages/ChatWidget';

const MealPlanApp = () => {
  const [currentDay, setCurrentDay] = useState(0);
<<<<<<< HEAD
  const navigate = useNavigate(); 
  
  const weeklyMealPlan = sampleMealPlan; 
  const days = Object.keys(weeklyMealPlan).filter(day => day !== 'InventoryNeeded');
=======
  const [isChatOpen, setIsChatOpen] = useState(false);

  const weeklyMealPlan = sampleMealPlan;
  const days = Object.keys(weeklyMealPlan);
>>>>>>> main
  const meals = ['Breakfast', 'Lunch', 'Dinner'];

  const nextDay = () => {
    setCurrentDay((prev) => (prev + 1) % days.length);
  };

  const prevDay = () => {
    setCurrentDay((prev) => (prev - 1 + days.length) % days.length);
  };

  const handleLogout = () => {
    console.log('Logging out...');
  };

  const handleChatbotClick = () => {
    setIsChatOpen(true);
  };

  const currentDayName = days[currentDay];
  const currentDayPlan = weeklyMealPlan[currentDayName];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-4 md:p-8">
<<<<<<< HEAD
      <div className="max-w-6xl mx-auto">
        {/* Logout Button - Top Right */}
=======
      <div className="max-w-4xl mx-auto">
        {/* Logout */}
>>>>>>> main
        <div className="flex justify-end mb-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 bg-white text-red-600 rounded-lg shadow-md hover:shadow-lg"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Weekly Meal Plan
          </h1>
          <p className="text-gray-600">
            Swipe through your delicious week ahead
          </p>
        </div>

        <DayNavigation
          currentDay={currentDay}
          currentDayName={Object.keys(weeklyMealPlan)[currentDay]}
          onPrev={prevDay}
          onNext={nextDay}
        />

        <DayIndicator
          days={days}
          currentDay={currentDay}
          onDayClick={setCurrentDay}
        />

<<<<<<< HEAD
        {/* Meals Container */}
        <div className="space-y-8">
          {meals.map((mealType) => (
            <div key={mealType} className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 border-b-2 border-emerald-500 pb-2">
                {mealType}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {currentDayPlan[mealType]?.map((meal, index) => (
                  <MealCard 
                    key={`${currentDayName}-${mealType}-${index}`}
                    meal={meal}
                  />
                ))}
              </div>
            </div>
=======
        <div className="space-y-6">
          {meals.map((mealType) => (
            <MealCard
              key={mealType}
              mealType={mealType}
              meal={currentDayPlan[mealType]}
            />
>>>>>>> main
          ))}
        </div>

        <div className="mt-8 text-center text-gray-500 text-sm">
          Use arrow buttons or dots to navigate between days
        </div>
      </div>

      {/* Floating Button */}
      <button
        onClick={handleChatbotClick}
        className="fixed bottom-6 right-6 bg-emerald-600 hover:bg-emerald-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-transform hover:scale-110 z-50"
        aria-label="Open Chatbot"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Chat Widget */}
      <ChatWidget
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
      />
    </div>
  );
};

export default MealPlanApp;