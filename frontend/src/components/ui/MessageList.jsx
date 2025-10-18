import React from "react";
import { TypingIndicator } from "./TypingIndicator";

export function MessageList({ messages, isTyping }) {
  return (
    <div className="flex flex-col space-y-3 p-4 bg-transparent min-h-[300px]">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`max-w-xs px-4 py-2 rounded-lg shadow ${
            msg.role === "user"
              ? "self-end bg-black text-white"
              : "self-start bg-gray-700 text-white"
          }`}
        >
          {msg.content}
        </div>
      ))}
      {isTyping && <TypingIndicator />}
    </div>
  );
}

