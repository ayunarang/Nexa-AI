import axios from "axios";

export default function EmbedButton({ chunks, setStored }) {
  const handleStoreEmbeddings = async () => {
    try {
      const res = await axios.post("http://localhost:8000/api/transcript/embed-store", { chunks });
      if (res.data.status === "success") {
        setStored(true);
        alert(`Stored ${res.data.stored} chunks.`);
      }
    } catch (err) {
      alert("Failed to store embeddings.");
      console.error(err);
    }
  };

  return (
    <button onClick={handleStoreEmbeddings} className="bg-green-600 text-white px-4 py-2 rounded">
      Save Embeddings to FAISS
    </button>
  );
}
