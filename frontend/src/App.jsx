import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from '@/pages/landingpage'
import Login from '@/pages/login'
import SignUp from '@/pages/signup.jsx'
import MealPlanApp from "./pages/MealPlan";
import Chatbot from "./pages/Chatbot";   // now correct

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <LandingPage /> } />
        <Route path="/login" element={ <Login />} />
        <Route path="/signup" element={ <SignUp />} />
        <Route path="/home" element={<MealPlanApp />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
