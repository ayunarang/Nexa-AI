import re

def prepare_openrouter_prompt(chunks):
    prompt_lines = []
    for chunk in chunks:
        sample_text = " ".join(chunk["text"].split()[:10])
        start = round(chunk["start"], 1)
        end = round(chunk["end"], 1)
        prompt_lines.append(f"[{start:.1f}s-{end:.1f}s] Label: {chunk['label']} | Text: \"{sample_text}\"")

    return f"""
You are an AI tasked with refining labeled, timestamped segments from a YouTube transcript. An initial classifier has generated rough labels which may be vague, incorrect, or repetitive.

Your objective is to improve the quality of these labels through correction, renaming, and grouping — producing no more than 12–14 final entries with updated timestamps.

--- HARD RULES ---

1. Sponsorship Labeling:
Only use "Sponsorship" if the Text explicitly includes language like:
- "This video is sponsored by..."
- "Thanks to [brand] for sponsoring..."
- "In partnership with..."
- "Paid promotion", "Affiliate links", etc.
Otherwise, relabel based on actual content.

2. Do NOT Modify Text:
Do not change or return the Text. Only use it to guide labeling.

3. No Non-Contiguous Repeats:
Avoid using the same label for segments that are not adjacent. Rename them using broader or more descriptive labels.

4. Merge Only Adjacent Segments:
Only group segments if they are immediately next to each other and clearly related.

5. Maintain Chronology:
Keep all segments in strict chronological order. Merged timestamps must be continuous and non-overlapping.

--- REFINEMENT RULES ---

6. Improve Generic Labels:
Replace vague labels like "Chat" with something more specific using cues from the Text. For example, rename "Chat" → "Late Night Talk" or "Bookstore Chat".

7. Rename with Intent:
Use "Haul" instead of "Product Review" when only items are being shown. Keep "Product Review" only if opinions or analysis are included.

8. Avoid Repeating Words Across Labels:
Don’t reuse the same core word in different labels unless they are merged. Example: Replace "Outing and Chat" and "Outing Plans" with distinct, creative names like "Cafe Vlog", "City Errands".

--- FINAL CLEANUP INSTRUCTIONS ---

9. Merge Adjacent Duplicates:
If the same label appears in consecutive segments, merge them into a single entry with updated timestamps.

10. Use Context-Based Names:
If specific details (e.g., "matcha", "zoo", "new sneakers") appear in the Text, include them in the label name.

11. Final Grouping Pass:
If several adjacent segments reflect a shared theme (e.g., errands, dinner planning), group them under one broader label. Ensure grouped segments form a continuous narrative, and merge small segments (under 60s) into a larger one if relevant.

--- STRICT FINAL RULE ---

You must return a maximum of 12 final entries.
Use grouping aggressively to reduce fragmentation and deliver cohesive, meaningful labels.

Do not include Text in the output. Only return cleaned, chronological timestamp-label pairs.

--- OUTPUT FORMAT (STRICT) ---

[start timestamp - end timestamp] Refined Label

Example:
[0.0s - 55.0s] Outfit Ideas  
[55.1s - 120.2s] Cafe Visit  
[120.3s - 190.5s] Self Reflection

Data:
{chr(10).join(prompt_lines)}
"""


def parse_openrouter_labels(openrouter_response: str):
    refined = []
    lines = openrouter_response.strip().splitlines()

    for line in lines:
        match = re.match(r"\[(\d+(\.\d+)?)s\s*-\s*(\d+(\.\d+)?)s\]\s+(.+)", line)
        if match:
            start = float(match.group(1))
            end = float(match.group(3))
            label = match.group(5).strip()
            refined.append({
                "start": start,
                "end": end,
                "label": label
            })
    return refined
