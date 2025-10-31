from pydantic import BaseModel, Field
from typing import List, Optional


class InsightOutput(BaseModel):
    """For generating one-line insights for long-term memory."""
    insight: str
    
class ContextOutput(BaseModel):
    """Research context fetched from semantic memory."""
    related_facts: List[str]
    relevance_scores: Optional[List[float]] = None
    
class AnswerOutput(BaseModel):
    """Structured output for synthesized answers."""
    answer: str = Field(..., description="Final answer text")
    confidence: Optional[float] = Field(None, description="Model's confidence score (0-1)")
    sources: Optional[List[str]] = Field(None, description="References or retrieved docs")