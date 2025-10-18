import React from "react";

export function PromptSuggestions({ label, append, suggestions }) {
  return (
    <div className="w-full mb-8">
      <h2 className="text-center text-2xl font-bold text-black mb-5">{label}</h2>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => append({ role: "user", content: suggestion })}
            className="flex-1 py-3 px-6 rounded-full bg-black text-white font-semibold shadow transition hover:scale-105 hover:bg-gray-900 focus:outline-none"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
}
