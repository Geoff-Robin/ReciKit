import React from "react";

export function TypingIndicator() {
  return (
    <div className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-gray-900 w-fit text-gray-400 text-sm italic">
      
      <span className="typing-dots">
        <span>.</span>
        <span>.</span>
        <span>.</span>
      </span>
      <style jsx>{`
        .typing-dots span {
          animation: blink 1.4s infinite;
          font-weight: bold;
        }
        .typing-dots span:nth-child(2) {
          animation-delay: 0.2s;
        }
        .typing-dots span:nth-child(3) {
          animation-delay: 0.4s;
        }
        @keyframes blink {
          0%, 20% {
            opacity: 0;
          }
          50% {
            opacity: 1;
          }
          100% {
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
