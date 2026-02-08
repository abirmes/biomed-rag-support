from typing import Optional, List
from sqlalchemy import select, func, and_ , Integer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models.query import Query


class QueryRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(
        self,
        user_id: int,
        query: str,
        response: str,
        relevance_score: Optional[float] = None,
        support_score: Optional[float] = None,
        is_relevant: bool = True,
        is_supported: bool = True,
        sources: Optional[str] = None,
        chunks_used: int = 0,
        response_time_ms: Optional[int] = None
    ) -> Query:
        query_obj = Query(
            user_id=user_id,
            query=query,
            response=response,
            relevance_score=relevance_score,
            support_score=support_score,
            is_relevant=is_relevant,
            is_supported=is_supported,
            sources=sources,
            chunks_used=chunks_used,
            response_time_ms=response_time_ms
        )
        self.db.add(query_obj)
        await self.db.commit()
        await self.db.refresh(query_obj)
        return query_obj
    
    async def get_by_id(self, query_id: int) -> Optional[Query]:
        result = await self.db.execute(
            select(Query).where(Query.id == query_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[Query]:
        result = await self.db.execute(
            select(Query)
            .where(Query.user_id == user_id)
            .order_by(Query.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Query]:
        result = await self.db.execute(
            select(Query)
            .order_by(Query.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def count_by_user(self, user_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Query.id)).where(Query.user_id == user_id)
        )
        return result.scalar_one()
    
    async def count_all(self) -> int:
        result = await self.db.execute(
            select(func.count(Query.id))
        )
        return result.scalar_one()
    
    async def get_recent_queries(
        self,
        user_id: Optional[int] = None,
        hours: int = 24,
        limit: int = 10
    ) -> List[Query]:
        since = datetime.utcnow() - timedelta(hours=hours)
        query = select(Query).where(Query.created_at >= since)
        
        if user_id:
            query = query.where(Query.user_id == user_id)
        
        query = query.order_by(Query.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_statistics(self, user_id: Optional[int] = None) -> dict:
        query = select(
            func.count(Query.id).label("total_queries"),
            func.avg(Query.response_time_ms).label("avg_response_time"),
            func.avg(Query.relevance_score).label("avg_relevance"),
            func.avg(Query.support_score).label("avg_support"),
            func.sum(func.cast(Query.is_relevant, Integer)).label("relevant_count"),
            func.sum(func.cast(Query.is_supported, Integer)).label("supported_count")
        )
        
        if user_id:
            query = query.where(Query.user_id == user_id)
        
        result = await self.db.execute(query)
        stats = result.one()
        
        total = stats.total_queries or 0
        
        return {
            "total_queries": total,
            "avg_response_time_ms": float(stats.avg_response_time or 0),
            "avg_relevance_score": float(stats.avg_relevance or 0),
            "avg_support_score": float(stats.avg_support or 0),
            "relevant_queries_percentage": (stats.relevant_count / total * 100) if total > 0 else 0,
            "supported_queries_percentage": (stats.supported_count / total * 100) if total > 0 else 0
        }
    
    async def delete(self, query: Query) -> None:
        await self.db.delete(query)
        await self.db.commit()