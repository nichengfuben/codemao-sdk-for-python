"""CodeMao SDK for Python - A modern, async Python SDK for CodeMao API."""

from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pycodemao.client import CodeMaoClient
from pycodemao.models import User, Work, Post, ForumBoard
from pycodemao.exceptions import (
    CodeMaoError,
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
    PermissionError,
    ServerError,
    NetworkError,
    TimeoutError
)

__version__ = "2.0.0"
__all__ = [
    "CodeMaoClient",
    "User",
    "Work", 
    "Post",
    "ForumBoard",
    "CodeMaoError",
    "AuthenticationError",
    "APIError",
    "RateLimitError",
    "ValidationError",
    "ResourceNotFoundError",
    "PermissionError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    "__version__"
]

# Convenience function for quick client creation
def create_client(api_key: str, base_url: Optional[str] = None) -> CodeMaoClient:
    """Create a new CodeMao API client.
    
    Args:
        api_key: Your CodeMao API key
        base_url: Optional custom base URL for the API
        
    Returns:
        Configured CodeMaoClient instance
        
    Example:
        >>> import pycodemao
        >>> client = pycodemao.create_client("your_api_key_here")
        >>> user = await client.get_user("some_username")
        >>> print(user.nickname)
    """
    return CodeMaoClient(api_key=api_key, base_url=base_url)