from typing import Any, Optional, Dict
from fastapi import HTTPException, status


class BiomedRAGException(Exception):
    """Exception de base pour l'application"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(BiomedRAGException):
    """Erreur d'authentification"""
    pass


class AuthorizationError(BiomedRAGException):
    """Erreur d'autorisation"""
    pass


class DocumentProcessingError(BiomedRAGException):
    """Erreur lors du traitement de document"""
    pass


class EmbeddingError(BiomedRAGException):
    """Erreur lors de la génération d'embeddings"""
    pass


class VectorStoreError(BiomedRAGException):
    """Erreur avec le vector store"""
    pass


class LLMError(BiomedRAGException):
    """Erreur avec le LLM"""
    pass


class RetrievalError(BiomedRAGException):
    """Erreur lors de la récupération de documents"""
    pass


class ValidationError(BiomedRAGException):
    """Erreur de validation"""
    pass


# HTTP Exceptions pour FastAPI
class HTTPExceptions:
    """Collection d'exceptions HTTP"""
    
    @staticmethod
    def unauthorized(detail: str = "Non authentifié") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @staticmethod
    def forbidden(detail: str = "Accès interdit") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
    
    @staticmethod
    def not_found(detail: str = "Ressource non trouvée") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
    
    @staticmethod
    def bad_request(detail: str = "Requête invalide") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    
    @staticmethod
    def internal_error(detail: str = "Erreur interne du serveur") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
    
    @staticmethod
    def conflict(detail: str = "Conflit") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )
    
    @staticmethod
    def unprocessable_entity(detail: str = "Entité non traitable") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )