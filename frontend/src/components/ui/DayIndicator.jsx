import React from 'react';

const DayIndicator = ({ days, currentDay, onDayClick }) => {
  return (
    <div className="flex justify-center gap-2 mb-8">
      {days.map((day, index) => (
        <button
          key={day}
          onClick={() => onDayClick(index)}
          className={`w-3 h-3 rounded-full transition-all ${
            index === currentDay
              ? 'bg-emerald-600 w-8'
              : 'bg-gray-300 hover:bg-gray-400'
          }`}
          aria-label={`Go to ${day}`}
        />
      ))}
    </div>
  );
};

export default DayIndicator;