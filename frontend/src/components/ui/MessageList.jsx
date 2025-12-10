import React, { useEffect, useRef } from "react";
import { TypingIndicator } from "./TypingIndicator";

export function MessageList({ messages, isTyping }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex flex-col space-y-3 p-4 bg-transparent min-h-[300px] overflow-y-auto h-full">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`max-w-[75%] px-4 py-2 rounded-xl shadow-md whitespace-pre-wrap ${
            msg.role === "user"
              ? "self-end bg-black text-white"
              : "self-start bg-gray-700 text-white"
          }`}
        >
          {msg.content}
        </div>
      ))}

      {isTyping && <TypingIndicator />}

      {/* Invisible element to ensure auto-scroll */}
      <div ref={bottomRef}></div>
    </div>
  );
}
