import React, { useRef, useState, useEffect } from "react";
import { transcribeAudio } from "../lib/utils/audio";
import { ChatForm } from "../components/ui/ChatForm";
import { MessageInput } from "../components/ui/MessageInput";
import { MessageList } from "../components/ui/MessageList";
import { PromptSuggestions } from "../components/ui/PromptSuggestions";

export default function Chatbot() {
  const [value, setValue] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [messages, setMessages] = useState([]);
  const timeout = useRef(null);
  const messageListRef = useRef(null);

  const cancelTimeout = () => {
    if (timeout.current) {
      clearTimeout(timeout.current);
    }
  };

  const setNewTimeout = (callback, ms) => {
    cancelTimeout();
    const id = setTimeout(callback, ms);
    timeout.current = id;
  };

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTo({
        top: messageListRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isGenerating]);

  // Session Management
  const getSessionId = () => {
    let id = localStorage.getItem("chat_session_id");
    if (!id) {
      id = "guest_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
      localStorage.setItem("chat_session_id", id);
    }
    return id;
  };

  const sendMessageToAgent = async (userText) => {
    setIsGenerating(true);
    try {
      const baseUrl = import.meta.env.VITE_BACKEND_URL || "";
      const response = await fetch(`${baseUrl}/api/chats`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText, thread_id: getSessionId() }),
        credentials: "include"
      });
      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error("Error calling API:", error);
      return "Sorry, something went wrong.";
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!value.trim()) return;

    const userMessage = { id: Date.now().toString(), role: "user", content: value };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setValue("");

    const reply = await sendMessageToAgent(value);
    const botMessage = { id: (Date.now() + 1).toString(), role: "assistant", content: reply };
    setMessages((prev) => [...prev, botMessage]);
  };

  const appendPrompt = async (message) => {
    const updatedMessages = [...messages, message];
    setMessages(updatedMessages);

    const reply = await sendMessageToAgent(message.content);
    const botMessage = { id: (Date.now() + 1).toString(), role: "assistant", content: reply };
    setMessages((prev) => [...prev, botMessage]);
  };

  const suggestions = [
    "Suggest me a vegetarian dinner.",
    "How to make pancakes quickly?",
    "Share a healthy smoothie recipe."
  ];

  return (
    <div
      className="flex flex-col justify-center items-center min-h-screen text-white p-4"
      style={{
        backgroundImage: "url('/image.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="w-full max-w-3xl mx-auto flex flex-col h-full">
        <PromptSuggestions
          label="Try these prompts"
          append={appendPrompt}
          suggestions={suggestions}
        />
        <div
          ref={messageListRef}
          className="flex-1 overflow-y-auto mb-4"
          style={{ maxHeight: "70vh" }}
        >
          <MessageList messages={messages} isTyping={isGenerating} />
        </div>
        <ChatForm className="w-full" isPending={false} handleSubmit={handleSubmit}>
          {({ files, setFiles }) => (
            <MessageInput
              value={value}
              onChange={(event) => setValue(event.target.value)}
              allowAttachments
              files={files}
              setFiles={setFiles}
              stop={() => {
                setIsGenerating(false);
                cancelTimeout();
              }}
              isGenerating={isGenerating}
              transcribeAudio={transcribeAudio}
            />
          )}
        </ChatForm>
      </div>
    </div>
  );
}
