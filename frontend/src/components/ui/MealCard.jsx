import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const MealCard = ({ meal }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
      {/* Card Header */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-800 mb-2">
              {meal.title}
            </h3>
            <p className="text-sm text-emerald-600 font-medium mb-2">
              Why this meal: {meal.reason}
            </p>
          </div>
          <div className="ml-4 text-emerald-600">
            {isExpanded ? <ChevronUp className="w-6 h-6" /> : <ChevronDown className="w-6 h-6" />}
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="p-4 pt-0 border-t border-gray-100">
          {/* Ingredients Section */}
          <div className="mb-4">
            <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
              <span className="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-sm">
                Ingredients
              </span>
            </h4>
            <ul className="space-y-1 ml-2">
              {meal.ingredients?.map((ingredient, index) => (
                <li key={index} className="text-gray-700 text-sm">
                  • {ingredient.name}: {ingredient.quantity} {ingredient.metric}
                </li>
              ))}
            </ul>
          </div>

          {/* Preparation Steps */}
          <div>
            <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
              <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
                Preparation Steps
              </span>
            </h4>
            <div className="bg-gray-50 p-3 rounded-lg">
              <p className="text-gray-700 text-sm whitespace-pre-line">
                {meal.directions}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MealCard;