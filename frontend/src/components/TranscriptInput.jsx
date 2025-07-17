import axios from "../api/axiosInstance";

export default function TranscriptInput({ url, setUrl, setChunks, setStored }) {
  const handleFetchTranscript = async () => {
    setStored(false);
    try {
      const res = await axios.post("/fetch", { url });
      setChunks(res.data);
    } catch (err) {
      alert("Failed to fetch transcript");
      console.error(err);
    }
  };

  return (
    <div className="mb-4">
      <input
        type="text"
        placeholder="Paste YouTube video URL..."
        className="border p-2 w-full rounded mb-2"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={handleFetchTranscript} className="bg-blue-600 text-white px-4 py-2 rounded">
        Fetch Transcript
      </button>
    </div>
  );
}
