import axios from "axios";
import { useState } from "react";

export default function TranscriptInput({
  url,
  setUrl,
  setSuccess,
  setVideoId,
  setLoading,
  loading,
  success
}) {
  const [error, setError] = useState("");

  const handleFetchTranscript = async () => {
    if (loading) return;

    setLoading(true);
    setError("");

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/transcript/fetch`, { url });
      const sessionId = res.data.session_id;
      sessionStorage.setItem("yt_session_id", sessionId);

      setSuccess(res.data.status);
      setVideoId(res.data.video_id);
    } catch (err) {
      console.error(err);
      if (err.response?.status === 400 && err.response?.data?.detail === "The video is not in English.") {
        setError("This video is not in English. Right now Nexa AI only supports videos with english audio.");
      }
      else if (err.response?.status === 400 && err.response?.data?.detail === "The video does not have subtitles.") {
        setError("This video does not have subtitles. Nexa AI uses subtitles to analyze video content.");
      }
      else {
        setError("URL invalid or server error. Please check the URL or try again.");
      }
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
          disabled={loading}
        />
        <button
          onClick={handleFetchTranscript}
          disabled={loading}
          className={`${loading ? "bg-purple-400 cursor-not-allowed" : "bg-purple-600 hover:bg-purple-700"
            } text-white font-semibold py-2 md:py-3 text-sm md:px-5 px-3 rounded-lg transition whitespace-nowrap`}
          aria-label="Fetch transcript for video URL"
        >
          {loading ? "Loading..." : "Try URL"}
        </button>
      </div>

      {!success && !loading &&
        <p className={`mt-2 text-sm text-red-400 ${error ? "visible" : "invisible"}`} role="alert">
          {error || "placeholder text"}
        </p>
      }


    </div>
  );
}
