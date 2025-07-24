import { useEffect, useState, useCallback } from "react";
import axios from "../api/axiosInstance";
import { toast } from "sonner";

export default function TimestampDisplay({ videoId, activeAction }) {
  const [segments, setSegments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60).toString().padStart(2, "0");
    const secs = Math.floor(seconds % 60).toString().padStart(2, "0");
    return `${mins}:${secs}`;
  };

  const mergeSegments = (raw) => {
    const merged = [];
    for (let seg of raw) {
      const last = merged[merged.length - 1];
      if (last && last.label === seg.label) {
        last.end = seg.end;
      } else {
        merged.push({ ...seg });
      }
    }
    return merged;
  };

  const fetchTimestamps = useCallback(async () => {
    if (activeAction !== "timestamps" || !videoId) return;

    setLoading(true);
    try {
      const { data } = await axios.post("/timestamps/create", { videoId });
      const rawSegments = data?.segments || [];

      const mergedSegments = mergeSegments(rawSegments);
      setSegments(mergedSegments);
      toast.success("Timestamps Generated! You can copy them.")
    } catch (err) {
      toast.error("Failed to fetch. Please try again.");
      setSegments([]);
    } finally {
      setLoading(false);
    }
  }, [videoId, activeAction]);

  useEffect(() => {
    fetchTimestamps();
  }, [fetchTimestamps]);

  const handleCopy = () => {
    const text = segments
      .map((seg) => `[${formatTime(seg.start)} - ${formatTime(seg.end)}] ${seg.label}`)
      .join("\n");

    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="mt-10 max-w-xl mx-auto fade-up">
      {loading ? (
        <div className="h-56 rounded-xl bg-[#1e1b2e] animate-pulse border border-[#292946] shadow-md" />
      ) : segments.length === 0 ? (
        <div className="p-6 rounded-xl bg-[#1e1b2e] border border-[#292946] shadow-lg text-center text-gray-300">
          No timestamps found. Try again or check the video ID.
        </div>
      ) : (
        <div className="p-6 rounded-xl bg-[#1e1b2e] border border-[#292946] shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-white text-xl font-bold">Timestamps</h2>
            <button
              onClick={handleCopy}
              className="text-sm bg-purple-600 hover:bg-purple-700 text-white px-4 py-1.5 rounded-lg transition"
            >
              {copied ? "Copied!" : "Copy All"}
            </button>
          </div>
          <div className="flex flex-col gap-2">
            {segments.map((seg, index) => (
              <div
                key={index}
                className="flex justify-between items-center bg-[#2a2a40] px-4 py-2 rounded-lg gap-2"
              >
                <div className="text-purple-300 font-mono text-sm justify-start flex flex-col sm:flex-row items-center">
                  <span>[{formatTime(seg.start)} -</span>
                  <span>{formatTime(seg.end)}]</span>
                </div>
                <div className="text-white font-semibold text-sm justify-end text-right">
                  {seg.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
