from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """Extracts the video ID from any YouTube URL format."""
    parsed_url = urlparse(url)
    hostname = (parsed_url.hostname or '').lower()
    path = parsed_url.path

    for sub in ["www.", "m.", "music.", "gaming."]:
        hostname = hostname.replace(sub, "")

    if hostname == "youtu.be":
        return path.lstrip('/').split('?')[0]

    if hostname == "youtube.com":
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]

        for prefix in ["/embed/", "/v/", "/shorts/"]:
            if path.startswith(prefix):
                return path.split("/")[2]

    raise ValueError(f"Invalid YouTube URL: {url}")


def normalize_transcript_data(raw_data):
    """Converts transcript entries to a uniform dictionary format."""
    return [
        {
            'text': getattr(entry, 'text', ''),
            'start': getattr(entry, 'start', 0),
            'duration': getattr(entry, 'duration', 0)
        }
        for entry in raw_data
    ]


def fetch_transcript_data(video_id: str):
    """Fetches and returns English transcript data if available."""
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        # 1. Manual English transcript
        try:
            transcript = transcripts.find_transcript(['en'])
            return normalize_transcript_data(transcript.fetch())
        except (NoTranscriptFound, TranscriptsDisabled):
            pass

        # 2. Auto-generated English transcript
        try:
            auto_transcript = transcripts.find_generated_transcript(['en'])
            return normalize_transcript_data(auto_transcript.fetch())
        except Exception:
            pass

        raise RuntimeError("The video is not in English.")

    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
        print(f"[Transcript API error]: {e}")
        raise RuntimeError("Transcript not available for this video.")


def fetch_and_chunk_transcript(url: str, chunk_duration: float = 30.0):
    """Main function: fetches transcript for URL and chunks it."""
    video_id = extract_video_id(url)
    transcript_data = fetch_transcript_data(video_id)

    chunks = []
    current_chunk = ""
    current_start = transcript_data[0].get("start", 0)
    chunk_end = current_start + chunk_duration

    for entry in transcript_data:
        if entry.get("start", 0) < chunk_end:
            current_chunk += " " + entry["text"]
        else:
            chunks.append({
                "start": current_start,
                "end": chunk_end,
                "text": current_chunk.strip()
            })
            current_start = entry["start"]
            chunk_end = current_start + chunk_duration
            current_chunk = entry["text"]

    if current_chunk:
        chunks.append({
            "start": current_start,
            "end": chunk_end,
            "text": current_chunk.strip()
        })

    return chunks, video_id
