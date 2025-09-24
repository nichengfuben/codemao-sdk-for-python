"""Integration tests for CodeMao API client."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from uuid import uuid4

from pycodemao.client import CodeMaoClient
from pycodemao.exceptions import (
    AuthenticationError,
    APIError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError
)
from pycodemao.models import User, Work, Post, ForumBoard, APIResponse


class TestCodeMaoClientIntegration:
    """Integration tests for CodeMaoClient."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return CodeMaoClient(api_key="test_api_key")
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock aiohttp session."""
        session = AsyncMock()
        session.request = AsyncMock()
        return session
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock response."""
        response = AsyncMock()
        response.status = 200
        response.json = AsyncMock()
        response.text = AsyncMock(return_value="OK")
        return response
    
    @pytest.mark.asyncio
    async def test_successful_authentication_flow(self, client, mock_session, mock_response):
        """Test successful authentication flow."""
        # Mock successful authentication response
        mock_response.json.return_value = {
            "success": True,
            "code": 200,
            "message": "Authentication successful",
            "data": {
                "user": {
                    "id": str(uuid4()),
                    "username": "testuser",
                    "nickname": "Test User",
                    "level": 5,
                    "coins": 100,
                    "diamonds": 50,
                    "followers_count": 25,
                    "following_count": 15,
                    "works_count": 10,
                    "posts_count": 5,
                    "created_at": datetime.now().isoformat(),
                    "is_verified": True,
                    "is_premium": False
                }
            }
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            user = await client.authenticate("test_api_key")
            
            assert user is not None
            assert user.username == "testuser"
            assert user.nickname == "Test User"
            assert user.level == 5
    
    @pytest.mark.asyncio
    async def test_failed_authentication_flow(self, client, mock_session, mock_response):
        """Test failed authentication flow."""
        # Mock failed authentication response
        mock_response.status = 401
        mock_response.json.return_value = {
            "success": False,
            "code": 401,
            "message": "Invalid API key",
            "data": None
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            with pytest.raises(AuthenticationError) as exc_info:
                await client.authenticate("invalid_api_key")
            
            assert "Invalid API key" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, client, mock_session, mock_response):
        """Test rate limit error handling."""
        # Mock rate limit response
        mock_response.status = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.json.return_value = {
            "success": False,
            "code": 429,
            "message": "Rate limit exceeded",
            "data": None
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            with pytest.raises(RateLimitError) as exc_info:
                await client.get_user("testuser")
            
            assert "Rate limit exceeded" in str(exc_info.value)
            assert exc_info.value.retry_after == 60
    
    @pytest.mark.asyncio
    async def test_user_profile_retrieval_flow(self, client, mock_session, mock_response):
        """Test user profile retrieval flow."""
        user_data = {
            "id": str(uuid4()),
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
            "created_at": datetime.now().isoformat(),
            "is_verified": True,
            "is_premium": False
        }
        
        mock_response.json.return_value = {
            "success": True,
            "code": 200,
            "message": "User retrieved successfully",
            "data": {"user": user_data}
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            user = await client.get_user("testuser")
            
            assert user is not None
            assert user.username == "testuser"
            assert user.nickname == "Test User"
            assert user.email == "test@example.com"
            assert user.level == 5
    
    @pytest.mark.asyncio
    async def work_creation_and_retrieval_flow(self, client, mock_session, mock_response):
        """Test work creation and retrieval flow."""
        # Mock work creation
        work_data = {
            "id": str(uuid4()),
            "title": "Test Work",
            "description": "A test work",
            "language": "python",
            "tags": ["test", "python", "demo"],
            "likes_count": 15,
            "comments_count": 3,
            "collections_count": 8,
            "views_count": 150,
            "is_public": True,
            "is_featured": False,
            "created_at": datetime.now().isoformat()
        }
        
        mock_response.json.return_value = {
            "success": True,
            "code": 201,
            "message": "Work created successfully",
            "data": {"work": work_data}
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            work = await client.create_work(
                title="Test Work",
                description="A test work",
                language="python",
                tags=["test", "python", "demo"]
            )
            
            assert work is not None
            assert work.title == "Test Work"
            assert work.language == "python"
            assert work.tags == ["test", "python", "demo"]
    
    @pytest.mark.asyncio
    async def test_work_listing_with_pagination(self, client, mock_session, mock_response):
        """Test work listing with pagination."""
        works_data = [
            {
                "id": str(uuid4()),
                "title": f"Work {i}",
                "description": f"Description {i}",
                "language": "python",
                "tags": ["test"],
                "likes_count": i * 10,
                "comments_count": i * 5,
                "collections_count": i * 3,
                "views_count": i * 100,
                "is_public": True,
                "is_featured": False,
                "created_at": datetime.now().isoformat()
            }
            for i in range(1, 4)
        ]
        
        mock_response.json.return_value = {
            "success": True,
            "code": 200,
            "message": "Works retrieved successfully",
            "data": {
                "items": works_data,
                "total": 3,
                "page": 1,
                "per_page": 20,
                "total_pages": 1,
                "has_next": False,
                "has_prev": False
            }
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            works = await client.get_user_works("testuser", page=1, per_page=20)
            
            assert len(works) == 3
            assert works[0].title == "Work 1"
            assert works[1].title == "Work 2"
            assert works[2].title == "Work 3"
    
    @pytest.mark.asyncio
    async def test_forum_post_creation_flow(self, client, mock_session, mock_response):
        """Test forum post creation flow."""
        # Mock forum board
        board_data = {
            "id": str(uuid4()),
            "name": "General Discussion",
            "description": "General discussion board",
            "category": "General",
            "posts_count": 100,
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        
        # Mock post creation
        post_data = {
            "id": str(uuid4()),
            "title": "Test Post",
            "content": "This is a test post content.",
            "board": board_data,
            "is_pinned": False,
            "is_locked": False,
            "likes_count": 10,
            "comments_count": 5,
            "views_count": 100,
            "tags": ["discussion", "help"],
            "created_at": datetime.now().isoformat()
        }
        
        mock_response.json.return_value = {
            "success": True,
            "code": 201,
            "message": "Post created successfully",
            "data": {"post": post_data}
        }
        
        with patch.object(client, '_session', mock_session):
            mock_session.request.return_value = mock_response
            
            post = await client.create_post(
                title="Test Post",
                content="This is a test post content.",
                board_id=board_data["id"],
                tags=["discussion", "help"]
            )
            
            assert post is not None
            assert post.title == "Test Post"
            assert post.content == "This is a test post content."
            assert post.board.name == "General Discussion"
            assert post.tags == ["discussion", "help"]
    
    @pytest.mark.asyncio
    async def test_error_recovery_and_retry(self, client, mock_session, mock_response):
        """Test error recovery and retry mechanism."""
        # First request fails with network error
        # Second request succeeds
        
        user_data = {
            "id": str(uuid4()),
            "username": "testuser",
            "nickname": "Test User",
            "created_at": datetime.now().isoformat()
        }
        
        success_response = AsyncMock()
        success_response.status = 200
        success_response.json.return_value = {
            "success": True,
            "code": 200,
            "message": "User retrieved successfully",
            "data": {"user": user_data}
        }
        
        # Mock network error for first request, success for second
        mock_session.request.side_effect = [
            Exception("Network error"),  # First request fails
            success_response  # Second request succeeds
        ]
        
        with patch.object(client, '_session', mock_session):
            with patch('asyncio.sleep', new_callable=AsyncMock):  # Mock sleep for faster tests
                user = await client.get_user("testuser")
                
                assert user is not None
                assert user.username == "testuser"
                assert mock_session.request.call_count == 2  # Retried once
    
    @pytest.mark.asyncio
    async def test_concurrent_api_requests(self, client, mock_session, mock_response):
        """Test concurrent API requests."""
        # Mock multiple user responses
        users_data = [
            {
                "id": str(uuid4()),
                "username": f"user{i}",
                "nickname": f"User {i}",
                "created_at": datetime.now().isoformat()
            }
            for i in range(1, 4)
        ]
        
        # Create mock responses for each user
        responses = []
        for user_data in users_data:
            response = AsyncMock()
            response.status = 200
            response.json.return_value = {
                "success": True,
                "code": 200,
                "message": "User retrieved successfully",
                "data": {"user": user_data}
            }
            responses.append(response)
        
        mock_session.request.side_effect = responses
        
        with patch.object(client, '_session', mock_session):
            # Make concurrent requests
            tasks = [
                client.get_user(f"user{i}")
                for i in range(1, 4)
            ]
            
            users = await asyncio.gather(*tasks)
            
            assert len(users) == 3
            assert users[0].username == "user1"
            assert users[1].username == "user2"
            assert users[2].username == "user3"
            assert mock_session.request.call_count == 3
    
    @pytest.mark.asyncio
    async def test_context_manager_usage(self):
        """Test client as context manager."""
        async with CodeMaoClient(api_key="test_key") as client:
            assert client is not None
            assert client._session is not None
        
        # Session should be closed after context exit
        # Note: In real implementation, we'd check if session is closed
    
    @pytest.mark.asyncio
    async def test_client_cleanup(self, client):
        """Test proper client cleanup."""
        # Create a mock session
        mock_session = AsyncMock()
        client._session = mock_session
        
        # Close the client
        await client.close()
        
        # Verify session was closed
        mock_session.close.assert_called_once()