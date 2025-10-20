import React from "react";
import { Paperclip, Mic } from "lucide-react";

export function MessageInput({
  value,
  onChange,
  allowAttachments,
  files,
  setFiles,
  isGenerating,
  stop,
  transcribeAudio,
}) {
  return (
    <div className="flex items-center w-full bg-transparent">
      <input
        type="text"
        className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none px-3 text-sm"
        placeholder="Ask AI..."
        value={value}
        onChange={onChange}
        disabled={isGenerating}
      />

      {allowAttachments && (
        <button
          type="button"
          className="p-2 hover:bg-[#2a2a2a] rounded-full transition"
          onClick={() => {
            document.getElementById("fileInput").click();
          }}
        >
          <Paperclip size={18} />
        </button>
      )}

      <input
        id="fileInput"
        type="file"
        multiple
        className="hidden"
        onChange={(e) => setFiles(Array.from(e.target.files))}
      />

      <button
        type="button"
        className="p-2 hover:bg-[#2a2a2a] rounded-full transition"
      >
        <Mic size={18} />
      </button>

      {isGenerating && (
        <button
          type="button"
          onClick={stop}
          className="text-xs text-red-400 ml-2"
        >
          Stop
        </button>
      )}
    </div>
  );
}
