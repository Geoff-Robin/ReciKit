// File: src/pages/LandingPage.jsx
import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import FOG from "vanta/dist/vanta.fog.min";
import ImageCarousel from "../components/ui/image-carousel";
import Navbar from "../components/ui/navbar";
import FeatureCard from "../components/ui/FeatureCard";
import LifestyleSection from "../components/ui/lifestyle";
import Footer from "../components/ui/footer";

const LandingPage = () => {
  const vantaRef = useRef(null);
  const vantaEffect = useRef(null);

  useEffect(() => {
    if (!vantaEffect.current) {
      vantaEffect.current = FOG({
        el: vantaRef.current,
        THREE: THREE,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200,
        minWidth: 200,
        highlightColor: 0xa8e6a3, // matcha cream green
        midtoneColor: 0x7fcf7a, // vibrant matcha midtone
        lowlightColor: 0x4da356, // deep leafy green
        baseColor: 0xdaf0d4, // pale green base
        blurFactor: 0.45,
        speed: 1.2,
        zoom: 1.25,
      });
    }
    return () => {
      if (vantaEffect.current) vantaEffect.current.destroy();
    };
  }, []);

  return (
    <div className="relative w-full min-h-screen overflow-x-hidden text-gray-800 m-0 p-0">
      {/* Vanta background */}
      <div ref={vantaRef} className="fixed inset-0 -z-10 w-screen h-screen" style={{ margin: 0, padding: 0 }} />

      {/* Soft gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-green-100/40 via-green-200/30 to-green-300/50 pointer-events-none -z-5" />

      {/* Navbar */}
      <div className="absolute top-0 left-0 w-full z-30">
        <Navbar />
      </div>

      {/* Hero Section */}
      <div className="relative z-20 flex flex-col items-center justify-center w-full min-h-screen px-4 sm:px-6 text-center space-y-10">
        <div className="max-w-4xl mt-28 sm:mt-36">
          <h1
            className="text-5xl md:text-6xl font-extrabold 
             bg-gradient-to-r from-white via-emerald-200 to-emerald-600 
             bg-clip-text text-transparent drop-shadow-[0_4px_10px_rgba(0,0,0,0.4)] mb-3"
          >
            Smart Cooking Made Simple
          </h1>
          <h2
            className="text-3xl md:text-4xl font-semibold text-white/90 
                       drop-shadow-[0_2px_4px_rgba(0,0,0,0.4)] mb-10"
          >
            Plan Better, Eat Smarter, and Waste Less
          </h2>
        </div>

        {/* Carousel */}
        <div className="w-full max-w-5xl mb-8 sm:mb-12 px-2">
          <ImageCarousel />
        </div>

        {/* Feature Cards */}
        <div className="w-full max-w-6xl px-2 sm:px-4 mb-24">
          <FeatureCard />
        </div>
      </div>

      {/* Lifestyle Section */}
      <div className="relative z-10 bg-gradient-to-b from-green-200/40 via-yellow-100/60 to-yellow-200/80 pt-10">
        <LifestyleSection />
      </div>

      {/* Footer Section */}
      <div className="relative z-10">
        <Footer />
      </div>

      {/* Bottom soft fade */}
      <div className="absolute bottom-0 w-full h-32 bg-gradient-to-t from-green-300/70 to-transparent blur-md z-10" />
    </div>
  );
};

export default LandingPage;