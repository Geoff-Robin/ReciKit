import React, { useState } from "react";

export function ChatForm({ children, className, handleSubmit, isPending }) {
  const [files, setFiles] = useState([]);

  return (
    <form
      onSubmit={handleSubmit}
      className={`${className} flex items-center bg-[#1a1a1a] rounded-2xl p-3 shadow-lg`}
    >
      {children({ files, setFiles })}
      <button
        type="submit"
        disabled={isPending}
        className="p-2 bg-[#3a3a3a] hover:bg-[#4a4a4a] rounded-full transition ml-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-4 h-4 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </button>
    </form>
  );
}
