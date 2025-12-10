import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MealPlanApp from "./pages/MealPlan";
import Chatbot from "./pages/Chatbot";   // now correct

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MealPlanApp />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
