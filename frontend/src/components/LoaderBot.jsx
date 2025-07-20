import { Bot } from "lucide-react";

export default function LoaderBot({ message = "Loading" }) {
  return (
    <div className="flex items-start gap-4 mt-10">
      <div className="w-12 h-10 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center shadow-md">
        <span className="text-xl font-bold text-white">
          <Bot />
        </span>
      </div>
      <div className="bg-[#1e1b2e] border border-[#292946] rounded-2xl px-4 py-3 shadow-lg w-full">
        <p className="text-purple-300 text-[16px] font-medium flex items-center gap-2 overflow-visible">
          {message}
          <span className="ml-1 flex items-end gap-2 h-1">
            <span className="w-2 h-2 bg-purple-400 rounded-full jump" style={{ animationDelay: "0s" }} />
            <span className="w-2 h-2 bg-purple-400 rounded-full jump" style={{ animationDelay: "0.1s" }} />
            <span className="w-2 h-2 bg-purple-400 rounded-full jump" style={{ animationDelay: "0.2s" }} />
            <span className="w-2 h-2 bg-purple-400 rounded-full jump" style={{ animationDelay: "0.3s" }} />
          </span>
        </p>
      </div>
    </div>
  );
}
