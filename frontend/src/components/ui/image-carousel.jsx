import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";

const ImageCarousel = () => {
  const [isHovered, setIsHovered] = useState(false);
  const controls = useAnimation();
  const containerRef = useRef(null);

  const foodImages = [
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1559847844-5315695dadae?w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&h=400&fit=crop",
  ];

  const images = [...foodImages, ...foodImages, ...foodImages];

  useEffect(() => {
    let animationFrame;
    let xPosition = 0;

    const animate = () => {
      if (!isHovered) {
        xPosition -= 1; // slightly slower for smoothness
        if (containerRef.current) {
          const scrollWidth = containerRef.current.scrollWidth / 3;
          if (Math.abs(xPosition) >= scrollWidth) xPosition = 0;
          containerRef.current.style.transform = `translateX(${xPosition}px)`;
        }
      }
      animationFrame = requestAnimationFrame(animate);
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [isHovered]);

  return (
    <div
      className="relative overflow-hidden w-full select-none
                 bg-gradient-to-r from-green-200 via-emerald-100 to-lime-200 py-6"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <motion.div
        ref={containerRef}
        className="flex space-x-4 will-change-transform"
        animate={controls}
      >
        {images.map((img, index) => (
          <div
            key={index}
            className="flex-shrink-0 w-[14rem] h-40 md:w-[16rem] md:h-44
                       rounded-xl overflow-hidden shadow-md 
                       hover:shadow-xl transition-all duration-300 bg-white"
          >
            <motion.img
              src={img}
              alt={`Food dish ${index + 1}`}
              className="w-full h-full object-cover"
              whileHover={{ scale: 1.1 }}
              transition={{ duration: 0.4 }}
            />
          </div>
        ))}
      </motion.div>

      {/* Edge fade for better look */}
      <div className="absolute left-0 top-0 w-24 h-full 
                      bg-gradient-to-r from-green-200 to-transparent pointer-events-none" />
      <div className="absolute right-0 top-0 w-24 h-full 
                      bg-gradient-to-l from-green-200 to-transparent pointer-events-none" />
    </div>
  );
};

export default ImageCarousel;
