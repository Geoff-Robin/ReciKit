import React from 'react';
import { Utensils, Clock, ChefHat } from 'lucide-react';

const MealCard = ({ mealType, meal }) => {
  const getMealIcon = (mealName) => {
    if (mealName === 'Breakfast') return <ChefHat className="w-5 h-5" />;
    if (mealName === 'Lunch') return <Utensils className="w-5 h-5" />;
    return <Clock className="w-5 h-5" />;
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-shadow p-6 border border-gray-100">
      {/* Meal Header */}
      <div className="flex items-center gap-3 mb-4 pb-4 border-b border-gray-100">
        <div className="p-2 bg-orange-100 rounded-lg text-orange-600">
          {getMealIcon(mealType)}
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">
            {mealType}
          </h3>
          <h4 className="text-xl font-bold text-gray-800">{meal.title}</h4>
        </div>
      </div>

      {/* Reason Badge */}
      <div className="mb-4 p-3 bg-amber-50 rounded-lg border-l-4 border-amber-400">
        <p className="text-sm text-gray-700">
          <span className="font-semibold text-amber-700">Why this meal: </span>
          {meal.reason}
        </p>
      </div>

      {/* Ingredients */}
      <div className="mb-4">
        <h5 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <span className="w-1 h-4 bg-orange-500 rounded"></span>
          Ingredients
        </h5>
        <p className="text-gray-600 text-sm leading-relaxed pl-3">
          {meal.ingredients}
        </p>
      </div>

      {/* Directions */}
      <div>
        <h5 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <span className="w-1 h-4 bg-orange-500 rounded"></span>
          Directions
        </h5>
        <p className="text-gray-600 text-sm leading-relaxed pl-3">
          {meal.directions}
        </p>
      </div>
    </div>
  );
};

export default MealCard;