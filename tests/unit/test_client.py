"""Unit tests for CodeMaoClient."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from uuid import UUID
import aiohttp

from pycodemao import CodeMaoClient
from pycodemao.models import User, Work, Post, ForumBoard
from pycodemao.exceptions import (
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
    NetworkError,
)


class TestCodeMaoClient:
    """Test cases for CodeMaoClient."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return CodeMaoClient(
            base_url="https://api.test.codemao.cn",
            enable_logging=False
        )
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.base_url == "https://api.test.codemao.cn"
        assert not client.is_authenticated
        assert client.current_user is None
        await client.close()
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with CodeMaoClient(enable_logging=False) as client:
            assert client._session is not None
            assert not client._session.closed
        
        # Session should be closed after exiting context
        assert client._session.closed
    
    @pytest.mark.asyncio
    async def test_session_creation(self, client):
        """Test session creation."""
        await client._ensure_session()
        assert client._session is not None
        assert not client._session.closed
        await client.close()
    
    @pytest.mark.asyncio
    async def test_close_session(self, client):
        """Test session closing."""
        await client._ensure_session()
        await client.close()
        assert client._session.closed
    
    @pytest.mark.asyncio
    async def test_login_success(self, client, mock_response):
        """Test successful login."""
        mock_response.update({
            "data": {
                "access_token": "test_token_123",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "testuser",
                    "nickname": "Test User",
                    "email": "test@example.com",
                    "level": 5,
                    "coins": 100,
                    "diamonds": 50,
                    "followers_count": 25,
                    "following_count": 15,
                    "works_count": 10,
                    "posts_count": 5,
                    "created_at": "2023-01-01T00:00:00Z",
                    "is_verified": True,
                    "is_premium": False
                }
            }
        })
        
        with patch.object(client, '_make_request', return_value=mock_response):
            user = await client.login("testuser", "password123")
            
            assert client.is_authenticated
            assert client.current_user is not None
            assert client.current_user.username == "testuser"
            assert client.api_key == "test_token_123"
            assert isinstance(user, User)
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        with patch.object(client, '_make_request', side_effect=AuthenticationError("Invalid credentials")):
            with pytest.raises(AuthenticationError):
                await client.login("invalid", "wrong")
            
            assert not client.is_authenticated
            assert client.current_user is None
    
    @pytest.mark.asyncio
    async def test_login_missing_credentials(self, client):
        """Test login with missing credentials."""
        with pytest.raises(ValidationError, match="Username and password are required"):
            await client.login("", "")
        
        with pytest.raises(ValidationError, match="Username and password are required"):
            await client.login("username", "")
    
    @pytest.mark.asyncio
    async def test_logout(self, client, mock_response):
        """Test logout functionality."""
        # First login
        mock_response.update({
            "data": {
                "access_token": "test_token",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "testuser",
                    "nickname": "Test User",
                    "created_at": "2023-01-01T00:00:00Z"
                }
            }
        })
        
        with patch.object(client, '_make_request', return_value=mock_response):
            await client.login("testuser", "password")
        
        # Then logout
        with patch.object(client, '_make_request', return_value={"success": True}):
            await client.logout()
            
            assert not client.is_authenticated
            assert client.current_user is None
            assert client.api_key is None
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, client, mock_response):
        """Test getting user by ID."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "nickname": "Test User",
            "email": "test@example.com",
            "level": 5,
            "coins": 100,
            "diamonds": 50,
            "followers_count": 25,
            "following_count": 15,
            "works_count": 10,
            "posts_count": 5,
            "created_at": "2023-01-01T00:00:00Z",
            "is_verified": True,
            "is_premium": False
        }
        
        mock_response.update({"data": user_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            user = await client.get_user(UUID("123e4567-e89b-12d3-a456-426614174000"))
            
            assert isinstance(user, User)
            assert user.username == "testuser"
            assert user.level == 5
    
    @pytest.mark.asyncio
    async def test_get_user_by_username(self, client, mock_response):
        """Test getting user by username."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "nickname": "Test User",
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        mock_response.update({"data": user_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            user = await client.get_user_by_username("testuser")
            
            assert isinstance(user, User)
            assert user.username == "testuser"
    
    @pytest.mark.asyncio
    async def test_update_user_profile(self, client, mock_response):
        """Test updating user profile."""
        updated_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "nickname": "Updated Name",
            "bio": "Updated bio",
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        mock_response.update({"data": updated_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            user = await client.update_user_profile(
                UUID("123e4567-e89b-12d3-a456-426614174000"),
                nickname="Updated Name",
                bio="Updated bio"
            )
            
            assert isinstance(user, User)
            assert user.nickname == "Updated Name"
            assert user.bio == "Updated bio"
    
    @pytest.mark.asyncio
    async def test_get_user_works(self, client, mock_paginated_response):
        """Test getting user works."""
        work_data = {
            "id": "223e4567-e89b-12d3-a456-426614174000",
            "title": "Test Work",
            "author": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "nickname": "Test User",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "language": "python",
            "tags": ["test", "demo"],
            "likes_count": 15,
            "created_at": "2023-01-15T10:30:00Z"
        }
        
        mock_paginated_response.update({
            "items": [work_data],
            "total": 1,
            "total_pages": 1,
            "has_next": False,
            "has_prev": False
        })
        
        mock_response = {"data": mock_paginated_response}
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = await client.get_user_works(
                UUID("123e4567-e89b-12d3-a456-426614174000")
            )
            
            assert result.total == 1
            assert len(result.items) == 1
            assert result.items[0]["title"] == "Test Work"
    
    @pytest.mark.asyncio
    async def test_get_work(self, client, mock_response):
        """Test getting work by ID."""
        work_data = {
            "id": "223e4567-e89b-12d3-a456-426614174000",
            "title": "Test Work",
            "author": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "nickname": "Test User",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "created_at": "2023-01-15T10:30:00Z"
        }
        
        mock_response.update({"data": work_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            work = await client.get_work(UUID("223e4567-e89b-12d3-a456-426614174000"))
            
            assert isinstance(work, Work)
            assert work.title == "Test Work"
    
    @pytest.mark.asyncio
    async def test_create_work(self, client, mock_response):
        """Test creating a new work."""
        work_data = {
            "id": "223e4567-e89b-12d3-a456-426614174000",
            "title": "New Work",
            "content": "print('Hello World')",
            "language": "python",
            "author": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "nickname": "Test User",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "created_at": "2023-01-20T15:30:00Z"
        }
        
        mock_response.update({"data": work_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            work = await client.create_work(
                "New Work",
                "print('Hello World')",
                language="python"
            )
            
            assert isinstance(work, Work)
            assert work.title == "New Work"
            assert work.content == "print('Hello World')"
    
    @pytest.mark.asyncio
    async def test_update_work(self, client, mock_response):
        """Test updating existing work."""
        updated_data = {
            "id": "223e4567-e89b-12d3-a456-426614174000",
            "title": "Updated Work Title",
            "content": "Updated content",
            "created_at": "2023-01-15T10:30:00Z"
        }
        
        mock_response.update({"data": updated_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            work = await client.update_work(
                UUID("223e4567-e89b-12d3-a456-426614174000"),
                title="Updated Work Title",
                content="Updated content"
            )
            
            assert isinstance(work, Work)
            assert work.title == "Updated Work Title"
            assert work.content == "Updated content"
    
    @pytest.mark.asyncio
    async def test_delete_work(self, client):
        """Test deleting work."""
        with patch.object(client, '_make_request', return_value={"success": True}):
            result = await client.delete_work(UUID("223e4567-e89b-12d3-a456-426614174000"))
            assert result is True
    
    @pytest.mark.asyncio
    async def test_get_forum_posts(self, client, mock_paginated_response):
        """Test getting forum posts."""
        post_data = {
            "id": "323e4567-e89b-12d3-a456-426614174000",
            "title": "Test Post",
            "content": "Test post content",
            "author": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "nickname": "Test User",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "board": {
                "id": "423e4567-e89b-12d3-a456-426614174000",
                "name": "Test Board",
                "category": "General",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "created_at": "2023-01-20T14:20:00Z"
        }
        
        mock_paginated_response.update({
            "items": [post_data],
            "total": 1,
            "total_pages": 1,
            "has_next": False,
            "has_prev": False
        })
        
        mock_response = {"data": mock_paginated_response}
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = await client.get_forum_posts()
            
            assert result.total == 1
            assert len(result.items) == 1
            assert result.items[0]["title"] == "Test Post"
    
    @pytest.mark.asyncio
    async def test_create_post(self, client, mock_response):
        """Test creating a new forum post."""
        post_data = {
            "id": "323e4567-e89b-12d3-a456-426614174000",
            "title": "New Post",
            "content": "New post content",
            "author": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "nickname": "Test User",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "board": {
                "id": "423e4567-e89b-12d3-a456-426614174000",
                "name": "Test Board",
                "category": "General",
                "created_at": "2023-01-01T00:00:00Z"
            },
            "created_at": "2023-01-20T14:20:00Z"
        }
        
        mock_response.update({"data": post_data})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            post = await client.create_post(
                "New Post",
                "New post content",
                UUID("423e4567-e89b-12d3-a456-426614174000")
            )
            
            assert isinstance(post, Post)
            assert post.title == "New Post"
            assert post.content == "New post content"
    
    @pytest.mark.asyncio
    async def test_get_forum_boards(self, client, mock_response):
        """Test getting forum boards."""
        board_data = {
            "id": "423e4567-e89b-12d3-a456-426614174000",
            "name": "Test Board",
            "description": "A test forum board",
            "category": "General",
            "posts_count": 50,
            "is_active": True,
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        mock_response.update({"data": [board_data]})
        
        with patch.object(client, '_make_request', return_value=mock_response):
            boards = await client.get_forum_boards()
            
            assert len(boards) == 1
            assert isinstance(boards[0], ForumBoard)
            assert boards[0].name == "Test Board"
    
    @pytest.mark.asyncio
    async def test_social_operations(self, client):
        """Test social operations (follow, like, collect)."""
        test_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        
        with patch.object(client, '_make_request', return_value={"success": True}):
            # Test follow operations
            assert await client.follow_user(test_id) is True
            assert await client.unfollow_user(test_id) is True
            
            # Test like operations
            assert await client.like_work(test_id) is True
            assert await client.unlike_work(test_id) is True
            
            # Test collect operations
            assert await client.collect_work(test_id) is True
            assert await client.uncollect_work(test_id) is True
    
    @pytest.mark.asyncio
    async def test_make_request_auth_required(self, client):
        """Test that auth is required for protected endpoints."""
        with pytest.raises(AuthenticationError, match="Authentication required"):
            await client._make_request("GET", "/protected", require_auth=True)
        
        await client.close()
    
    @pytest.mark.asyncio
    async def test_make_request_network_error(self, client):
        """Test network error handling."""
        with patch('aiohttp.ClientSession.request', side_effect=aiohttp.ClientError("Network error")):
            with pytest.raises(NetworkError, match="Network request failed"):
                await client._make_request("GET", "/test", require_auth=False)
        
        await client.close()
    
    @pytest.mark.asyncio
    async def test_make_request_timeout(self, client):
        """Test timeout handling."""
        with patch('aiohttp.ClientSession.request', side_effect=asyncio.TimeoutError()):
            with pytest.raises(NetworkError, match="Request timeout"):
                await client._make_request("GET", "/test", require_auth=False)
        
        await client.close()