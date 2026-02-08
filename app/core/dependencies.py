from typing import Optional
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.core.security import decode_token, verify_token_type
from app.core.exceptions import HTTPExceptions
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Récupère l'utilisateur actuel à partir du token JWT
    
    Args:
        credentials: Credentials HTTP Bearer
        db: Session de base de données
        
    Returns:
        User: Utilisateur authentifié
        
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    token = credentials.credentials
    
    # Décoder le token
    payload = decode_token(token)
    if not payload:
        raise HTTPExceptions.unauthorized("Token invalide ou expiré")
    
    # Vérifier le type de token
    if not verify_token_type(payload, "access"):
        raise HTTPExceptions.unauthorized("Type de token invalide")
    
    # Récupérer l'ID utilisateur
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPExceptions.unauthorized("Token invalide")
    
    # Récupérer l'utilisateur
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(int(user_id))
    
    if not user:
        raise HTTPExceptions.unauthorized("Utilisateur non trouvé")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
   
    if current_user.role != "admin":
        raise HTTPExceptions.forbidden("Droits administrateur requis")
    
    return current_user


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:

    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    
    if not payload or not verify_token_type(payload, "access"):
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user_repo = UserRepository(db)
    return await user_repo.get_by_id(int(user_id))