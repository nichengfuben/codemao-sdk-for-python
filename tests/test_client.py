"""
CodeMao 客户端测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from codemaokit import CodeMaoClient
from codemaokit.models import User, Board, Post
from codemaokit.exceptions import (
    AuthenticationError, APIError, ValidationError,
    ResourceNotFoundError, NetworkError
)


class TestCodeMaoClient:
    """测试CodeMao客户端"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return CodeMaoClient()
    
    @pytest.fixture
    def mock_response(self):
        """模拟响应"""
        def _create_mock_response(status_code=200, json_data=None, text=""):
            response = Mock()
            response.status_code = status_code
            response.text = text
            response.json.return_value = json_data or {}
            return response
        return _create_mock_response
    
    def test_client_initialization(self, client):
        """测试客户端初始化"""
        assert client.is_authenticated is False
        assert client.current_user is None
        assert client.auth_token is None
        assert client.timeout == 30
    
    def test_client_context_manager(self):
        """测试上下文管理器"""
        with CodeMaoClient() as client:
            assert isinstance(client, CodeMaoClient)
    
    @patch('requests.Session.request')
    def test_successful_login(self, mock_request, client, mock_response):
        """测试成功登录"""
        # 模拟登录响应
        login_response = {
            'auth': {
                'token': 'test_token',
                'phone_number': '13800138000',
                'email': 'test@example.com',
                'has_password': True,
                'is_weak_password': False
            },
            'user_info': {
                'id': 12345,
                'nickname': '测试用户',
                'avatar_url': 'https://example.com/avatar.jpg',
                'fullname': '测试全名',
                'birthday': 946656000,
                'sex': 1,
                'qq': '123456',
                'description': '测试描述'
            }
        }
        
        mock_request.return_value = mock_response(json_data=login_response)
        
        # 执行登录
        user = client.login("testuser", "testpass")
        
        # 验证结果
        assert client.is_authenticated is True
        assert client.auth_token == 'test_token'
        assert isinstance(user, User)
        assert user.nickname == '测试用户'
        assert user.id == 12345
    
    @patch('requests.Session.request')
    def test_failed_login_wrong_credentials(self, mock_request, client, mock_response):
        """测试登录失败 - 错误凭据"""
        error_response = {
            'error_number': 2,
            'error_message': '用户不存在或者密码错误'
        }
        
        mock_request.return_value = mock_response(status_code=400, json_data=error_response)
        
        with pytest.raises(AuthenticationError, match="用户不存在或密码错误"):
            client.login("wronguser", "wrongpass")
        
        assert client.is_authenticated is False
    
    @patch('requests.Session.request')
    def test_logout(self, mock_request, client, mock_response):
        """测试登出"""
        # 先登录
        login_response = {
            'auth': {'token': 'test_token'},
            'user_info': {'id': 12345, 'nickname': '测试用户'}
        }
        mock_request.return_value = mock_response(json_data=login_response)
        client.login("testuser", "testpass")
        
        # 模拟登出响应
        mock_request.return_value = mock_response(json_data={'success': True})
        
        # 执行登出
        client.logout()
        
        # 验证状态
        assert client.is_authenticated is False
        assert client.current_user is None
        assert client.auth_token is None
    
    @patch('requests.Session.request')
    def test_get_boards(self, mock_request, client, mock_response):
        """测试获取板块列表"""
        boards_response = {
            'items': [
                {
                    'id': '1',
                    'name': '技术讨论',
                    'icon_url': 'https://example.com/icon1.png',
                    'is_hot': True
                },
                {
                    'id': '2', 
                    'name': '新手入门',
                    'icon_url': 'https://example.com/icon2.png',
                    'is_hot': False
                }
            ]
        }
        
        mock_request.return_value = mock_response(json_data=boards_response)
        
        boards = client.get_boards()
        
        assert len(boards) == 2
        assert isinstance(boards[0], Board)
        assert boards[0].name == '技术讨论'
        assert boards[0].is_hot is True
    
    @patch('requests.Session.request')
    def test_get_board_by_id(self, mock_request, client, mock_response):
        """测试根据ID获取板块"""
        board_response = {
            'id': '1',
            'name': '技术讨论',
            'description': '技术相关讨论',
            'icon_url': 'https://example.com/icon.png',
            'is_hot': True,
            'n_posts': 100,
            'n_discussions': 50
        }
        
        mock_request.return_value = mock_response(json_data=board_response)
        
        board = client.get_board_by_id('1')
        
        assert isinstance(board, Board)
        assert board.id == '1'
        assert board.name == '技术讨论'
        assert board.n_posts == 100
    
    @patch('requests.Session.request')
    def test_create_post_success(self, mock_request, client, mock_response):
        """测试成功发布帖子"""
        # 先登录
        login_response = {
            'auth': {'token': 'test_token'},
            'user_info': {'id': 12345, 'nickname': '测试用户'}
        }
        mock_request.return_value = mock_response(json_data=login_response)
        client.login("testuser", "testpass")
        
        # 模拟板块信息
        board_response = {
            'id': '1',
            'name': '技术讨论',
            'icon_url': 'https://example.com/icon.png',
            'is_hot': True
        }
        mock_request.return_value = mock_response(json_data=board_response)
        
        # 模拟发布帖子响应
        post_response = {'id': 'post_123'}
        mock_request.return_value = mock_response(json_data=post_response)
        
        post_id = client.create_post(
            title="测试帖子标题",
            content="这是一个测试帖子内容，长度足够。",
            board_name="技术讨论"
        )
        
        assert post_id == 'post_123'
    
    def test_create_post_validation_errors(self, client):
        """测试发布帖子参数验证"""
        # 测试标题过短
        with pytest.raises(ValidationError, match="标题长度必须在5-50字之间"):
            client.create_post("短", "内容足够长", "板块")
        
        # 测试标题过长
        long_title = "a" * 51
        with pytest.raises(ValidationError, match="标题长度必须在5-50字之间"):
            client.create_post(long_title, "内容足够长", "板块")
        
        # 测试内容过短
        with pytest.raises(ValidationError, match="内容长度必须不少于10字"):
            client.create_post("有效标题", "短内容", "板块")
    
    def test_create_post_not_authenticated(self, client):
        """测试未登录时发布帖子"""
        with pytest.raises(AuthenticationError, match="请先登录"):
            client.create_post("标题", "内容足够长", "板块")
    
    @patch('requests.Session.request')
    def test_delete_post(self, mock_request, client, mock_response):
        """测试删除帖子"""
        # 先登录
        login_response = {
            'auth': {'token': 'test_token'},
            'user_info': {'id': 12345, 'nickname': '测试用户'}
        }
        mock_request.return_value = mock_response(json_data=login_response)
        client.login("testuser", "testpass")
        
        # 模拟删除响应
        mock_request.return_value = mock_response(json_data={'success': True})
        
        # 执行删除（不应该抛出异常）
        client.delete_post("post_123")
    
    @patch('requests.Session.request')
    def test_get_message_stats(self, mock_request, client, mock_response):
        """测试获取消息统计"""
        # 先登录
        login_response = {
            'auth': {'token': 'test_token'},
            'user_info': {'id': 12345, 'nickname': '测试用户'}
        }
        mock_request.return_value = mock_response(json_data=login_response)
        client.login("testuser", "testpass")
        
        # 模拟消息统计响应
        stats_response = [
            {'count': 5},  # comment_reply
            {'count': 3},  # like_fork  
            {'count': 2}   # system
        ]
        mock_request.return_value = mock_response(json_data=stats_response)
        
        stats = client.get_message_stats()
        
        assert stats.comment_reply == 5
        assert stats.like_fork == 3
        assert stats.system == 2
    
    @patch('requests.Session.request')
    def test_network_error(self, mock_request, client):
        """测试网络错误处理"""
        from requests.exceptions import ConnectionError
        mock_request.side_effect = ConnectionError("网络连接失败")
        
        with pytest.raises(NetworkError, match="网络请求失败"):
            client.login("testuser", "testpass")
    
    @patch('requests.Session.request')
    def test_api_rate_limit(self, mock_request, client, mock_response):
        """测试API频率限制"""
        mock_request.return_value = mock_response(status_code=429)
        
        with pytest.raises(CodeMaoError, match="请求过于频繁"):
            client.get_boards()
    
    @patch('requests.Session.request')
    def test_server_error(self, mock_request, client, mock_response):
        """测试服务器错误"""
        mock_request.return_value = mock_response(status_code=500)
        
        with pytest.raises(NetworkError, match="服务器错误"):
            client.get_boards()