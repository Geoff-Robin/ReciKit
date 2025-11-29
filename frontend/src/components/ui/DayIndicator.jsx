import React from 'react';

const DayIndicator = ({ days, currentDay, onDayClick }) => {
  return (
    <div className="flex justify-center gap-2 mb-8">
      {days.map((_, index) => (
        <button
          key={index}
          onClick={() => onDayClick(index)}
          className={`w-2 h-2 rounded-full transition-all ${
            index === currentDay ? 'bg-orange-600 w-8' : 'bg-gray-300 hover:bg-gray-400'
          }`}
        />
      ))}
    </div>
  );
};

export default DayIndicator;