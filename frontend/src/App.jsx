import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from '@/pages/landingpage'
import Login from '@/pages/login'
import SignUp from '@/pages/signup.jsx'
import MealPlanApp from "@/pages/MealPlan";
import Chatbot from "@/pages/chatbot";
import ChatWidget from "@/pages/ChatWidget";
import Inventory from "@/pages/inventory.jsx";
import { MessageSquare } from "lucide-react";

function App() {
  const [isChatOpen, setIsChatOpen] = React.useState(false);

  return (
    <BrowserRouter>
      <div className="relative min-h-screen">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/home" element={<MealPlanApp />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/inventory" element={<Inventory />} />
        </Routes>

        {/* Floating Action Button */}
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-emerald-600 text-white rounded-full shadow-lg hover:bg-emerald-700 transition-colors z-40"
        >
          <MessageSquare className="w-6 h-6" />
        </button>

        {/* Global Chat Widget */}
        <ChatWidget isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      </div>
    </BrowserRouter>
  );
}

export default App;