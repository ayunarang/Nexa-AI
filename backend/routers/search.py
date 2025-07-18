from fastapi import APIRouter, HTTPException, Query
from models.schema import SearchQueryRequest, EnhancedSearchResult
from services.search_utils import search_chunks
from services.openrouter_utils import call_openrouter
import traceback
import json

router = APIRouter()


@router.post("/search", response_model=EnhancedSearchResult)
def summarize_search(data: SearchQueryRequest, session_id: str = Query(...)):
    try:
        top_k = 3
        chunks = search_chunks(session_id, data.video_id, data.query, top_k=top_k)

        if not chunks:
            return {
                "answer": "Sorry, I couldn't find anything relevant in the video.",
                "timestamps": [],
                "confidence": "low"
            }

        for i, chunk in enumerate(chunks):
            chunk["index"] = i

        formatted_snippets = "\n\n".join([
            f"[Index: {chunk['index']}] [Start: {chunk['start']:.2f}s] {chunk['text']}"
            for chunk in chunks
        ])

        prompt = f"""
You are an intelligent assistant helping users search inside YouTube videos using transcript chunks.

## Behavior Guide:
- If the user's query is directly answered, provide a short answer and the index of the best chunk (e.g., [0]).
- If the answer is partially found, provide a short summary and top {top_k} most relevant indexes (e.g., [0, 2, 1]).
- If the answer is not found, politely say so and return the top {top_k} interesting indexes anyway.

## Return only this JSON format:
{{
  "answer": "string",
  "indexes": [int],
  "confidence": "high" | "medium" | "low"
}}

## User Query:
"{data.query}"

## Transcript Chunk Indexes (top {top_k} matches):
{formatted_snippets}
"""

        gpt_response = call_openrouter(prompt)
        print("OpenRouter Response:", gpt_response)

        try:
            gpt_result = json.loads(gpt_response)
            indexes = gpt_result.get("indexes", list(range(len(chunks))))  

            selected_timestamps = [
                {
                    "start": chunk["start"],
                    "transcript": chunk["text"]
                }
                for chunk in chunks
                if chunk["index"] in indexes
            ]

            return {
                "answer": gpt_result.get("answer", "No answer available."),
                "timestamps": selected_timestamps,
                "confidence": gpt_result.get("confidence", "low")
            }

        except json.JSONDecodeError:
            print("❌ Failed to parse GPT response as JSON.")
            return {
                "answer": gpt_response.strip(),
                "timestamps": [
                    {"start": chunk["start"], "transcript": chunk["text"]}
                    for chunk in chunks
                ],
                "confidence": "low"
            }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
