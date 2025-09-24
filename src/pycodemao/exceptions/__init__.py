"""Custom exceptions for PyCodeMao."""

from typing import Optional, Dict, Any


class CodeMaoError(Exception):
    """Base exception for all PyCodeMao errors."""
    
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class AuthenticationError(CodeMaoError):
    """Raised when authentication fails."""
    pass


class APIError(CodeMaoError):
    """Raised when API request fails."""
    pass


class RateLimitError(CodeMaoError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ValidationError(CodeMaoError):
    """Raised when input validation fails."""
    pass


class NetworkError(CodeMaoError):
    """Raised when network request fails."""
    pass


class UserNotFoundError(CodeMaoError):
    """Raised when a user is not found."""
    pass


class PostNotFoundError(CodeMaoError):
    """Raised when a post is not found."""
    pass


class WorkNotFoundError(CodeMaoError):
    """Raised when a work is not found."""
    pass


class ForumBoardNotFoundError(CodeMaoError):
    """Raised when a forum board is not found."""
    pass


class InsufficientPermissionsError(CodeMaoError):
    """Raised when user lacks required permissions."""
    pass