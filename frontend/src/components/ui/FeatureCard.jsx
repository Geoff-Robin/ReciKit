// File: src/components/ui/FeatureCard.jsx
import React from "react";

const FeatureCard = () => {
  const features = [
    {
      title: "Zero-Waste Kitchen",
      description:
        "Track groceries in real time, avoid duplicates, and reduce food waste — your pantry stays smart, and so do your meals.",
      icon: "M3 7h18v4H3V7z M4 11v8a1 1 0 001 1h14a1 1 0 001-1v-8 M8 13c2-2 5-2 7-0.5 M11 11c0.8-.8 2-1.2 3-0.8",
      gradient: "from-emerald-100 via-green-200 to-emerald-300",
      iconColor: "text-emerald-700",
    },
    {
      title: "Your Smart Chef",
      description:
        "Let AI plan your weekly menu, suggest recipes, and adapt to your mood, ingredients, and dietary needs — cooking has never been this effortless.",
      icon: "M6 11c0-2.5 2.2-4.5 4.8-4.5S15.6 8.5 15.6 11H6z M3 15h18 M8 15.2v4.5a1 1 0 001 1h6a1 1 0 001-1v-4.5",
      gradient: "from-green-100 via-emerald-200 to-emerald-400",
      iconColor: "text-green-800",
    },
    {
      title: "Chat. Cook. Repeat.",
      description:
        "Talk to your AI-powered kitchen assistant — get instant nutrition tips, allergy-safe recipes, and seamless voice commands for hands-free cooking.",
      icon: "M21 15a2 2 0 01-2 2H8l-5 4V5a2 2 0 012-2h14a2 2 0 012 2v10z M14.5 8.5c1.2 1.2 1.2 3.2 0 4.4l-1.1 1.1 M14 7.5a1.1 1.1 0 11-2.2 0 1.1 1.1 0 012.2 0z",
      gradient: "from-lime-100 via-green-200 to-emerald-300",
      iconColor: "text-lime-700",
    },
  ];

  return (
    <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6 px-4">
      {features.map((feature, index) => (
        <div
          key={index}
          className={`rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 p-6 transform hover:-translate-y-2 
          bg-gradient-to-br ${feature.gradient} relative overflow-hidden`}
        >
          {/* subtle overlay for contrast */}
          <div className="absolute inset-0 bg-white/50 backdrop-blur-[2px]"></div>

          <div className="relative z-10">
            <div
              className={`w-12 h-12 bg-white/60 backdrop-blur-md rounded-xl flex items-center justify-center mb-4 shadow-sm`}
            >
              <svg
                className={`w-7 h-7 ${feature.iconColor}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={feature.icon}
                />
              </svg>
            </div>

            <h3 className="text-lg font-bold text-gray-900 mb-2">
              {feature.title}
            </h3>
            <p className="text-gray-700 text-sm leading-relaxed">
              {feature.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default FeatureCard;
