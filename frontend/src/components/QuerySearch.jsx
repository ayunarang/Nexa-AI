import { useState } from "react";
import axios from "../api/axiosInstance";
import ResultCard from "./ResultCard";

function SearchForm({ query, setQuery, isSearching, onSearch }) {
  return (
    <div className="flex flex-col sm:flex-row gap-3 mb-6">
      <input
        type="text"
        aria-label="Search video content"
        value={query}
        placeholder="Ask a question or search phrase..."
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSearch()}
        className="flex-1 px-4 py-2 rounded-lg bg-[#1e1b2e] text-white border border-purple-400 placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
      />
      <button
        onClick={onSearch}
        disabled={isSearching || !query.trim()}
        aria-disabled={isSearching || !query.trim()}
        className={`px-5 py-2 rounded-lg transition cursor-pointer font-medium whitespace-nowrap ${
          isSearching || !query.trim()
            ? "bg-purple-500/40 text-purple-200 cursor-not-allowed"
            : "bg-purple-600 hover:bg-purple-700 text-white"
        }`}
      >
        {isSearching ? "Searching..." : "Search"}
      </button>
    </div>
  );
}

export default function QuerySearch({ videoId, player }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim() || !videoId) return;
    setIsSearching(true);
    setError(null);
    setHasSearched(true);

    try {
      const res = await axios.post("/search/search", {
        query,
        video_id: videoId,
      });
      setResults(res.data);
    } catch (err) {
      console.error("Search failed:", err);
      setError("Something went wrong. Please try again.");
      setResults(null);
    } finally {
      setIsSearching(false);
    }
  };

  const seekTo = (seconds) => {
    if (player?.seekTo) player.seekTo(seconds, true);
  };

  return (
    <section className="w-full max-w-3xl mx-auto">
      <h2 className="md:text-2xl text-lg font-semibold mb-4 text-white">
        Type What You Would Like to See
      </h2>

      <SearchForm
        query={query}
        setQuery={setQuery}
        isSearching={isSearching}
        onSearch={handleSearch}
      />

      {!hasSearched && !isSearching && (
        <p className="text-sm text-gray-500 mb-4">
          Type a question - “Did they mention...” or “What was the part
          about...” and hit Search.
        </p>
      )}

      {isSearching && <ShimmerResultList />}

      {!isSearching && error && (
        <div className="text-red-300 text-sm mt-2" role="alert">
          {error}
        </div>
      )}

      {!isSearching && !error && results && (
        <ResultCard result={results} query={query} onSeek={seekTo} />
      )}

      {!isSearching && hasSearched && !error && !results && (
        <p className="text-sm text-purple-300/70 mt-2">
          No matches found for{" "}
          <span className="text-purple-200 font-medium">“{query}”</span>.
        </p>
      )}
    </section>
  );
}


function ShimmerBar({ w = "w-full" }) {
  return (
    <div
      className={`h-4 ${w} rounded bg-gradient-to-r from-[#242437] via-[#2d2d44] to-[#242437] 
      animate-pulse bg-[length:200%_100%]`}
    />
  );
}

function ShimmerResultCard() {
  return (
    <div className="p-4 rounded-xl border border-[#292946] bg-[#1a1a2b] shadow-sm flex flex-col gap-3 animate-pulse">
      <div className="flex justify-between gap-4">
        <ShimmerBar w="w-1/3" />
        <div className="h-6 w-12 rounded-md bg-[#26263a]" />
      </div>
      <ShimmerBar />
      <ShimmerBar w="w-5/6" />
      <ShimmerBar w="w-2/3" />
    </div>
  );
}

function ShimmerResultList() {
  return (
    <div className="flex flex-col gap-4">
      <ShimmerResultCard />
      <ShimmerResultCard />
    </div>
  );
}
