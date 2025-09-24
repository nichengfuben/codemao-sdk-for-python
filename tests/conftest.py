"""Test configuration and fixtures for PyCodeMao."""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock
import logging

from pycodemao import CodeMaoClient
from pycodemao.models import User, Work, Post, ForumBoard


# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[CodeMaoClient, None]:
    """Create a test client."""
    client = CodeMaoClient(
        base_url="https://api.test.codemao.cn",
        enable_logging=True,
        log_level="DEBUG"
    )
    yield client
    await client.close()


@pytest.fixture
def mock_user() -> User:
    """Create a mock user for testing."""
    return User(
        id="123e4567-e89b-12d3-a456-426614174000",
        username="testuser",
        nickname="Test User",
        email="test@example.com",
        level=5,
        coins=100,
        diamonds=50,
        followers_count=25,
        following_count=15,
        works_count=10,
        posts_count=5,
        created_at="2023-01-01T00:00:00Z",
        is_verified=True,
        is_premium=False
    )


@pytest.fixture
def mock_work() -> Work:
    """Create a mock work for testing."""
    return Work(
        id="223e4567-e89b-12d3-a456-426614174000",
        title="Test Work",
        description="A test work for unit testing",
        author=mock_user(),
        language="python",
        tags=["test", "python", "demo"],
        likes_count=15,
        comments_count=3,
        collections_count=8,
        views_count=150,
        is_public=True,
        is_featured=False,
        created_at="2023-01-15T10:30:00Z"
    )


@pytest.fixture
def mock_post() -> Post:
    """Create a mock post for testing."""
    return Post(
        id="323e4567-e89b-12d3-a456-426614174000",
        title="Test Post",
        content="This is a test post content for unit testing.",
        author=mock_user(),
        board=mock_board(),
        likes_count=10,
        comments_count=5,
        views_count=100,
        tags=["discussion", "help"],
        created_at="2023-01-20T14:20:00Z"
    )


@pytest.fixture
def mock_board() -> ForumBoard:
    """Create a mock forum board for testing."""
    return ForumBoard(
        id="423e4567-e89b-12d3-a456-426614174000",
        name="Test Board",
        description="A test forum board",
        category="General",
        posts_count=50,
        is_active=True,
        created_at="2023-01-01T00:00:00Z"
    )


@pytest.fixture
def mock_response() -> dict:
    """Create a mock API response."""
    return {
        "success": True,
        "code": 200,
        "message": "Success",
        "data": {},
        "timestamp": "2023-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_paginated_response() -> dict:
    """Create a mock paginated response."""
    return {
        "items": [],
        "total": 0,
        "page": 1,
        "per_page": 20,
        "total_pages": 0,
        "has_next": False,
        "has_prev": False
    }


@pytest.fixture
def mock_session() -> AsyncMock:
    """Create a mock aiohttp session."""
    session = AsyncMock()
    session.closed = False
    session.request = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_response_obj() -> AsyncMock:
    """Create a mock response object."""
    response = AsyncMock()
    response.status = 200
    response.json = AsyncMock(return_value={
        "success": True,
        "code": 200,
        "message": "Success",
        "data": {}
    })
    response.text = AsyncMock(return_value='{"success": true}')
    response.headers = {}
    return response