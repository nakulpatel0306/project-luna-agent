import { useState } from "react";

export function Spotlight() {
  const [input, setInput] = useState("");
  const [isVisible, setIsVisible] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("command:", input);
    // TODO: send to backend
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-slate-900/95 backdrop-blur-sm flex items-start justify-center pt-32">
      <div className="w-full max-w-2xl px-4">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="what would you like to do?"
            className="w-full px-6 py-4 text-xl bg-slate-800 text-slate-100 rounded-xl border border-slate-700 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 placeholder:text-slate-500 shadow-2xl"
            autoFocus
          />
        </form>
        
        {input && (
          <div className="mt-4 p-4 bg-slate-800 rounded-xl border border-slate-700">
            <p className="text-sm text-slate-400">you typed: {input}</p>
            <p className="text-xs text-slate-500 mt-2">press enter to execute (not implemented yet)</p>
          </div>
        )}
      </div>
    </div>
  );
}