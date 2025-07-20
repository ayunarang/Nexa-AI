import YouTube from "react-youtube";

function PlaceholderOverlay() {
  return (
    <div className="absolute inset-0 bg-[rgba(216,180,254,0.2)] border-4 border-purple-700 rounded-2xl flex items-center justify-center shadow-lg transition-opacity duration-700 ease-in-out">
      <div
        className="w-14 h-14 bg-white/40 text-purple-700/40 flex items-center justify-center rounded-full"
        aria-label="Click to play"
      >
        <svg
          className="w-10 h-10 ml-1"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M8 5v14l11-7z" />
        </svg>
      </div>
    </div>
  );
}

function YouTubeEmbed({ videoId, setPlayer }) {
  return (
    <div className="absolute inset-0 w-full h-full rounded-2xl overflow-hidden shadow-lg transition-opacity duration-700 ease-in-out">
      <div className="relative w-full h-full">
        <YouTube
          videoId={videoId}
          className="absolute top-0 left-0 w-full h-full"
          iframeClassName="w-full h-full"
          opts={{
            width: "100%",
            height: "100%",
            playerVars: { autoplay: 0 },
          }}
          onReady={(event) => setPlayer(event.target)}
        />
      </div>
    </div>
  );
}


export default function VideoPlayer({ videoId, setPlayer }) {
  return (
    <div className="relative w-full max-w-3xl aspect-video">
      {!videoId && <PlaceholderOverlay />}
      {videoId && <YouTubeEmbed videoId={videoId} setPlayer={setPlayer} />}
    </div>
  );
}
