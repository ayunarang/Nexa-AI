from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    query = urlparse(url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ["www.youtube.com", "youtube.com"]:
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]
        elif query.path.startswith("/embed/"):
            return query.path.split("/")[2]
        elif query.path.startswith("/v/"):
            return query.path.split("/")[2]
    raise ValueError("Invalid YouTube URL")

def fetch_and_chunk_transcript(url: str, chunk_duration: float = 30.0):
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    chunks = []
    current_chunk = ""
    current_start = transcript[0]["start"]
    chunk_end = current_start + chunk_duration

    for entry in transcript:
        if entry["start"] < chunk_end:
            current_chunk += " " + entry["text"]
        else:
            chunks.append({
                "start": current_start,
                "end": chunk_end,
                "text": current_chunk.strip()
            })
            # start new chunk
            current_start = entry["start"]
            chunk_end = current_start + chunk_duration
            current_chunk = entry["text"]

    if current_chunk:
        chunks.append({
            "start": current_start,
            "end": chunk_end,
            "text": current_chunk.strip()
        })

    return chunks , video_id
