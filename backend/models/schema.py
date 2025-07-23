from pydantic import BaseModel
from typing import List, Literal, Optional

class TranscriptRequest(BaseModel):
    url: str


class TranscriptChunk(BaseModel):
    status: Literal["Success", "Duplicate"]
    video_id: str
    session_id: str

class ChunkEmbeddingRequest(BaseModel):
    chunks: list[TranscriptChunk]


class ClearSessionRequest(BaseModel):
    session_id: str


class SearchQueryRequest(BaseModel):
    video_id: str
    query: str

class TimestampedSummary(BaseModel):
    start: float
    transcript: str


class EnhancedSearchResult(BaseModel):
    answer: str
    timestamps: list[TimestampedSummary]
    confidence: Literal["high", "medium", "low"]


class TimestampRequest(BaseModel):
    videoId: str
