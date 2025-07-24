from fastapi import APIRouter, HTTPException, Query
from models.schema import SearchQueryRequest, EnhancedSearchResult
from utils.search_utils import search_chunks
from utils.openrouter_utils import call_openrouter
import traceback
import json
import re

router = APIRouter()


@router.post("/search", response_model=EnhancedSearchResult)
def summarize_search(data: SearchQueryRequest, session_id: str = Query(...)):
    try:
        top_k = 5
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
You are a helpful assistant that searches content in YouTube videos using transcript snippets.

Instructions:

- Interpret the user's query intelligently:
  - Match direct mentions, indirect answers, or universally accepted explanations of the query.
  - If any part of the query is clearly answered, implied, or explained, treat it as relevant.

Response Logic:

1. Directly Answered:
   - If the query is directly answered or clearly addressed in one chunk:
     - Respond briefly.
     - Return the best matching index. Example: "indexes": [0]

2. Partially Answered / Multiple Chunks:
   - If the answer is partially answered or spread across multiple chunks:
     - Summarize the relevant content.
     - Return top {top_k} chunk indexes. Example: "indexes": [0, 2, 4]

3. Not Answered:
   - If the query is not answered at all:
     - Respond politely. For example:
       "No, there was no part about '{{query}}' in the video, but here are some interesting bits you may enjoy."
     - Return 3 relevant indexes from the top {top_k} as suggestions.

Output Format (strict JSON):
{{
  "answer": "string",
  "indexes": [int],
  "confidence": "high" | "medium" | "low"
}}

User Query:
"{data.query}"

Top {top_k} Transcript Chunks:
{formatted_snippets}
"""


        gpt_response = call_openrouter(prompt)

        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", gpt_response, re.DOTALL)
        if match:
            gpt_response = match.group(1)

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

            # Create index-to-timestamp mapping in MM:SS
            index_to_time = {
                chunk["index"]: f"{int(chunk['start'] // 60):02d}:{int(chunk['start'] % 60):02d}"
                for chunk in chunks
            }

            raw_answer = gpt_result.get("answer", "No answer available.")

            # Replace single index mentions: "at index 1" or "index 0"
            def replace_single_index(match):
                index = int(match.group(1))
                timestamp = index_to_time.get(index)
                return f"at {timestamp}" if timestamp else ""

            answer_with_timestamps = re.sub(
                r"(?:at\s+)?index\s+(\d+)",
                replace_single_index,
                raw_answer,
                flags=re.IGNORECASE
            )

            # Replace list of indexes: "indexes [0, 1]"
            def replace_multiple_indexes(match):
                index_list = match.group(1)
                try:
                    index_nums = [int(i.strip()) for i in index_list.split(",")]
                    times = [index_to_time[i] for i in index_nums if i in index_to_time]
                    return "at " + ", ".join(times)
                except:
                    return ""

            answer_with_timestamps = re.sub(
                r"indexes\s*\[\s*([\d\s,]+)\s*\]",
                replace_multiple_indexes,
                answer_with_timestamps,
                flags=re.IGNORECASE
            ).strip()

            return {
                "answer": answer_with_timestamps,
                "timestamps": selected_timestamps,
                "confidence": gpt_result.get("confidence", "low")
            }

        except json.JSONDecodeError:
            print("Failed to parse GPT response as JSON.")
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
