from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChunkMetadata(BaseModel):
    document_name: str
    page_number: Optional[int] = None
    chunk_index: int
    total_chunks: Optional[int] = None
    section: Optional[str] = None
    subsection: Optional[str] = None


class Chunk(BaseModel):
    id: str
    content: str
    metadata: ChunkMetadata
    embedding: Optional[List[float]] = None


class RetrievedChunk(BaseModel):
    chunk: Chunk
    similarity_score: float
    rerank_score: Optional[float] = None


class RAGRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    top_k: Optional[int] = Field(5, ge=1, le=20)
    enable_reranking: bool = True
    enable_self_rag: bool = True


class SelfRAGScores(BaseModel):
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    support_score: float = Field(..., ge=0.0, le=1.0)
    is_relevant: bool
    is_supported: bool
    critique: Optional[str] = None


class RAGResponse(BaseModel):
    query: str
    response: str
    retrieved_chunks: List[RetrievedChunk]
    self_rag_scores: Optional[SelfRAGScores] = None
    sources: List[Dict[str, Any]]
    response_time_ms: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentUploadResponse(BaseModel):
    filename: str
    file_size: int
    chunks_created: int
    processing_time_ms: int
    status: str


class DocumentInfo(BaseModel):
    filename: str
    num_chunks: int
    indexed_at: datetime
    file_size: int


class VectorStoreStats(BaseModel):
    total_documents: int
    total_chunks: int
    collection_name: str
    embedding_dimension: int