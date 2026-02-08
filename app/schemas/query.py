from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class QueryBase(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)


class QueryCreate(QueryBase):
    """Schéma pour la création d'une query"""
    pass


class SourceInfo(BaseModel):
    document_name: str
    page: Optional[int] = None
    chunk_id: Optional[str] = None
    relevance_score: float


class QueryResponse(BaseModel):
    id: int
    user_id: int
    query: str
    response: str
    relevance_score: Optional[float] = None
    support_score: Optional[float] = None
    is_relevant: bool
    is_supported: bool
    sources: Optional[str] = None
    chunks_used: int
    created_at: datetime
    response_time_ms: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class QueryListResponse(BaseModel):
    queries: List[QueryResponse]
    total: int
    page: int
    page_size: int


class QueryStats(BaseModel):
    total_queries: int
    avg_response_time_ms: float
    avg_relevance_score: float
    avg_support_score: float
    relevant_queries_percentage: float
    supported_queries_percentage: float