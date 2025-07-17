export default function TranscriptViewer({ chunks }) {
  if (!chunks.length) return null;

  return (
    <div className="my-6">
      <h2 className="text-xl font-semibold mb-2">Transcript Chunks ({chunks.length})</h2>
      {chunks.map((chunk, i) => (
        <div key={i} className="border-b py-2 text-sm">
          <p className="text-gray-600 font-semibold">
            {chunk.start.toFixed(1)}s – {chunk.end.toFixed(1)}s
          </p>
          <p>{chunk.text}</p>
        </div>
      ))}
    </div>
  );
}
