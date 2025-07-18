import { useEffect, useState } from "react";
import TranscriptInput from "./components/TranscriptInput";
import TranscriptViewer from "./components/TranscriptViewer";
import EmbedButton from "./components/EmbedButton";
import { initializeSession } from "./api/axiosInstance";
import QuerySearch from "./components/QuerySearch";
import YouTube from "react-youtube";

function App() {
  const [url, setUrl] = useState("");
  const [chunks, setChunks] = useState([]);
  const [stored, setStored] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [videoId, setVideoId] = useState(null);
  const [player, setPlayer] = useState(null); // ✅ YouTube player instance

  useEffect(() => {
    const fetchSession = async () => {
      const session = await initializeSession();
      setSessionId(session);
    };
    fetchSession();
  }, []);

  const handleChunks = (chunkList) => {
    setChunks(chunkList);
    if (chunkList.length > 0) {
      setVideoId(chunkList[0].video_id);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">YouTube Transcript Analyzer</h1>

      <TranscriptInput
        url={url}
        setUrl={setUrl}
        setChunks={handleChunks}
        setStored={setStored}
      />

      <TranscriptViewer chunks={chunks} />

      {videoId && (
        <div className="my-6">
          <h3 className="font-semibold mb-2">▶️ Video Player</h3>
          <YouTube
            videoId={videoId}
            opts={{
              width: "100%",
              playerVars: { autoplay: 0 },
            }}
            onReady={(event) => {
              setPlayer(event.target); // ✅ Store player instance
            }}
          />
        </div>
      )}

      {chunks.length > 0 && !stored && (
        <EmbedButton chunks={chunks} setStored={setStored} />
      )}

      {stored && (
        <>
          <p className="text-green-600 font-semibold mt-4">
            Chunks embedded and stored successfully!
          </p>
          <div className="mt-6">
            <QuerySearch videoId={videoId} player={player} /> 
          </div>
        </>
      )}
    </div>
  );
}

export default App;
