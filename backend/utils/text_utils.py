import re

def clean_text(text: str) -> str:
    return re.sub(r'[\[\<].*?[\]\>]', '', text).strip()

def enforce_intro_outro_rules(chunks):
    if not chunks:
        return chunks, [], []

    intro_keywords = ["welcome", "today", "this video", "my name is", "i'm going to", "hey guys", "in today's video"]
    outro_keywords = ["thanks for watching", "subscribe", "see you", "next video", "bye", "catch you later", "that's all", "signing off"]

    def is_intro(text):
        return any(kw in clean_text(text).lower() for kw in intro_keywords)

    def is_outro(text):
        return any(kw in clean_text(text).lower() for kw in outro_keywords)

    intro_chunks = []
    outro_chunks = []

    # Forcefully label first and last as Intro and Outro
    chunks[0]["label"] = "Intro"
    intro_chunks.append(chunks[0])

    chunks[-1]["label"] = "Outro"
    outro_chunks.append(chunks[-1])

    # Refine intro with second chunk if matched
    if len(chunks) > 1 and is_intro(chunks[1]["text"]):
        chunks[1]["label"] = "Intro"
        intro_chunks.append(chunks[1])

    # Refine outro with second last chunk if matched
    if len(chunks) > 2 and is_outro(chunks[-2]["text"]):
        chunks[-2]["label"] = "Outro"
        outro_chunks.insert(0, chunks[-2])  # maintain order

    return chunks, intro_chunks, outro_chunks
