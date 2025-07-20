import { formatTimestamp } from "../utils/transcriptUtils";

export default function TimestampLink({ seconds, onSeek }) {
  return (
    <button
      onClick={() => onSeek(seconds)}
      className="text-purple-300 hover:text-purple-100 underline decoration-dotted cursor-pointer mx-1"
    >
      {formatTimestamp(seconds)}
    </button>
  );
}
