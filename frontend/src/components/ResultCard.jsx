import { formatTimestamp } from "../utils/transcriptUtils";

export default function ResultCard({ result, onSeek }) {
  return (
    <div className="space-y-4">
      <div className="bg-gray-100 p-4 rounded shadow-sm">
        <p className="font-medium">💬 Answer:</p>
        <p className="italic">{result.answer}</p>
        <p className="text-sm text-gray-600 mt-1">
          Confidence:{" "}
          <span
            className={`ml-1 text-xs font-medium px-2 py-1 rounded-full ${result.confidence === "high"
                ? "bg-green-100 text-green-800"
                : result.confidence === "medium"
                  ? "bg-yellow-100 text-yellow-800"
                  : "bg-red-100 text-red-800"
              }`}
          >
            {result.confidence.toUpperCase()}
          </span>
        </p>
      </div>

      {result.timestamps?.map((timestamp, idx) => (
        <div
          key={idx}
          className="p-3 bg-white border rounded hover:bg-blue-50 transition"
        >
          <button
            onClick={() => onSeek(timestamp.start)}
            className="text-blue-600 mt-1 text-xs underline hover:text-blue-800"
          >
            ⏱ Go to {formatTimestamp(timestamp.start)}
          </button>
          <p className="text-sm text-gray-600 italic line-clamp-2">
            "{timestamp.transcript}"
          </p>
        </div>
      ))}
    </div>
  );
}
