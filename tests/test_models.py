"""
数据模型测试
"""

import pytest
from datetime import datetime
from codemaokit.models import User, Board, Post, Work, MessageStats, UserHonor


class TestUser:
    """测试用户模型"""
    
    def test_user_creation(self):
        """测试用户创建"""
        user = User(
            id=12345,
            nickname="测试用户",
            avatar_url="https://example.com/avatar.jpg",
            fullname="测试全名",
            birthday=946656000,
            sex=1,
            qq="123456",
            description="测试描述"
        )
        
        assert user.id == 12345
        assert user.nickname == "测试用户"
        assert user.avatar_url == "https://example.com/avatar.jpg"
        assert user.fullname == "测试全名"
        assert user.birthday == 946656000
        assert user.sex == 1
        assert user.qq == "123456"
        assert user.description == "测试描述"
    
    def test_user_from_dict(self):
        """测试从字典创建用户"""
        data = {
            'id': 12345,
            'nickname': '测试用户',
            'avatar_url': 'https://example.com/avatar.jpg',
            'fullname': '测试全名',
            'birthday': 946656000,
            'sex': 1,
            'qq': '123456',
            'description': '测试描述'
        }
        
        user = User.from_dict(data)
        
        assert user.id == 12345
        assert user.nickname == "测试用户"
        assert user.avatar_url == "https://example.com/avatar.jpg"
    
    def test_user_from_dict_missing_fields(self):
        """测试从字典创建用户 - 缺少字段"""
        data = {
            'id': 12345,
            'nickname': '测试用户'
            # 缺少其他字段
        }
        
        user = User.from_dict(data)
        
        assert user.id == 12345
        assert user.nickname == "测试用户"
        assert user.avatar_url is None
        assert user.fullname is None
        assert user.birthday is None


class TestBoard:
    """测试板块模型"""
    
    def test_board_creation(self):
        """测试板块创建"""
        board = Board(
            id="1",
            name="技术讨论",
            description="技术相关讨论",
            icon_url="https://example.com/icon.png",
            is_hot=True,
            n_posts=100,
            n_discussions=50
        )
        
        assert board.id == "1"
        assert board.name == "技术讨论"
        assert board.description == "技术相关讨论"
        assert board.icon_url == "https://example.com/icon.png"
        assert board.is_hot is True
        assert board.n_posts == 100
        assert board.n_discussions == 50
    
    def test_board_from_dict(self):
        """测试从字典创建板块"""
        data = {
            'id': '1',
            'name': '技术讨论',
            'description': '技术相关讨论',
            'icon_url': 'https://example.com/icon.png',
            'is_hot': True,
            'n_posts': 100,
            'n_discussions': 50
        }
        
        board = Board.from_dict(data)
        
        assert board.id == "1"
        assert board.name == "技术讨论"
        assert board.description == "技术相关讨论"
        assert board.is_hot is True


class TestPost:
    """测试帖子模型"""
    
    def test_post_creation(self):
        """测试帖子创建"""
        post = Post(
            id="post_123",
            title="测试帖子标题",
            content="这是一个测试帖子内容",
            author_id=12345,
            author_nickname="测试用户",
            board_id="1",
            board_name="技术讨论",
            created_at=1609459200,
            updated_at=1609459200,
            likes=10,
            replies=5,
            views=100
        )
        
        assert post.id == "post_123"
        assert post.title == "测试帖子标题"
        assert post.content == "这是一个测试帖子内容"
        assert post.author_id == 12345
        assert post.author_nickname == "测试用户"
        assert post.board_id == "1"
        assert post.board_name == "技术讨论"
        assert post.created_at == 1609459200
        assert post.updated_at == 1609459200
        assert post.likes == 10
        assert post.replies == 5
        assert post.views == 100
    
    def test_post_from_dict(self):
        """测试从字典创建帖子"""
        data = {
            'id': 'post_123',
            'title': '测试帖子标题',
            'content': '这是一个测试帖子内容',
            'author_id': 12345,
            'author_nickname': '测试用户',
            'board_id': '1',
            'board_name': '技术讨论',
            'created_at': 1609459200,
            'updated_at': 1609459200,
            'likes': 10,
            'replies': 5,
            'views': 100
        }
        
        post = Post.from_dict(data)
        
        assert post.id == "post_123"
        assert post.title == "测试帖子标题"
        assert post.author_nickname == "测试用户"


class TestWork:
    """测试作品模型"""
    
    def test_work_creation(self):
        """测试作品创建"""
        work = Work(
            id="work_123",
            title="测试作品",
            description="这是一个测试作品",
            author_id=12345,
            author_nickname="测试用户",
            type="game",
            thumbnail_url="https://example.com/thumb.jpg",
            view_count=1000,
            like_count=50,
            fork_count=10,
            created_at=1609459200,
            updated_at=1609459200
        )
        
        assert work.id == "work_123"
        assert work.title == "测试作品"
        assert work.description == "这是一个测试作品"
        assert work.author_id == 12345
        assert work.author_nickname == "测试用户"
        assert work.type == "game"
        assert work.thumbnail_url == "https://example.com/thumb.jpg"
        assert work.view_count == 1000
        assert work.like_count == 50
        assert work.fork_count == 10
        assert work.created_at == 1609459200
        assert work.updated_at == 1609459200
    
    def test_work_from_dict(self):
        """测试从字典创建作品"""
        data = {
            'id': 'work_123',
            'title': '测试作品',
            'description': '这是一个测试作品',
            'author_id': 12345,
            'author_nickname': '测试用户',
            'type': 'game',
            'thumbnail_url': 'https://example.com/thumb.jpg',
            'view_count': 1000,
            'like_count': 50,
            'fork_count': 10,
            'created_at': 1609459200,
            'updated_at': 1609459200
        }
        
        work = Work.from_dict(data)
        
        assert work.id == "work_123"
        assert work.title == "测试作品"
        assert work.type == "game"


class TestMessageStats:
    """测试消息统计模型"""
    
    def test_message_stats_creation(self):
        """测试消息统计创建"""
        stats = MessageStats(
            comment_reply=5,
            like_fork=3,
            system=2
        )
        
        assert stats.comment_reply == 5
        assert stats.like_fork == 3
        assert stats.system == 2
        assert stats.total == 10
    
    def test_message_stats_from_dict(self):
        """测试从字典创建消息统计"""
        data = [
            {'count': 5},  # comment_reply
            {'count': 3},  # like_fork
            {'count': 2}   # system
        ]
        
        stats = MessageStats.from_dict(data)
        
        assert stats.comment_reply == 5
        assert stats.like_fork == 3
        assert stats.system == 2
        assert stats.total == 10
    
    def test_message_stats_empty_data(self):
        """测试空数据的消息统计"""
        data = []
        
        stats = MessageStats.from_dict(data)
        
        assert stats.comment_reply == 0
        assert stats.like_fork == 0
        assert stats.system == 0
        assert stats.total == 0


class TestUserHonor:
    """测试用户荣誉模型"""
    
    def test_user_honor_creation(self):
        """测试用户荣誉创建"""
        honor = UserHonor(
            id="honor_123",
            name="优秀创作者",
            description="创作了大量优秀作品",
            icon_url="https://example.com/honor.png",
            level=1,
            obtained_at=1609459200
        )
        
        assert honor.id == "honor_123"
        assert honor.name == "优秀创作者"
        assert honor.description == "创作了大量优秀作品"
        assert honor.icon_url == "https://example.com/honor.png"
        assert honor.level == 1
        assert honor.obtained_at == 1609459200
    
    def test_user_honor_from_dict(self):
        """测试从字典创建用户荣誉"""
        data = {
            'id': 'honor_123',
            'name': '优秀创作者',
            'description': '创作了大量优秀作品',
            'icon_url': 'https://example.com/honor.png',
            'level': 1,
            'obtained_at': 1609459200
        }
        
        honor = UserHonor.from_dict(data)
        
        assert honor.id == "honor_123"
        assert honor.name == "优秀创作者"
        assert honor.level == 1