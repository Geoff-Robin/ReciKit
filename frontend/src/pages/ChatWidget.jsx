import React, { useState, useRef, useEffect } from "react";
import { X } from "lucide-react";
import { Link } from "react-router-dom";

export default function ChatWidget({ isOpen, onClose }) {
  const [value, setValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const messagesEndRef = useRef(null);

  // Always run hooks, only render JSX if isOpen
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isGenerating]);

  const sendMessageToAgent = async (updatedMessages) => {
    setIsGenerating(true);
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: updatedMessages }),
      });

      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error(error);
      return "Sorry, something went wrong.";
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!value.trim()) return;

    const userMessage = { id: Date.now().toString(), role: "user", content: value };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setValue("");

    const reply = await sendMessageToAgent(updatedMessages);

    setMessages((prev) => [
      ...prev,
      { id: (Date.now() + 1).toString(), role: "assistant", content: reply },
    ]);
  };

  // Render JSX only if open
  if (!isOpen) return null;

  return (
    <div className="fixed bottom-20 right-6 w-80 h-96 bg-white rounded-xl shadow-2xl z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-emerald-600 text-white rounded-t-xl">
        <Link to="/chat" className="font-semibold hover:underline">Chat Assistant</Link>
        <button onClick={onClose}>
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-3 overflow-y-auto space-y-2 text-sm text-gray-800">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`max-w-[75%] px-3 py-2 rounded-lg ${
              msg.role === "user"
                ? "ml-auto bg-emerald-600 text-white"
                : "mr-auto bg-gray-200 text-gray-800"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {isGenerating && (
          <div className="mr-auto bg-gray-200 px-3 py-2 rounded-lg text-gray-600">
            Typing…
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-3 border-t">
        <input
          type="text"
          placeholder="Type a message..."
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
      </form>
    </div>
  );
}
