"""
CodeMao 主客户端类
"""

import json
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import User, Board, Post, Work, MessageStats, UserHonor
from .exceptions import (
    CodeMaoError, AuthenticationError, APIError, 
    ValidationError, ResourceNotFoundError, NetworkError
)

logger = logging.getLogger(__name__)


class CodeMaoClient:
    """
    CodeMao SDK主客户端
    
    支持用户认证、帖子管理、作品操作等完整功能
    
    示例:
        >>> client = CodeMaoClient()
        >>> client.login("username", "password")
        >>> user = client.get_current_user()
        >>> print(f"欢迎 {user.nickname}!")
    """
    
    BASE_URL = "https://api.codemao.cn"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        初始化客户端
        
        Args:
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_session(max_retries)
        
        # 用户状态
        self.is_authenticated = False
        self.current_user: Optional[User] = None
        self.auth_token: Optional[str] = None
        self.cookies: Dict[str, str] = {}
        
        # 缓存
        self._boards_cache: Optional[List[Board]] = None
        
    def _setup_session(self, max_retries: int) -> None:
        """配置HTTP会话"""
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认请求头
        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[Dict[str, Any]] = None,
                 params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: 请求方法 (GET, POST, PATCH, DELETE)
            endpoint: API端点
            data: 请求数据
            params: URL参数
            
        Returns:
            API响应数据
            
        Raises:
            NetworkError: 网络连接失败
            APIError: API返回错误
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params,
                cookies=self.cookies,
                timeout=self.timeout
            )
            
            # 检查响应状态
            if response.status_code == 404:
                raise ResourceNotFoundError(f"资源不存在: {endpoint}")
            elif response.status_code == 401:
                self.is_authenticated = False
                raise AuthenticationError("认证失败，请重新登录")
            elif response.status_code == 429:
                raise CodeMaoError("请求过于频繁，请稍后再试")
            elif response.status_code >= 500:
                raise NetworkError(f"服务器错误: {response.status_code}")
            
            # 解析响应数据
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                raise APIError(f"无效的JSON响应: {response.text}")
            
            # 检查API错误
            if isinstance(response_data, dict):
                if response_data.get('error_code'):
                    error_msg = response_data.get('error_message', '未知错误')
                    error_code = response_data.get('error_code')
                    
                    if error_code == 'Not Found':
                        raise ResourceNotFoundError(error_msg)
                    elif '认证' in error_msg or '登录' in error_msg:
                        raise AuthenticationError(error_msg)
                    else:
                        raise APIError(error_msg, error_code, response_data)
                        
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络请求失败: {str(e)}")
    
    def login(self, identity: str, password: str) -> User:
        """
        用户登录
        
        Args:
            identity: 用户名、邮箱或手机号
            password: 密码
            
        Returns:
            当前用户对象
            
        Raises:
            AuthenticationError: 登录失败
        """
        login_data = {
            "identity": identity,
            "password": password,
            "pid": "65edCTyg"
        }
        
        try:
            response = self._request("POST", "/tiger/v3/web/accounts/login", login_data)
            
            # 保存认证信息
            self.cookies = self.session.cookies.get_dict()
            self.auth_token = response.get('auth', {}).get('token')
            self.is_authenticated = True
            
            # 创建用户对象
            user_info = response.get('user_info', {})
            self.current_user = User.from_dict(user_info)
            
            logger.info(f"用户 {self.current_user.nickname} 登录成功")
            return self.current_user
            
        except APIError as e:
            if e.error_code == 2:
                raise AuthenticationError("用户不存在或密码错误")
            raise AuthenticationError(f"登录失败: {e.message}")
    
    def logout(self) -> None:
        """用户登出"""
        if not self.is_authenticated:
            return
            
        try:
            self._request("POST", "/tiger/v3/web/accounts/logout")
        except Exception as e:
            logger.warning(f"登出时出错: {e}")
        finally:
            self.is_authenticated = False
            self.current_user = None
            self.auth_token = None
            self.cookies = {}
            self.session.cookies.clear()
            logger.info("用户已登出")
    
    def get_current_user(self) -> Optional[User]:
        """获取当前登录用户"""
        if not self.is_authenticated:
            return None
            
        if self.current_user:
            return self.current_user
            
        # 重新获取用户信息
        try:
            response = self._request("GET", "/api/user/info")
            user_data = response.get('data', {}).get('userInfo', {})
            self.current_user = User.from_dict(user_data)
            return self.current_user
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            return None
    
    def get_boards(self, refresh: bool = False) -> List[Board]:
        """
        获取所有论坛板块
        
        Args:
            refresh: 是否强制刷新缓存
            
        Returns:
            板块列表
        """
        if self._boards_cache and not refresh:
            return self._boards_cache
            
        try:
            response = self._request("GET", "/web/forums/boards/simples/all")
            boards_data = response.get('items', [])
            
            boards = [Board.from_dict(board_data) for board_data in boards_data]
            self._boards_cache = boards
            
            return boards
        except Exception as e:
            logger.error(f"获取板块列表失败: {e}")
            raise APIError(f"获取板块列表失败: {e}")
    
    def get_board_by_id(self, board_id: Union[str, int]) -> Board:
        """
        根据ID获取板块信息
        
        Args:
            board_id: 板块ID
            
        Returns:
            板块对象
        """
        try:
            response = self._request("GET", f"/web/forums/boards/{board_id}")
            return Board.from_dict(response)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"板块不存在: {board_id}")
        except Exception as e:
            logger.error(f"获取板块信息失败: {e}")
            raise APIError(f"获取板块信息失败: {e}")
    
    def get_board_by_name(self, board_name: str) -> Board:
        """
        根据名称获取板块信息
        
        Args:
            board_name: 板块名称
            
        Returns:
            板块对象
            
        Raises:
            ResourceNotFoundError: 板块不存在
        """
        boards = self.get_boards()
        
        for board in boards:
            if board.name == board_name:
                return self.get_board_by_id(board.id)
                
        raise ResourceNotFoundError(f"板块不存在: {board_name}")
    
    def create_post(self, title: str, content: str, 
                    board_name: str, studio_id: Optional[str] = None) -> str:
        """
        发布帖子
        
        Args:
            title: 帖子标题（5-50字）
            content: 帖子内容（最少10字）
            board_name: 板块名称
            studio_id: 工作室ID（可选）
            
        Returns:
            帖子ID
            
        Raises:
            ValidationError: 参数验证失败
            AuthenticationError: 未登录
        """
        if not self.is_authenticated:
            raise AuthenticationError("请先登录")
            
        # 参数验证
        if len(title) < 5 or len(title) > 50:
            raise ValidationError("标题长度必须在5-50字之间")
        if len(content) < 10:
            raise ValidationError("内容长度必须不少于10字")
            
        # 获取板块信息
        board = self.get_board_by_name(board_name)
        
        post_data = {
            "title": title,
            "content": content,
            "studio_id": studio_id
        }
        
        try:
            response = self._request("POST", f"/web/forums/boards/{board.id}/posts", post_data)
            post_id = response.get('id')
            
            if post_id:
                logger.info(f"用户 {self.current_user.nickname} 在板块 {board_name} 发布帖子成功")
                return str(post_id)
            else:
                raise APIError("发布帖子失败，未返回帖子ID")
                
        except APIError as e:
            if e.error_code == 'Param-Invalid@Common':
                raise ValidationError("请求参数验证失败")
            raise APIError(f"发布帖子失败: {e.message}")
    
    def delete_post(self, post_id: Union[str, int]) -> None:
        """
        删除帖子
        
        Args:
            post_id: 帖子ID
            
        Raises:
            AuthenticationError: 未登录
            ResourceNotFoundError: 帖子不存在
        """
        if not self.is_authenticated:
            raise AuthenticationError("请先登录")
            
        try:
            self._request("DELETE", f"/web/forums/posts/{post_id}")
            logger.info(f"用户 {self.current_user.nickname} 删除帖子 {post_id} 成功")
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"帖子不存在: {post_id}")
        except Exception as e:
            logger.error(f"删除帖子失败: {e}")
            raise APIError(f"删除帖子失败: {e}")
    
    def reply_to_post(self, post_id: Union[str, int], content: str) -> str:
        """
        回复帖子
        
        Args:
            post_id: 帖子ID
            content: 回复内容
            
        Returns:
            回复ID
        """
        if not self.is_authenticated:
            raise AuthenticationError("请先登录")
            
        reply_data = {"content": content}
        
        try:
            response = self._request("POST", f"/web/forums/posts/{post_id}/replies", reply_data)
            reply_id = response.get('id')
            
            if reply_id:
                logger.info(f"用户 {self.current_user.nickname} 回复帖子 {post_id} 成功")
                return str(reply_id)
            else:
                raise APIError("回复帖子失败，未返回回复ID")
                
        except APIError as e:
            raise APIError(f"回复帖子失败: {e.message}")
    
    def get_message_stats(self) -> MessageStats:
        """
        获取消息统计
        
        Returns:
            消息统计对象
        """
        if not self.is_authenticated:
            raise AuthenticationError("请先登录")
            
        try:
            response = self._request("GET", "/web/message-record/count")
            return MessageStats.from_dict(response)
        except Exception as e:
            logger.error(f"获取消息统计失败: {e}")
            raise APIError(f"获取消息统计失败: {e}")
    
    def update_user_info(self, **kwargs) -> None:
        """
        更新用户信息
        
        Args:
            **kwargs: 要更新的字段（nickname, fullname, description, sex, birthday, avatar_url）
            
        Raises:
            AuthenticationError: 未登录
            ValidationError: 参数验证失败
        """
        if not self.is_authenticated:
            raise AuthenticationError("请先登录")
            
        # 验证参数
        valid_fields = {'nickname', 'fullname', 'description', 'sex', 'birthday', 'avatar_url'}
        invalid_fields = set(kwargs.keys()) - valid_fields
        if invalid_fields:
            raise ValidationError(f"无效的字段: {invalid_fields}")
        
        # 更新每个字段
        for field, value in kwargs.items():
            try:
                self._request("PATCH", f"/tiger/v3/web/accounts/{field}", {field: value})
                logger.info(f"用户 {self.current_user.nickname} 更新 {field} 成功")
            except APIError as e:
                if e.error_code == 5:
                    raise ValidationError(f"字段 {field} 格式错误")
                raise APIError(f"更新 {field} 失败: {e.message}")
    
    def __enter__(self):
        """上下文管理器支持"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器清理"""
        self.logout()