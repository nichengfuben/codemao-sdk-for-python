"""Unit tests for models."""

import pytest
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import ValidationError

from pycodemao.models import User, Work, Post, ForumBoard, APIResponse, PaginatedResponse


class TestUser:
    """Test cases for User model."""
    
    def test_user_creation_valid(self):
        """Test creating a valid user."""
        user = User(
            id=uuid4(),
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
            created_at=datetime.now(),
            is_verified=True,
            is_premium=False
        )
        
        assert user.username == "testuser"
        assert user.nickname == "Test User"
        assert user.email == "test@example.com"
        assert user.level == 5
        assert user.is_verified is True
    
    def test_user_username_validation(self):
        """Test username validation."""
        # Valid usernames
        valid_usernames = ["user123", "test_user", "a1b2c3", "x" * 20]
        for username in valid_usernames:
            user = User(
                id=uuid4(),
                username=username,
                nickname="Test User",
                created_at=datetime.now()
            )
            assert user.username == username
        
        # Invalid usernames
        invalid_usernames = ["ab", "x" * 21, "user@123", "test-user", "user space"]
        for username in invalid_usernames:
            with pytest.raises(ValidationError):
                User(
                    id=uuid4(),
                    username=username,
                    nickname="Test User",
                    created_at=datetime.now()
                )
    
    def test_user_nickname_validation(self):
        """Test nickname validation."""
        # Valid nickname
        valid_nickname = "x" * 50
        user = User(
            id=uuid4(),
            username="testuser",
            nickname=valid_nickname,
            created_at=datetime.now()
        )
        assert user.nickname == valid_nickname
        
        # Invalid nickname (too long)
        with pytest.raises(ValidationError):
            User(
                id=uuid4(),
                username="testuser",
                nickname="x" * 51,
                created_at=datetime.now()
            )
    
    def test_user_optional_fields(self):
        """Test user with optional fields."""
        user = User(
            id=uuid4(),
            username="minimal",
            nickname="Minimal User",
            created_at=datetime.now()
        )
        
        # Check defaults
        assert user.level == 1
        assert user.coins == 0
        assert user.diamonds == 0
        assert user.followers_count == 0
        assert user.following_count == 0
        assert user.works_count == 0
        assert user.posts_count == 0
        assert user.is_verified is False
        assert user.is_premium is False
        assert user.email is None
        assert user.avatar is None
        assert user.bio is None


class TestWork:
    """Test cases for Work model."""
    
    def test_work_creation_valid(self):
        """Test creating a valid work."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        work = Work(
            id=uuid4(),
            title="Test Work",
            description="A test work",
            author=user,
            language="python",
            tags=["test", "python", "demo"],
            likes_count=15,
            comments_count=3,
            collections_count=8,
            views_count=150,
            is_public=True,
            is_featured=False,
            created_at=datetime.now()
        )
        
        assert work.title == "Test Work"
        assert work.description == "A test work"
        assert work.author == user
        assert work.language == "python"
        assert work.tags == ["test", "python", "demo"]
        assert work.likes_count == 15
        assert work.is_public is True
        assert work.is_featured is False
    
    def test_work_title_validation(self):
        """Test work title validation."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        # Valid titles
        valid_titles = ["A", "x" * 100]
        for title in valid_titles:
            work = Work(
                id=uuid4(),
                title=title,
                author=user,
                created_at=datetime.now()
            )
            assert work.title == title
        
        # Invalid titles
        invalid_titles = ["", "x" * 101]
        for title in invalid_titles:
            with pytest.raises(ValidationError):
                Work(
                    id=uuid4(),
                    title=title,
                    author=user,
                    created_at=datetime.now()
                )
    
    def test_work_optional_fields(self):
        """Test work with minimal fields."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        work = Work(
            id=uuid4(),
            title="Minimal Work",
            author=user,
            created_at=datetime.now()
        )
        
        # Check defaults
        assert work.description is None
        assert work.thumbnail is None
        assert work.content is None
        assert work.language is None
        assert work.tags == []
        assert work.likes_count == 0
        assert work.comments_count == 0
        assert work.collections_count == 0
        assert work.views_count == 0
        assert work.is_public is True
        assert work.is_featured is False
        assert work.updated_at is None


class TestPost:
    """Test cases for Post model."""
    
    def test_post_creation_valid(self):
        """Test creating a valid post."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        board = ForumBoard(
            id=uuid4(),
            name="Test Board",
            category="General",
            created_at=datetime.now()
        )
        
        post = Post(
            id=uuid4(),
            title="Test Post",
            content="This is a test post content.",
            author=user,
            board=board,
            is_pinned=False,
            is_locked=False,
            likes_count=10,
            comments_count=5,
            views_count=100,
            tags=["discussion", "help"],
            created_at=datetime.now()
        )
        
        assert post.title == "Test Post"
        assert post.content == "This is a test post content."
        assert post.author == user
        assert post.board == board
        assert post.is_pinned is False
        assert post.is_locked is False
        assert post.likes_count == 10
        assert post.tags == ["discussion", "help"]
    
    def test_post_title_validation(self):
        """Test post title validation."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        board = ForumBoard(
            id=uuid4(),
            name="Test Board",
            category="General",
            created_at=datetime.now()
        )
        
        # Valid titles
        valid_titles = ["A", "x" * 200]
        for title in valid_titles:
            post = Post(
                id=uuid4(),
                title=title,
                content="Content",
                author=user,
                board=board,
                created_at=datetime.now()
            )
            assert post.title == title
        
        # Invalid titles
        invalid_titles = ["", "x" * 201]
        for title in invalid_titles:
            with pytest.raises(ValidationError):
                Post(
                    id=uuid4(),
                    title=title,
                    content="Content",
                    author=user,
                    board=board,
                    created_at=datetime.now()
                )
    
    def test_post_content_validation(self):
        """Test post content validation."""
        user = User(
            id=uuid4(),
            username="author",
            nickname="Author Name",
            created_at=datetime.now()
        )
        
        board = ForumBoard(
            id=uuid4(),
            name="Test Board",
            category="General",
            created_at=datetime.now()
        )
        
        # Valid content
        valid_content = ["A", "x" * 10000]
        for content in valid_content:
            post = Post(
                id=uuid4(),
                title="Title",
                content=content,
                author=user,
                board=board,
                created_at=datetime.now()
            )
            assert post.content == content
        
        # Invalid content
        invalid_content = ["", "x" * 10001]
        for content in invalid_content:
            with pytest.raises(ValidationError):
                Post(
                    id=uuid4(),
                    title="Title",
                    content=content,
                    author=user,
                    board=board,
                    created_at=datetime.now()
                )


class TestForumBoard:
    """Test cases for ForumBoard model."""
    
    def test_forum_board_creation_valid(self):
        """Test creating a valid forum board."""
        board = ForumBoard(
            id=uuid4(),
            name="Test Board",
            description="A test board",
            category="General",
            posts_count=50,
            is_active=True,
            created_at=datetime.now()
        )
        
        assert board.name == "Test Board"
        assert board.description == "A test board"
        assert board.category == "General"
        assert board.posts_count == 50
        assert board.is_active is True
    
    def test_forum_board_name_validation(self):
        """Test forum board name validation."""
        # Valid names
        valid_names = ["A", "x" * 50]
        for name in valid_names:
            board = ForumBoard(
                id=uuid4(),
                name=name,
                category="General",
                created_at=datetime.now()
            )
            assert board.name == name
        
        # Invalid names
        invalid_names = ["", "x" * 51]
        for name in invalid_names:
            with pytest.raises(ValidationError):
                ForumBoard(
                    id=uuid4(),
                    name=name,
                    category="General",
                    created_at=datetime.now()
                )
    
    def test_forum_board_optional_fields(self):
        """Test forum board with minimal fields."""
        board = ForumBoard(
            id=uuid4(),
            name="Minimal Board",
            category="General",
            created_at=datetime.now()
        )
        
        # Check defaults
        assert board.description is None
        assert board.posts_count == 0
        assert board.moderators == []
        assert board.is_active is True


class TestAPIResponse:
    """Test cases for APIResponse model."""
    
    def test_api_response_valid(self):
        """Test creating a valid API response."""
        response = APIResponse(
            success=True,
            code=200,
            message="Success",
            data={"key": "value"}
        )
        
        assert response.success is True
        assert response.code == 200
        assert response.message == "Success"
        assert response.data == {"key": "value"}
        assert isinstance(response.timestamp, datetime)
    
    def test_api_response_minimal(self):
        """Test creating minimal API response."""
        response = APIResponse(
            success=False,
            code=400,
            message="Bad Request"
        )
        
        assert response.success is False
        assert response.code == 400
        assert response.message == "Bad Request"
        assert response.data is None


class TestPaginatedResponse:
    """Test cases for PaginatedResponse model."""
    
    def test_paginated_response_valid(self):
        """Test creating a valid paginated response."""
        response = PaginatedResponse(
            items=[{"id": 1}, {"id": 2}],
            total=2,
            page=1,
            per_page=20,
            total_pages=1,
            has_next=False,
            has_prev=False
        )
        
        assert len(response.items) == 2
        assert response.total == 2
        assert response.page == 1
        assert response.per_page == 20
        assert response.total_pages == 1
        assert response.has_next is False
        assert response.has_prev is False
    
    def test_paginated_response_empty(self):
        """Test creating empty paginated response."""
        response = PaginatedResponse(
            items=[],
            total=0,
            page=1,
            per_page=20,
            total_pages=0,
            has_next=False,
            has_prev=False
        )
        
        assert len(response.items) == 0
        assert response.total == 0
        assert response.total_pages == 0


class TestModelSerialization:
    """Test model serialization and deserialization."""
    
    def test_user_serialization(self, mock_user):
        """Test user model serialization."""
        user_dict = mock_user.dict()
        
        assert isinstance(user_dict, dict)
        assert user_dict["username"] == "testuser"
        assert user_dict["nickname"] == "Test User"
        assert user_dict["level"] == 5
    
    def test_user_json_serialization(self, mock_user):
        """Test user model JSON serialization."""
        user_json = mock_user.json()
        
        assert isinstance(user_json, str)
        assert "testuser" in user_json
        assert "Test User" in user_json
    
    def test_model_from_dict(self):
        """Test creating model from dictionary."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "dictuser",
            "nickname": "Dict User",
            "email": "dict@example.com",
            "level": 3,
            "coins": 50,
            "created_at": "2023-01-01T00:00:00Z"
        }
        
        user = User(**user_data)
        
        assert user.username == "dictuser"
        assert user.nickname == "Dict User"
        assert user.level == 3
        assert user.coins == 50