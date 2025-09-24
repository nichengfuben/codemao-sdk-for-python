"""Core API client implementation for PyCodeMao."""

import asyncio
import json
import logging
from typing import Any, Dict, Optional, List, Union
from uuid import UUID
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientResponse
from urllib.parse import urljoin, quote

from ..exceptions import (
    CodeMaoError,
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
    NetworkError,
    UserNotFoundError,
    PostNotFoundError,
    WorkNotFoundError,
)
from ..models import User, Work, Post, ForumBoard, APIResponse, PaginatedResponse
from ..utils import retry, rate_limit, safe_get, setup_logging

logger = logging.getLogger(__name__)


class CodeMaoClient:
    """
    Async-first CodeMao API client.
    
    Provides comprehensive interface to CodeMao platform with automatic
    rate limiting, retry logic, and error handling.
    
    Example:
        >>> import asyncio
        >>> from pycodemao import CodeMaoClient
        >>> 
        >>> async def main():
        ...     client = CodeMaoClient()
        ...     user = await client.login("username", "password")
        ...     works = await client.get_user_works(user.id)
        ...     print(f"User has {len(works)} works")
        >>> 
        >>> asyncio.run(main())
    """
    
    DEFAULT_BASE_URL = "https://api.codemao.cn"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_USER_AGENT = "PyCodeMao/2.0.0 (Python; +https://github.com/pycodemao/pycodemao)"
    
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        rate_limit_calls: int = 10,
        rate_limit_period: float = 1.0,
        enable_logging: bool = True,
        log_level: str = "INFO",
    ) -> None:
        """
        Initialize CodeMao client.
        
        Args:
            base_url: API base URL
            timeout: Request timeout in seconds
            user_agent: User agent string
            api_key: Optional API key for authentication
            max_retries: Maximum number of retry attempts
            rate_limit_calls: Number of calls allowed per period
            rate_limit_period: Time period for rate limiting in seconds
            enable_logging: Enable logging
            log_level: Logging level
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = ClientTimeout(total=timeout)
        self.user_agent = user_agent
        self.api_key = api_key
        self.max_retries = max_retries
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        
        self._session: Optional[ClientSession] = None
        self._authenticated = False
        self._current_user: Optional[User] = None
        
        if enable_logging:
            setup_logging(log_level)
    
    async def __aenter__(self) -> 'CodeMaoClient':
        """Async context manager entry."""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
    
    async def close(self) -> None:
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("Client session closed")
    
    async def _ensure_session(self) -> None:
        """Ensure client session is created."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            )
            logger.debug("Client session created")
    
    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    @rate_limit(calls=10, period=1.0)
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        await self._ensure_session()
        
        if require_auth and not self._authenticated:
            raise AuthenticationError("Authentication required. Please login first.")
        
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        request_headers = {"User-Agent": self.user_agent}
        if self.api_key:
            request_headers["Authorization"] = f"Bearer {self.api_key}"
        if headers:
            request_headers.update(headers)
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            async with self._session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
            ) as response:
                return await self._handle_response(response)
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            raise NetworkError(f"Network request failed: {e}") from e
        except asyncio.TimeoutError as e:
            logger.error(f"Request timeout: {e}")
            raise NetworkError(f"Request timeout after {self.timeout.total}s") from e
    
    async def _handle_response(self, response: ClientResponse) -> Dict[str, Any]:
        """Handle API response and errors."""
        status_code = response.status
        
        try:
            response_data = await response.json()
        except json.JSONDecodeError:
            response_text = await response.text()
            logger.error(f"Invalid JSON response: {response_text}")
            raise APIError(f"Invalid JSON response: {response_text}", code="INVALID_RESPONSE")
        
        logger.debug(f"Response status: {status_code}, data: {response_data}")
        
        if status_code == 429:
            retry_after = response.headers.get('Retry-After')
            retry_after_int = int(retry_after) if retry_after else None
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=retry_after_int,
                code="RATE_LIMIT_EXCEEDED"
            )
        
        if status_code == 401:
            raise AuthenticationError(
                "Authentication failed",
                code="AUTHENTICATION_FAILED"
            )
        
        if status_code == 404:
            error_msg = safe_get(response_data, 'message', 'Resource not found')
            if 'user' in error_msg.lower():
                raise UserNotFoundError(error_msg, code="USER_NOT_FOUND")
            elif 'post' in error_msg.lower():
                raise PostNotFoundError(error_msg, code="POST_NOT_FOUND")
            elif 'work' in error_msg.lower():
                raise WorkNotFoundError(error_msg, code="WORK_NOT_FOUND")
            else:
                raise APIError(error_msg, code="NOT_FOUND")
        
        if status_code >= 400:
            error_msg = safe_get(response_data, 'message', f'HTTP {status_code} error')
            error_code = safe_get(response_data, 'code', f'HTTP_{status_code}')
            raise APIError(error_msg, code=error_code)
        
        return response_data
    
    # Authentication methods
    async def login(self, username: str, password: str) -> User:
        """
        Login with username and password.
        
        Args:
            username: Username or email
            password: Password
            
        Returns:
            Authenticated user object
            
        Raises:
            AuthenticationError: If login fails
            ValidationError: If credentials are invalid
        """
        if not username or not password:
            raise ValidationError("Username and password are required")
        
        data = {
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        
        response = await self._make_request(
            "POST",
            "/auth/login",
            json_data=data,
            require_auth=False
        )
        
        # Extract token and user data
        token = safe_get(response, 'data.access_token')
        if not token:
            raise AuthenticationError("No access token in response")
        
        self.api_key = token
        self._authenticated = True
        
        user_data = safe_get(response, 'data.user')
        if not user_data:
            raise AuthenticationError("No user data in response")
        
        self._current_user = User(**user_data)
        logger.info(f"User {self._current_user.username} logged in successfully")
        
        return self._current_user
    
    async def logout(self) -> None:
        """Logout current user."""
        if self._authenticated:
            try:
                await self._make_request("POST", "/auth/logout")
            except Exception as e:
                logger.warning(f"Logout request failed: {e}")
            
            self._authenticated = False
            self._current_user = None
            self.api_key = None
            logger.info("User logged out")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        return self._authenticated
    
    @property
    def current_user(self) -> Optional[User]:
        """Get current authenticated user."""
        return self._current_user
    
    # User methods
    async def get_user(self, user_id: UUID) -> User:
        """Get user by ID."""
        response = await self._make_request("GET", f"/users/{user_id}")
        return User(**safe_get(response, 'data', {}))
    
    async def get_user_by_username(self, username: str) -> User:
        """Get user by username."""
        response = await self._make_request("GET", f"/users/username/{username}")
        return User(**safe_get(response, 'data', {}))
    
    async def update_user_profile(self, user_id: UUID, **kwargs: Any) -> User:
        """Update user profile."""
        response = await self._make_request(
            "PATCH",
            f"/users/{user_id}",
            json_data=kwargs
        )
        return User(**safe_get(response, 'data', {}))
    
    # Work methods
    async def get_user_works(
        self,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20,
        sort: str = "created_at"
    ) -> PaginatedResponse:
        """Get user's works."""
        params = {
            "page": page,
            "per_page": per_page,
            "sort": sort
        }
        
        response = await self._make_request(
            "GET",
            f"/users/{user_id}/works",
            params=params
        )
        
        works_data = safe_get(response, 'data', {})
        works = [Work(**work) for work in works_data.get('items', [])]
        
        return PaginatedResponse(
            items=[work.dict() for work in works],
            total=works_data.get('total', 0),
            page=page,
            per_page=per_page,
            total_pages=works_data.get('total_pages', 0),
            has_next=works_data.get('has_next', False),
            has_prev=works_data.get('has_prev', False)
        )
    
    async def get_work(self, work_id: UUID) -> Work:
        """Get work by ID."""
        response = await self._make_request("GET", f"/works/{work_id}")
        return Work(**safe_get(response, 'data', {}))
    
    async def create_work(self, title: str, content: str, **kwargs: Any) -> Work:
        """Create a new work."""
        data = {
            "title": title,
            "content": content,
            **kwargs
        }
        
        response = await self._make_request("POST", "/works", json_data=data)
        return Work(**safe_get(response, 'data', {}))
    
    async def update_work(self, work_id: UUID, **kwargs: Any) -> Work:
        """Update existing work."""
        response = await self._make_request(
            "PATCH",
            f"/works/{work_id}",
            json_data=kwargs
        )
        return Work(**safe_get(response, 'data', {}))
    
    async def delete_work(self, work_id: UUID) -> bool:
        """Delete work by ID."""
        await self._make_request("DELETE", f"/works/{work_id}")
        return True
    
    # Post methods
    async def get_forum_posts(
        self,
        board_id: Optional[UUID] = None,
        page: int = 1,
        per_page: int = 20,
        sort: str = "created_at"
    ) -> PaginatedResponse:
        """Get forum posts."""
        params = {
            "page": page,
            "per_page": per_page,
            "sort": sort
        }
        
        if board_id:
            params["board_id"] = str(board_id)
        
        response = await self._make_request("GET", "/posts", params=params)
        
        posts_data = safe_get(response, 'data', {})
        posts = [Post(**post) for post in posts_data.get('items', [])]
        
        return PaginatedResponse(
            items=[post.dict() for post in posts],
            total=posts_data.get('total', 0),
            page=page,
            per_page=per_page,
            total_pages=posts_data.get('total_pages', 0),
            has_next=posts_data.get('has_next', False),
            has_prev=posts_data.get('has_prev', False)
        )
    
    async def get_post(self, post_id: UUID) -> Post:
        """Get post by ID."""
        response = await self._make_request("GET", f"/posts/{post_id}")
        return Post(**safe_get(response, 'data', {}))
    
    async def create_post(
        self,
        title: str,
        content: str,
        board_id: UUID,
        **kwargs: Any
    ) -> Post:
        """Create a new forum post."""
        data = {
            "title": title,
            "content": content,
            "board_id": str(board_id),
            **kwargs
        }
        
        response = await self._make_request("POST", "/posts", json_data=data)
        return Post(**safe_get(response, 'data', {}))
    
    async def update_post(self, post_id: UUID, **kwargs: Any) -> Post:
        """Update existing post."""
        response = await self._make_request(
            "PATCH",
            f"/posts/{post_id}",
            json_data=kwargs
        )
        return Post(**safe_get(response, 'data', {}))
    
    async def delete_post(self, post_id: UUID) -> bool:
        """Delete post by ID."""
        await self._make_request("DELETE", f"/posts/{post_id}")
        return True
    
    # Forum board methods
    async def get_forum_boards(self) -> List[ForumBoard]:
        """Get all forum boards."""
        response = await self._make_request("GET", "/boards")
        boards_data = safe_get(response, 'data', [])
        return [ForumBoard(**board) for board in boards_data]
    
    async def get_forum_board(self, board_id: UUID) -> ForumBoard:
        """Get forum board by ID."""
        response = await self._make_request("GET", f"/boards/{board_id}")
        return ForumBoard(**safe_get(response, 'data', {}))
    
    # Social methods
    async def follow_user(self, user_id: UUID) -> bool:
        """Follow a user."""
        await self._make_request("POST", f"/users/{user_id}/follow")
        return True
    
    async def unfollow_user(self, user_id: UUID) -> bool:
        """Unfollow a user."""
        await self._make_request("DELETE", f"/users/{user_id}/follow")
        return True
    
    async def like_work(self, work_id: UUID) -> bool:
        """Like a work."""
        await self._make_request("POST", f"/works/{work_id}/like")
        return True
    
    async def unlike_work(self, work_id: UUID) -> bool:
        """Unlike a work."""
        await self._make_request("DELETE", f"/works/{work_id}/like")
        return True
    
    async def collect_work(self, work_id: UUID) -> bool:
        """Collect a work."""
        await self._make_request("POST", f"/works/{work_id}/collect")
        return True
    
    async def uncollect_work(self, work_id: UUID) -> bool:
        """Uncollect a work."""
        await self._make_request("DELETE", f"/works/{work_id}/collect")
        return True