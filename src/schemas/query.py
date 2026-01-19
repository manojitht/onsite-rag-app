from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    context: Optional[dict] = None
    user_clearance: Optional[List[str]] = []

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float
    applied_filters: List[str]
    conflict_resolution: Optional[dict] = None




