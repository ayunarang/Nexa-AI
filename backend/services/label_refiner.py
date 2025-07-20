import re

def prepare_openrouter_prompt(chunks):
    prompt_lines = []
    for chunk in chunks:
        sample_text = " ".join(chunk["text"].split()[:10])
        start = round(chunk["start"], 1)
        end = round(chunk["end"], 1)
        prompt_lines.append(f"[{start:.1f}s-{end:.1f}s] Label: {chunk['label']} | Text: \"{sample_text}\"")

    return f"""
You are an AI agent tasked with refining labeled, timestamped segments from a YouTube transcript. A traditional classifier has generated rough labels, which may be vague, incorrect, or repetitive. The end result should be AT MAX 12-14 total labels with timestamps.

Your task is to correct, rename, and group labels while following these strict rules:

---

Hard Rules (Must Follow Exactly):

1. Correct “Sponsorship” Mislabels:  
   Only assign the label "Sponsorship" if the Text explicitly includes promotional content using language like:  
   - “This video is sponsored by…”  
   - “Thanks to [brand] for sponsoring…”  
   - “In partnership with…”  
   - “Paid promotion”, “Affiliate links”, etc.  
   If none of these are present, do not use the label. Instead, re-label it based on actual Text content.

2. Do NOT Modify Text:  
   Do not edit, paraphrase, rewrite, or return the Text.  
   You may only use Text to understand and improve the label.

3. Do NOT Repeat Labels Non-Contiguously:  
   If a label (e.g., "Outfit Ideas") appears more than once but is not directly adjacent, you must rename one or more of them to prevent repetition. Use creative or broader category names instead.

4. Merge Only Contiguous Segments:  
   Segments may only be grouped if they are immediately adjacent and discuss the same or closely related topic. Do not merge distant or similar-but-non-adjacent segments.

5. Chronological Order Required:  
   Final output must keep all segments in strict chronological order.  
   Merged segments must have non-overlapping timestamps.

---

Refinement Rules (Creative But Constrained):

6. Refine Generic Labels:  
   Replace vague or bland labels with creative, specific 2–3 word labels that accurately reflect the segment content.  
   Example: Rename “Chat” to “Bookstore Chat” or “Late Night Talk” if relevant.

7. Rename Specific Terms Thoughtfully:  
   - If a segment labeled "Product Review" is just showing or talking about recently bought items (e.g., clothes, books), rename it to "Haul".  
   - Keep "Product Review" only when analysis, pros/cons, or opinions are shared about a product.

8. Avoid Word Reuse in Labels:  
   Do not reuse the same word across different labels in non-contiguous segments.  
   For example, avoid using:  
   - "Outing and Chat", then "Outing and Haul", then "Outing Plans"  
   Instead, rename to:  
   - “Cafe Hangout”, “Shopping Vlog”, “City Errands”

---

Final Cleanup Instructions:

9. Merge Contiguous Duplicate Labels:  
   If the same label appears in adjacent segments, merge them into one entry with combined timestamps.  
   Example:  
   [00:05 - 00:10] Outfit Ideas  
   [00:10 - 00:13] Outfit Ideas  
   → [00:05 - 00:13] Outfit Ideas

10. Use Context-Specific Names When Possible:  
    If Text clearly mentions a unique activity, location, or object (e.g., “matcha”, “zoo”, “new sneakers”), reflect it in the label.  
    Example: Rename “Food and Chat” → “Matcha Run” or “Cafe Visit”

11. Final Grouping:  
    After refining labels, scan for adjacent entries that are part of the same scene, narrative thread, or loosely related activity.  
    If multiple adjacent segments revolve around a shared theme or purpose (e.g., errands, food, prep, plans), they must be grouped under a single broader label that summarizes the full section.  
    Example:  
    Instead of:  
    [193.0s - 223.0s] Hungry Errands  
    [224.2s - 254.2s] Hunger Chat  
    [254.8s - 284.8s] Plan Adjustments  
    [284.9s - 314.9s] Dinner Thoughts  
    [315.0s - 345.0s] Return Plans  
    → Group them into:  
    [193.0s - 345.0s] Dinner Plans

    Do not return multiple micro-labels for a continuous sequence. Broad, cohesive grouping is required to reflect the larger context.  
    Especially combine segments that are only 50–60 seconds long into a larger labeled chunk if they belong to a shared scene or activity.

---

After all label refinement is done, perform one final pass over the list:
- If 2 or more adjacent segments are closely related in content or purpose (even with different labels), merge them under a single meaningful label in such a way to produce only MAXIMUM 12 entries.

**Your goal is to reduce fragmentation and deliver meaningful, cohesive groupings.**

🔴 Strict Final Rule (Cap Limit):

**DO NOT return more than 12 total entries.**  
Combine adjacent related segments wherever necessary to stay within this range.

---

Output Format (Strict):

Return the final list of merged and cleaned segments using this exact format:

[start timestamp - end timestamp] Refined Label

Example:

[starting - ending] Outfit Ideas  
[starting - ending] Cafe Visit  
[starting - ending] Self Reflection  

---

Never return the original or modified Text. Only return formatted refined timestamps and labels.

Return in this format only (where start timestamp and end timestamp represent newly merged timestamps if the label was grouped):

[start timestamp - end timestamp] Refined Label

Data:
{chr(10).join(prompt_lines)}
"""

def parse_openrouter_labels(openrouter_response: str):
    refined = []
    lines = openrouter_response.strip().splitlines()

    for line in lines:
        match = re.match(r"\[(\d+(\.\d+)?)s?-(\d+(\.\d+)?)s?\]\s+(.+)", line)
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
