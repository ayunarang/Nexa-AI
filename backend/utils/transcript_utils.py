import os
import time
import requests
from urllib.parse import urlparse, parse_qs

SCRAPINGDOG_API_KEY = os.getenv("SCRAPINGDOG_API_KEY")  
ENVIRONMENT = os.getenv("ENV", "development") 


def extract_video_id(url: str) -> str:
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
    return [
        {
            'text': getattr(entry, 'text', ''),
            'start': getattr(entry, 'start', 0),
            'duration': getattr(entry, 'duration', 0)
        }
        for entry in raw_data
    ]


def fetch_transcript_from_scrapingdog(video_id: str, retries: int = 3, delay: int = 2):
    if not SCRAPINGDOG_API_KEY:
        raise EnvironmentError("Missing SCRAPINGDOG_API_KEY in environment variables.")

    url = "https://api.scrapingdog.com/youtube/transcripts/"
    params = {
        "api_key": SCRAPINGDOG_API_KEY,
        "v": video_id,
        "language": "en",
        "country": "us"
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=20)
            print(f"[ScrapingDog] Attempt {attempt} - Status: {response.status_code}")
            if response.status_code == 200:
                raw = response.json().get("transcripts", [])
                return normalize_transcript_data(raw)

            if 400 <= response.status_code < 500 and response.status_code != 429:
                break

        except Exception:
            pass

        if attempt < retries:
            time.sleep(delay)

    return None


def fetch_transcript_from_api(video_id: str):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            return normalize_transcript_data(transcripts.find_transcript(['en']).fetch())
        except (NoTranscriptFound, TranscriptsDisabled):
            pass
        try:
            return normalize_transcript_data(transcripts.find_generated_transcript(['en']).fetch())
        except Exception:
            pass
        raise RuntimeError("The video is not in English.")
    except Exception:
        return None


def fetch_transcript_data(video_id: str):
    if ENVIRONMENT == "production":
        return fetch_transcript_from_scrapingdog(video_id)
    else:
        return fetch_transcript_from_api(video_id)


def fetch_and_chunk_transcript(url: str, chunk_duration: float = 30.0):
    video_id = extract_video_id(url)

    transcript_data = fetch_transcript_data(video_id)
    if not transcript_data:
        raise RuntimeError("Transcript not available.")

    chunks = []
    current_chunk_parts = []
    current_start = transcript_data[0]["start"]
    chunk_end = current_start + chunk_duration

    for entry in transcript_data:
        start = entry["start"]
        if start < chunk_end:
            current_chunk_parts.append(entry["text"])
        else:
            chunks.append({
                "start": current_start,
                "end": chunk_end,
                "text": " ".join(current_chunk_parts).strip()
            })
            current_start = start
            chunk_end = current_start + chunk_duration
            current_chunk_parts = [entry["text"]]

    if current_chunk_parts:
        chunks.append({
            "start": current_start,
            "end": chunk_end,
            "text": " ".join(current_chunk_parts).strip()
        })

    return chunks, video_id
