from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from app.core.security import get_password_hash


class UserRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, username: str, email: str, password: str, role: UserRole = UserRole.USER) -> User:
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(
                or_(User.username == username, User.email == email)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
    
    async def count(self) -> int:
        result = await self.db.execute(
            select(User)
        )
        return len(list(result.scalars().all()))