import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const DayNavigation = ({ currentDay, currentDayName, onPrev, onNext }) => {
  return (
    <div className="flex items-center justify-between mb-6">
      <button
        onClick={onPrev}
        className="p-3 rounded-full bg-white shadow-lg hover:shadow-xl hover:bg-orange-50 transition-all"
      >
        <ChevronLeft className="w-6 h-6 text-orange-600" />
      </button>
      
      <div className="text-center">
        <h2 className="text-3xl font-bold text-orange-600">{currentDayName}</h2>
        <p className="text-sm text-gray-500">Day {currentDay + 1} of 7</p>
      </div>
      
      <button
        onClick={onNext}
        className="p-3 rounded-full bg-white shadow-lg hover:shadow-xl hover:bg-orange-50 transition-all"
      >
        <ChevronRight className="w-6 h-6 text-orange-600" />
      </button>
    </div>
  );
};

export default DayNavigation;