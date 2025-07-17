from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    url: str

class TranscriptChunk(BaseModel):
    start: float
    end: float
    text: str
