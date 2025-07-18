import { useState } from "react";
import axios from "../api/axiosInstance";
import ResultCard from "./ResultCard";

export default function QuerySearch({ videoId, player }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null); 

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const res = await axios.post("/search/search", {
        query,
        video_id: videoId,
      });

      setResults(res.data);
      console.log(res.data);
    } catch (err) {
      console.error("Search failed:", err);
    }
  };

  const seekTo = (seconds) => {
    if (player?.seekTo) {
      player.seekTo(seconds, true);
    } else {
      console.warn("YouTube player not ready.");
    }
  };

  return (
    <div className="mt-6 p-4 border rounded-md shadow bg-white">
      <h2 className="text-xl font-semibold mb-4">Search in Transcript</h2>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          placeholder="Type your search..."
          onChange={(e) => setQuery(e.target.value)}
          className="border px-4 py-2 rounded w-full shadow-sm"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Search
        </button>
      </div>

          {results && (
            <ResultCard
              result={results}
              query={query}
              onSeek={seekTo}
            />
          )}
    </div>
  );
}
