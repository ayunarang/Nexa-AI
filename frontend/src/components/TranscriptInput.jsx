import { useState } from 'react';
import { fetchTranscript } from '../api/transcript';

export default function TranscriptInput() {
  const [url, setUrl] = useState('');
  const [chunks, setChunks] = useState([]);

  const handleSubmit = async () => {
    const result = await fetchTranscript(url);
    setChunks(result);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <input
        type="text"
        value={url}
        onChange={e => setUrl(e.target.value)}
        placeholder="Paste YouTube URL"
        className="border p-2 w-full rounded mb-2"
      />
      <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
        Get Transcript
      </button>

      {chunks.length > 0 && (
        <div className="mt-4">
          <h2 className="text-lg font-semibold">Transcript Chunks:</h2>
          {chunks.map((chunk, index) => (
            <div key={index} className="border-b py-2">
              <p><strong>{chunk.start.toFixed(1)}s - {chunk.end.toFixed(1)}s:</strong></p>
              <p>{chunk.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
