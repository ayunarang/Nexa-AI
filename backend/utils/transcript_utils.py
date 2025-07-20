import os
import tempfile
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
from webvtt import read as read_vtt
import yt_dlp


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


def fetch_transcript_from_api(video_id: str):
    try:
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
    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return None


def fetch_transcript_from_webvtt(video_id: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, f"{video_id}.vtt")
        try:
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'subtitleslangs': ['en'],
                'subtitlesformat': 'vtt',
                'outtmpl': os.path.join(tmpdir, '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

            transcript = []
            for caption in read_vtt(output_path):
                start_seconds = time_str_to_seconds(caption.start)
                end_seconds = time_str_to_seconds(caption.end)
                duration = end_seconds - start_seconds
                transcript.append({
                    "start": start_seconds,
                    "duration": duration,
                    "text": caption.text.replace('\n', ' ')
                })

            return transcript
        except Exception as e:
            print(f"[WebVTT Fallback Error]: {e}")
            return None


def time_str_to_seconds(time_str):
    h, m, s = time_str.replace(',', '.').split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)


def fetch_transcript_data(video_id: str):
    transcript = fetch_transcript_from_api(video_id)
    if transcript:
        return transcript
    return fetch_transcript_from_webvtt(video_id)


def fetch_and_chunk_transcript(url: str, chunk_duration: float = 30.0):
    video_id = extract_video_id(url)
    transcript_data = fetch_transcript_data(video_id)

    if not transcript_data:
        raise RuntimeError("Transcript not available via API or fallback.")

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
