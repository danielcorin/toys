"use client";

import { useChat } from "ai/react";

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: "http://127.0.0.1:8000/ask"
  });

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div>
        {messages.map((m) => (
          <div key={m.id}>
            {m.role === "user" ? "User: " : "AI: "}
            {m.content}
          </div>
        ))}

        <form onSubmit={handleSubmit}>
          <label>
            Say something...
            <input value={input} onChange={handleInputChange} />
          </label>
          <button type="submit">Send</button>
        </form>
      </div>
    </main>
  );
}
