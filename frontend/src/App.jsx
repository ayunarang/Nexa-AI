import { useEffect, useState } from "react";
import TranscriptInput from "./components/TranscriptInput";
import QuerySearch from "./components/QuerySearch";
import TimestampDisplay from "./components/TimestampDisplay";
import VideoPlayer from "./components/VideoPlayer";
import LoaderBot from "./components/LoaderBot";
import ShimmerPlayerBox from "./components/ShimmerPlayerBox";
import { initializeSession } from "./api/axiosInstance";
import { Bot } from "lucide-react";

export default function App() {
  const [url, setUrl] = useState("");
  const [success, setSuccess] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [videoId, setVideoId] = useState(null);
  const [player, setPlayer] = useState(null);
  const [activeAction, setActiveAction] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    initializeSession().then(setSessionId);
  }, []);

  const handleTimestampsClick = () => {
    setActiveAction("timestamps");
  };

  return (
    <main className="min-h-screen bg-[#0b0b15] text-white px-4 md:px-8 py-20 font-sans">
      <section className="max-w-7xl mx-auto mb-16 text-center">
        <h1 className="text-xl md:text-4xl font-extrabold leading-tight mb-4">
          AI-Powered YouTube Timestamps & Content Finder
          <br />
          <span className="text-purple-400">Just paste a link — we do the rest.</span>
        </h1>
      </section>

      <section className="max-w-7xl mx-auto flex flex-col lg:flex-row gap-8 items-start justify-between">
        <div className="flex-1 w-full">
          <div className="bg-[#151526] md:p-6 p-4 rounded-2xl shadow-lg border border-[#292946] space-y-1 md:space-y-0">
            <TranscriptInput
              url={url}
              setUrl={setUrl}
              setSuccess={setSuccess}
              setVideoId={setVideoId}
              setLoading={setLoading}
              loading={loading}
              success={success}
            />

            <div className="relative min-h-[150px]">
              {!videoId && !loading && (
                <div className="text-base text-gray-400 space-y-3 leading-relaxed">
                  <p className="text-white font-semibold text-lg">
                    Uncover key moments in videos, instantly with AI.
                  </p>

                  <p>
                    Paste a YouTube link above. The AI will fetch the transcript and label segments like
                    <em className="text-white font-medium"> Intro</em>,
                    <em className="text-white font-medium"> Deep Dives</em>, and
                    <em className="text-white font-medium"> Key Moments</em>.
                  </p>
                  <p>
                    Have a question? Just type it — we’ll find the exact part of the video that answers it.
                  </p>
                  <p>
                    Click any timestamp to jump instantly. Fast. Smart. Effortless.
                  </p>
                </div>

              )}

              {loading && <LoaderBot message="Fetching video" />}

              {!loading && (success === "Success" || success === "Duplicate") && (
                <div className="mt-10">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-10 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center shadow-md">
                      <span className="text-xl font-bold"><Bot /></span>
                    </div>
                    <div className="bg-[#1e1b2e] border border-[#292946] rounded-2xl px-4 py-3 md:p-6 shadow-lg w-full">
                      <p className="text-purple-300 mb-4 md:mb-8 text-[16px] font-medium">
                        I’ve fetched the video details! What would you like to do next?
                      </p>
                      <div className="flex flex-col sm:flex-row gap-3">
                        <ActionButton
                          label="Auto Generate Timestamps"
                          active={activeAction === "timestamps"}
                          onClick={handleTimestampsClick}
                        />
                        <ActionButton
                          label="Ask Anything About This Video"
                          active={activeAction === "ask"}
                          onClick={() => setActiveAction("ask")}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="w-full max-w-lg mx-auto">
          {loading ? (
            <ShimmerPlayerBox />
          ) : (
            <VideoPlayer videoId={videoId} setPlayer={setPlayer} />
          )}
        </div>
      </section>

      {activeAction === "ask" && (
        <section
          role="region"
          aria-label="Query Search"
          className="max-w-5xl mx-auto mt-12 bg-[#151526] md:p-6 p-4 rounded-2xl shadow-lg border border-[#292946]"
        >
          <QuerySearch videoId={videoId} player={player} />
        </section>
      )}

      {activeAction === "timestamps" && (
        <section
          role="region"
          aria-label="Timestamp Display"
          className="max-w-5xl mx-auto mt-12"
        >
          <TimestampDisplay videoId={videoId} activeAction={activeAction} />
        </section>
      )}
    </main>
  );
}


function ActionButton({ label, onClick, active }) {
  return (
    <button
      onClick={onClick}
      className={`px-5 py-2 rounded-xl cursor-pointer border-2 transition-all duration-300 md:text-[16px] text-sm shadow-sm hover:shadow-md ${active
        ? "bg-purple-600 text-white border-purple-700"
        : "bg-[#151526] text-purple-300 border-purple-500 hover:bg-purple-700 hover:text-white"
        }`}
    >
      {label}
    </button>
  );
}
