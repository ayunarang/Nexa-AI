import axios from "../api/axiosInstance";
import { useState } from "react";

export default function TranscriptInput({ url, setUrl, setSuccess, setVideoId, setLoading }) {
  const [error, setError] = useState("");

  const handleFetchTranscript = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("/transcript/fetch", { url });
      setSuccess(res.data.status);
      setVideoId(res.data.video_id);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch transcript. Please check the URL.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <label htmlFor="video-url" className="sr-only">
        YouTube Video URL
      </label>
      <div className="flex w-full gap-4 items-center">
        <input
          id="video-url"
          type="text"
          placeholder="Paste YouTube video URL..."
          className="w-full px-4 py-3 rounded-lg bg-[#1e1b2e] text-white border border-purple-500 placeholder-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          aria-label="YouTube Video URL"
        />
        <button
          onClick={handleFetchTranscript}
          className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 md:py-3 text-sm md:px-5 px-3 rounded-lg transition whitespace-nowrap"
          aria-label="Fetch transcript for video URL"
          onKeyDown={(e) => {
            if (e.key === "Enter") handleFetchTranscript();
          }}
        >
          Try URL
        </button>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-400" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
