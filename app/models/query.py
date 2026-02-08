from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base


class Query(Base):
    
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    
    # Métadonnées Self-RAG
    relevance_score = Column(Float, nullable=True)
    support_score = Column(Float, nullable=True)
    is_relevant = Column(Boolean, default=True)
    is_supported = Column(Boolean, default=True)
    
    # Sources utilisées
    sources = Column(Text, nullable=True)  # JSON stringifié des sources
    chunks_used = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    response_time_ms = Column(Integer, nullable=True)  # Temps de réponse en millisecondes
    
    def __repr__(self) -> str:
        return f"<Query(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "response": self.response,
            "relevance_score": self.relevance_score,
            "support_score": self.support_score,
            "is_relevant": self.is_relevant,
            "is_supported": self.is_supported,
            "sources": self.sources,
            "chunks_used": self.chunks_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "response_time_ms": self.response_time_ms,
        }