import re

BRACKETS_RE = re.compile(r'[\[\<].*?[\]\>]')

INTRO_KEYWORDS = [kw.lower() for kw in [
    "welcome", "today", "this video", "my name is", "i'm going to", "hey guys", "in today's video"
]]
OUTRO_KEYWORDS = [kw.lower() for kw in [
    "thanks for watching", "subscribe", "see you", "next video", "bye", "catch you later", "that's all", "signing off"
]]

def clean_text(text: str) -> str:
    return BRACKETS_RE.sub('', text).strip()

def enforce_intro_outro_rules(chunks):
    if not chunks:
        return chunks, [], []

    def is_intro(text: str) -> bool:
        lowered = clean_text(text).lower()
        return any(kw in lowered for kw in INTRO_KEYWORDS)

    def is_outro(text: str) -> bool:
        lowered = clean_text(text).lower()
        return any(kw in lowered for kw in OUTRO_KEYWORDS)

    intro_chunks = []
    outro_chunks = []

    chunks[0]["label"] = "Intro"
    intro_chunks.append(chunks[0])

    chunks[-1]["label"] = "Outro"
    outro_chunks.append(chunks[-1])

    if len(chunks) > 1 and is_intro(chunks[1]["text"]):
        chunks[1]["label"] = "Intro"
        intro_chunks.append(chunks[1])

    if len(chunks) > 2 and is_outro(chunks[-2]["text"]):
        chunks[-2]["label"] = "Outro"
        outro_chunks.insert(0, chunks[-2])

    return chunks, intro_chunks, outro_chunks
