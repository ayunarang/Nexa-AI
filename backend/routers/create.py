import traceback
import uuid
from fastapi import APIRouter, HTTPException, Query
from session_store import get_session_metadata, get_session_timestamps
from models.schema import TimestampRequest
from services.classifier import classify_chunks
from services.label_refiner import prepare_openrouter_prompt, parse_openrouter_labels
from utils.openrouter_utils import call_openrouter
from utils.text_utils import enforce_intro_outro_rules

router = APIRouter()

@router.post("/create")
async def create_timestamps(data: TimestampRequest, session_id: str = Query(...)):
    video_id = data.videoId

    try:
        metadata = get_session_metadata(session_id)
        timestamps = get_session_timestamps(session_id)

        if video_id not in metadata:
            raise HTTPException(status_code=404, detail="Video metadata not found")

        if video_id in timestamps:
            return {
                "status": "Cached",
                "video_id": video_id,
                "segments": timestamps[video_id]
            }

        chunks = metadata[video_id]
        classified_chunks = classify_chunks(chunks)

        enforced_chunks, intro_chunks, outro_chunks = enforce_intro_outro_rules(classified_chunks)

        core_chunks = [c for c in enforced_chunks if c.get("label") not in ("Intro", "Outro")]

        prompt = prepare_openrouter_prompt(core_chunks)

        openrouter_output = call_openrouter(prompt)

        refined_segments = parse_openrouter_labels(openrouter_output)

        refined_segments.sort(key=lambda x: x["start"])

        if intro_chunks:
            intro_segment = {
                "id": str(uuid.uuid4()),
                "start": intro_chunks[0]["start"],
                "end": intro_chunks[-1]["end"],
                "label": "Intro"
            }
            refined_segments.insert(0, intro_segment)

        if outro_chunks:
            outro_segment = {
                "id": str(uuid.uuid4()),
                "start": outro_chunks[0]["start"],
                "end": outro_chunks[-1]["end"],
                "label": "Outro"
            }
            refined_segments.append(outro_segment)

        for segment in refined_segments:
            if "id" not in segment:
                segment["id"] = str(uuid.uuid4())

        timestamps[video_id] = refined_segments

        return {
            "status": "Success",
            "video_id": video_id,
            "segments": refined_segments
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
