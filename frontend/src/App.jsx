import { useEffect, useRef, useState } from "react";
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
  const [videoId, setVideoId] = useState(null);
  const [player, setPlayer] = useState(null);
  const [activeAction, setActiveAction] = useState("");
  const [loading, setLoading] = useState(false);
  const timestampRef = useRef(null);
  const queryRef = useRef(null);


  useEffect(() => {
    initializeSession();
  }, []);

  const handleTimestampsClick = () => {
    setActiveAction("timestamps");
    setTimeout(() => {
      timestampRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 250);
  };

  const handleAskClick = () => {
    setActiveAction("ask");
    setTimeout(() => {
      queryRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 250);
  };


  return (
    <div className="relative overflow-hidden min-h-screen bg-[#0b0b15]">
      <nav className="w-full backdrop-blur-md px-4 md:px-8 py-3 border-b border-[#1e1e2e]/60 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-xl md:text-2xl font-semibold tracking-wide select-none">
            <span className="relative inline-block italic font-bold pr-1 bg-gradient-to-r from-purple-200 to-purple-600 bg-clip-text text-transparent 
        drop-shadow-[0_0_8px_rgba(168,85,247,0.6)] 
        animate-pulse">
              Nexa AI
            </span>
          </h1>
        </div>
      </nav>

      <div className="absolute top-0 right-0 z-0 pointer-events-none">
        <div className="w-[400px] h-[400px] md:w-[700px] md:h-[700px] bg-purple-400 opacity-15 blur-[120px] rounded-full translate-x-1/3 -translate-y-1/3" />
      </div>


      <main className="relative z-10 min-h-screen text-white px-4 md:px-8 pt-8 pb-20 font-sans">
        <section className="max-w-7xl mx-auto mb-16 text-center ">
          <h1 className="text-xl md:text-4xl font-extrabold leading-tight mb-4">
            AI-Powered YouTube Timestamps & Content Finder
            <br />
            <span className="text-purple-400">Just paste a link! We do the rest.</span>
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
                setActiveAction={setActiveAction}
                activeAction={activeAction}
              />

              <div className="relative min-h-[150px]">
                {!videoId && !loading && (
                  <div className="md:text-base text-sm text-gray-400 md:space-y-0.5 space-y-2 leading-relaxed">
                    <p className="text-white font-semibold md:text-lg text-base">
                      How Nexa AI Works
                    </p>
                    <p>
                      <em className="font-medium">1.</em> Paste a YouTube link above. Our AI will process the video.
                    </p>
                    <p>
                      <em className="font-medium">2.</em> Once loaded, you can generate smart & specific timestamps labeled like
                      <em className="text-white font-medium"> Intro</em>,
                      <em className="text-white font-medium"> Dinner Plans</em>, and
                      <em className="text-white font-medium"> Self Reflection</em>, helping you navigate the content faster.
                    </p>
                    <p>
                      <em className="font-medium">3.</em> Looking for something specific? Just type your question. The AI will find the exact or related moments in the video, with clickable timestamps that take you right there.                    
                      </p>
                  </div>
                )}

                {loading && <LoaderBot message="Analyzing your video, please wait" />}

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
                            onClick={handleAskClick}
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
            ref={queryRef}
            role="region"
            aria-label="Query Search"
            className="max-w-5xl mx-auto mt-12 bg-[#151526] md:p-6 p-4 rounded-2xl shadow-lg border border-[#292946]"
          >
            <QuerySearch videoId={videoId} player={player} />
          </section>
        )}

        {activeAction === "timestamps" && (
          <section
            ref={timestampRef}
            role="region"
            aria-label="Timestamp Display"
            className="max-w-5xl mx-auto mt-12"
          >
            <TimestampDisplay videoId={videoId} activeAction={activeAction} />
          </section>
        )}
      </main>
    </div>
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
