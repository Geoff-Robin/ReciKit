import React from "react";
import { Link } from "react-router-dom";
import logo from "@/assets/logo.svg"

const Navbar = () => {
  return (
    <header className="bg-gradient-to-r from-green-700/90 via-emerald-600/80 to-green-500/90 backdrop-blur-lg shadow-lg fixed top-0 left-0 w-full z-50 border-b border-green-400/40">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-10">
        <div className="flex justify-between items-center h-16">
          {/* Logo Section */}
          <div className="flex items-center space-x-3">
            <div className="w-14 h-14 sm:w-16 sm:h-16 bg-white flex items-center justify-center shadow-md">
              <img
                src={logo}
                alt="ReciKit Logo"
                className="w-10 h-10 sm:w-12 sm:h-12"
              />
            </div>
            <span className="text-2xl sm:text-3xl font-bold text-white drop-shadow-md tracking-wide">
              ReciKit
            </span>
          </div>
          {/* Action Buttons */}
          <div className="flex items-center space-x-4">
            <Link to="/login">
              <button className="px-5 py-2 text-white border-2 border-white rounded-full font-medium hover:bg-white hover:text-green-700 transition duration-300 shadow-md">
                Login
              </button>
            </Link>
            <Link to="/signup">
              <button className="px-5 py-2 bg-white text-green-700 rounded-full font-semibold hover:bg-green-100 transition duration-300 shadow-md">
                Sign Up
              </button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
