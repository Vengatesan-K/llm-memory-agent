from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    use_cache: bool = True


class QueryResponse(BaseModel):
    answer: str
    source: str  # "cache" or "llm"
    conversation_id: Optional[str] = None
    cached: bool
