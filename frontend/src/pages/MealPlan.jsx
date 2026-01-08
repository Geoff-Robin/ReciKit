import React, { useState, useEffect } from "react";
import { LogOut, MessageCircle } from "lucide-react";
import { useNavigate, Link } from "react-router-dom";
import MealCard from "@/components/ui/MealCard";
import DayNavigation from "@/components/ui/DayNavigation";
import DayIndicator from "@/components/ui/DayIndicator";

const checkAndLoad = (setWeeklyMealPlan, setLoading) => {
  fetch(import.meta.env.VITE_BACKEND_URL + "/api/auth/check", {
    method: "GET",
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Auth check failed");
      }
      return fetch(
        import.meta.env.VITE_BACKEND_URL + "/api/recommendations",
        {
          method: "GET",
          credentials: "include",
        }
      );
    })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`API Error: ${res.status} ${res.statusText}`);
      }
      return res.json();
    })
    .then((data) => {
      if (data && typeof data === 'object' && !data.detail) {
        setWeeklyMealPlan(data);
      } else {
        console.error("Invalid data structure received:", data);
        setWeeklyMealPlan(null);
      }
      setLoading(false);
    })
    .catch((err) => {
      console.error(err.message);
      setLoading(false);
    });
};

const MealPlanApp = () => {
  const [currentDay, setCurrentDay] = useState(0);
  const [weeklyMealPlan, setWeeklyMealPlan] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    checkAndLoad(setWeeklyMealPlan, setLoading);
  }, []);

  const handleLogout = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(
        import.meta.env.VITE_BACKEND_URL + "/api/auth/logout",
        {
          method: "POST",
          credentials: "include",
        }
      );
      if (res.ok) {
        navigate("/login");
      }
    } catch {
      return;
    }
  };

  const handleChatbotClick = () => {
    navigate("/chatbot");
  };

  /* -------------------- LOADING STATE -------------------- */
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-600 font-medium">Loading your meal plan...</p>
        </div>
      </div>
    );
  }

  /* -------------------- ERROR STATE -------------------- */
  if (!weeklyMealPlan) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p>No data fetched! Call support or check internet.</p>
          <Link
            className="hover:underline text-emerald-600"
            onClick={handleLogout}
            to="/"
          >
            Go back to login page
          </Link>
        </div>
      </div>
    );
  }

  /* -------------------- DERIVED DATA -------------------- */
  const days = Object.keys(weeklyMealPlan).filter(
    (day) => day !== "InventoryNeeded"
  );

  const meals = ["Breakfast", "Lunch", "Dinner"];

  const nextDay = () => {
    setCurrentDay((prev) => (prev + 1) % days.length);
  };

  const prevDay = () => {
    setCurrentDay((prev) => (prev - 1 + days.length) % days.length);
  };

  const currentDayName = days[currentDay];
  const currentDayPlan = weeklyMealPlan[currentDayName];

  /* -------------------- MAIN UI -------------------- */
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Logout Button */}
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
          <p className="text-gray-600">
            Swipe through your delicious week ahead
          </p>
        </div>

        {/* Day Navigation */}
        <DayNavigation
          currentDay={currentDay}
          currentDayName={currentDayName}
          onPrev={prevDay}
          onNext={nextDay}
        />

        {/* Day Indicator */}
        <DayIndicator
          days={days}
          currentDay={currentDay}
          onDayClick={setCurrentDay}
        />

        {/* Meals */}
        <div className="space-y-8">
          {meals.map((mealType) => (
            <div key={mealType} className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-800 border-b-2 border-emerald-500 pb-2">
                {mealType}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Array.isArray(currentDayPlan[mealType]) && currentDayPlan[mealType].map((meal, index) => (
                  <MealCard
                    key={`${currentDayName}-${mealType}-${index}`}
                    meal={meal}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Use arrow buttons or dots to navigate between days</p>
        </div>

        {/* Chatbot Button */}
        <button
          onClick={handleChatbotClick}
          className="fixed bottom-6 right-6 bg-emerald-600 hover:bg-emerald-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all z-50"
          aria-label="Open Chatbot"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
};

export default MealPlanApp;
