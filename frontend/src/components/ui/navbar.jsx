import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <header className="bg-gradient-to-r from-green-700/90 via-emerald-600/80 to-green-500/90 backdrop-blur-lg shadow-lg fixed top-0 left-0 w-full z-50 border-b border-green-400/40">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-10">
        <div className="flex justify-between items-center h-16">
          {/* Logo Section */}
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-white/90 rounded-full flex items-center justify-center shadow-md border border-green-300">
              <svg
                className="w-6 h-6 text-green-700"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
            </div>
            <span className="text-2xl font-bold text-white drop-shadow-md tracking-wide">
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
