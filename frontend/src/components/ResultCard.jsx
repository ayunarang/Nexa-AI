import { formatTimestamp } from "../utils/transcriptUtils";
import TimestampLink from "./TimestampLink";
import ConfidenceBadge from "./ConfidenceBadge";

export default function ResultCard({ result, onSeek }) {
  return (
    <div className="space-y-6 fade-up">
      <div className="bg-[#151526] border border-[#292946] p-5 rounded-xl shadow-lg">
        <p className="text-sm font-semibold text-purple-300 mb-2">Answer:</p>
        <p className="text-lg text-gray-100 font-medium italic leading-relaxed break-words">
          <AnswerText text={result.answer} onSeek={onSeek} />
        </p>

        <div className="mt-4 flex items-center gap-2 text-sm text-gray-400">
          <span>Confidence:</span>
          <ConfidenceBadge level={result.confidence} />
        </div>
      </div>

      <div
        className={`grid gap-4 ${result.timestamps?.length > 1 ? "sm:grid-cols-2" : "grid-cols-1"
          }`}   >
        {result.timestamps?.map((timestamp, idx) => (
          <div
            key={idx}
            className="bg-[#1e1e2f] border border-[#2d2d46] p-4 rounded-xl shadow-md hover:shadow-lg transition duration-200"
          >
            <button
              onClick={() => onSeek(timestamp.start)}
              className="text-sm font-semibold text-purple-300 hover:text-purple-100 mb-2 block"
            >
              <span className="underline decoration-dotted text-2xl cursor-pointer">
                {formatTimestamp(timestamp.start)}
              </span>
            </button>

            <p className="text-base text-gray-300 italic leading-snug line-clamp-4">
              “{timestamp.transcript}”
            </p>
          </div>
        ))}
      </div>
    </div >
  );
}

function AnswerText({ text, onSeek }) {
  const timestampRegex = /(\d+(\.\d+)?)s/g;
  const parts = [];
  let lastIndex = 0;

  text.replace(timestampRegex, (match, value, _, index) => {
    const seconds = parseFloat(value);

    if (lastIndex < index) {
      parts.push(text.slice(lastIndex, index));
    }

    parts.push(
      <TimestampLink key={index} seconds={seconds} onSeek={onSeek} />
    );

    lastIndex = index + match.length;
  });

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return parts;
}
