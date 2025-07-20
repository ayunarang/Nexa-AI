export default function AISuggestion({ activeAction, setActiveAction }) {
  return (
    <div className="w-full mx-auto mt-6 transition-all duration-700 ease-in-out">
      <div className="flex items-start gap-4">
        {/* GPT Avatar */}
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center shadow-md">
          <span className="text-xl font-bold text-white">🤖</span>
        </div>

        {/* Message bubble */}
        <div className="bg-[#1e1b2e] border border-[#292946] rounded-2xl px-4 py-3 shadow-lg w-full">
          <p className="text-purple-300 mb-6 text-[16px]">
            I’ve fetched the video details! What would you like to do next?
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <ActionButton
              active={activeAction === "timestamps"}
              label="Auto Generate Timestamps"
              onClick={() => setActiveAction("timestamps")}
            />
            <ActionButton
              active={activeAction === "ask"}
              label="Ask Anything About This Video"
              onClick={() => setActiveAction("ask")}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function ActionButton({ active, label, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-5 py-2 rounded-xl cursor-pointer border-2 transition-all text-lg shadow-sm hover:shadow-md ${
        active
          ? "bg-purple-600 text-white border-purple-700"
          : "bg-[#151526] text-purple-300 border-purple-500 hover:bg-purple-700 hover:text-white"
      }`}
    >
      {label}
    </button>
  );
}
