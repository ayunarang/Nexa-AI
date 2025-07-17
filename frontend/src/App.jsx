import { useEffect, useState } from "react";
import TranscriptInput from "./components/TranscriptInput";
import TranscriptViewer from "./components/TranscriptViewer";
import EmbedButton from "./components/EmbedButton";
import { initializeSession } from "./api/axiosInstance";

function App() {
  const [url, setUrl] = useState("");
  const [chunks, setChunks] = useState([]);
  const [stored, setStored] = useState(false);

  useEffect(() => {
    initializeSession();
  }, []);

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">YouTube Transcript Analyzer</h1>
      <TranscriptInput url={url} setUrl={setUrl} setChunks={setChunks} setStored={setStored} />
      <TranscriptViewer chunks={chunks} />
      {chunks.length > 0 && (
        <EmbedButton chunks={chunks} setStored={setStored} />
      )}
      {stored && (
        <p className="text-green-600 font-semibold mt-4">
          Chunks embedded and stored successfully!
        </p>
      )}
    </div>
  );
}

export default App;
