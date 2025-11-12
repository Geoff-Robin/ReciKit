import React from "react";
import { Salad, Clock, Brain, Globe } from "lucide-react";

const LifestyleSection = () => {
  const features = [
    {
      icon: <Salad className="w-5 h-5" />,
      text: "Personalized meal plans for your health goals",
    },
    {
      icon: <Clock className="w-5 h-5" />,
      text: "Instant recipe suggestions from your pantry",
    },
    {
      icon: <Brain className="w-5 h-5" />,
      text: "AI that learns your preferences over time",
    },
    {
      icon: <Globe className="w-5 h-5" />,
      text: "Reduce food waste and save money effortlessly",
    },
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-emerald-50 via-green-100 to-emerald-200 overflow-hidden relative">
      <div className="max-w-7xl mx-auto px-6 lg:px-12">
        <div className="grid lg:grid-cols-2 gap-12 items-center">

          {/* LEFT: Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-4xl md:text-5xl font-extrabold text-gray-800 leading-tight">
                A healthier, smarter kitchen — made just for you.
              </h2>
              <p className="text-lg text-gray-700 leading-relaxed max-w-md">
                Simplify your meals with personalized planning, smart reminders,
                and nutrition tracking — so you can spend less time managing and
                more time enjoying.
              </p>
            </div>

            {/* Feature List */}
            <div className="grid sm:grid-cols-2 gap-5 pt-2">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 bg-white/70 backdrop-blur-sm p-3 rounded-xl shadow-sm hover:shadow-md transition"
                >
                  <div className="flex-shrink-0 w-10 h-10 bg-teal-700 rounded-full flex items-center justify-center text-white">
                    {feature.icon}
                  </div>
                  <p className="text-gray-800 text-sm font-medium leading-relaxed">
                    {feature.text}
                  </p>
                </div>
              ))}
            </div>

            {/* CTA Button */}
            <div className="pt-4">
              <button className="px-7 py-3 bg-emerald-700 text-white font-semibold rounded-full hover:bg-emerald-800 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center space-x-2">
                <span>Start Your Smart Meal Journey</span>
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* RIGHT: Photo Collage */}
          <div className="relative h-[480px] w-full flex justify-center">
            {/* Central image */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-80 rounded-3xl overflow-hidden shadow-2xl z-20 border-4 border-white">
              <img
                src="https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&h=800&fit=crop"
                alt="Person cooking"
                className="w-full h-full object-cover"
              />
            </div>

            {/* Top left */}
            <div className="absolute top-6 left-4 w-40 h-32 rounded-2xl overflow-hidden shadow-lg z-10 border-4 border-white">
              <img
                src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=400&fit=crop"
                alt="Delicious meal"
                className="w-full h-full object-cover"
              />
            </div>

            {/* Bottom left */}
            <div className="absolute bottom-8 left-8 w-44 h-36 rounded-2xl overflow-hidden shadow-lg z-10 border-4 border-white">
              <img
                src="https://images.unsplash.com/photo-1600891964092-4316c288032e?w=500&h=400&fit=crop"
                alt="Grilled steak"
                className="w-full h-full object-cover"
              />
            </div>

            {/* Bottom right */}
            <div className="absolute bottom-4 right-8 w-48 h-40 rounded-2xl overflow-hidden shadow-lg z-10 border-4 border-white">
              <img
                src="https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500&h=400&fit=crop"
                alt="Healthy meal"
                className="w-full h-full object-cover"
              />
            </div>

            {/* Top right tag */}
            <div className="absolute top-8 right-4 bg-emerald-700 text-white rounded-full shadow-lg px-5 py-2.5 z-30 flex items-center space-x-2">
              <span className="text-2xl">🥗</span>
              <span className="text-sm font-semibold">Vegan Party</span>
            </div>
          </div>
        </div>
      </div>

      {/* Decorative soft glow bottom fade */}
      <div className="absolute bottom-0 w-full h-20 bg-gradient-to-t from-emerald-300/70 to-transparent blur-md"></div>
    </section>
  );
};

export default LifestyleSection;
