"""
CodeMao 数据模型定义
"""

from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """用户模型"""
    id: int
    nickname: str
    avatar_url: str
    fullname: str = ""
    birthday: Optional[int] = None
    sex: int = 0
    qq: str = ""
    description: str = ""
    email: str = ""
    gold: int = 0
    level: int = 0
    username: str = ""
    doing: str = ""
    real_name: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """从字典创建用户实例"""
        return cls(
            id=data.get('id', 0),
            nickname=data.get('nickname', ''),
            avatar_url=data.get('avatar_url', data.get('avatar', '')),
            fullname=data.get('fullname', ''),
            birthday=data.get('birthday'),
            sex=data.get('sex', 0),
            qq=data.get('qq', ''),
            description=data.get('description', ''),
            email=data.get('email', ''),
            gold=data.get('gold', 0),
            level=data.get('level', 0),
            username=data.get('username', ''),
            doing=data.get('doing', ''),
            real_name=data.get('real_name', '')
        )


@dataclass
class Board:
    """论坛板块模型"""
    id: str
    name: str
    icon_url: str
    is_hot: bool = False
    description: str = ""
    n_posts: int = 0
    n_discussions: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Board":
        """从字典创建板块实例"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            icon_url=data.get('icon_url', ''),
            is_hot=data.get('is_hot', False),
            description=data.get('description', ''),
            n_posts=data.get('n_posts', 0),
            n_discussions=data.get('n_discussions', 0)
        )


@dataclass
class Post:
    """帖子模型"""
    id: str
    title: str
    content: str
    board_id: str
    studio_id: Optional[str] = None
    author_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Post":
        """从字典创建帖子实例"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            content=data.get('content', ''),
            board_id=data.get('board_id', ''),
            studio_id=data.get('studio_id'),
            author_id=data.get('author_id'),
            created_at=datetime.fromtimestamp(data.get('created_at', 0)) if data.get('created_at') else None
        )


@dataclass
class Work:
    """作品模型"""
    id: int
    name: str
    preview: str
    type: int
    view_times: int = 0
    collect_times: int = 0
    liked_times: int = 0
    fork_times: int = 0
    publish_time: int = 0
    description: str = ""
    fork_enable: bool = True
    parent_id: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Work":
        """从字典创建作品实例"""
        return cls(
            id=data.get('id', 0),
            name=data.get('work_name', data.get('name', '')),
            preview=data.get('preview', ''),
            type=data.get('type', 0),
            view_times=data.get('view_times', 0),
            collect_times=data.get('collect_times', 0),
            liked_times=data.get('liked_times', 0),
            fork_times=data.get('fork_times', 0),
            publish_time=data.get('publish_time', 0),
            description=data.get('description', ''),
            fork_enable=data.get('fork_enable', True),
            parent_id=data.get('parent_id', 0)
        )


@dataclass
class MessageStats:
    """消息统计模型"""
    comment_reply: int
    like_fork: int
    system: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageStats":
        """从字典创建消息统计实例"""
        return cls(
            comment_reply=data.get('comment_reply', 0),
            like_fork=data.get('like_fork', 0),
            system=data.get('system', 0)
        )


@dataclass
class UserHonor:
    """用户荣誉信息模型"""
    attention_status: bool = False
    block_total: int = 0
    re_created_total: int = 0
    attention_total: int = 0
    fans_total: int = 0
    collected_total: int = 0
    liked_total: int = 0
    view_times: int = 0
    author_level: int = 0
    is_official_certification: bool = False
    subject_id: int = 0
    work_shop_name: str = ""
    work_shop_level: int = 0
    like_score: int = 0
    collect_score: int = 0
    fork_score: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserHonor":
        """从字典创建用户荣誉实例"""
        return cls(
            attention_status=data.get('attention_status', False),
            block_total=data.get('block_total', 0),
            re_created_total=data.get('re_created_total', 0),
            attention_total=data.get('attention_total', 0),
            fans_total=data.get('fans_total', 0),
            collected_total=data.get('collected_total', 0),
            liked_total=data.get('liked_total', 0),
            view_times=data.get('view_times', 0),
            author_level=data.get('author_level', 0),
            is_official_certification=data.get('is_official_certification', False),
            subject_id=data.get('subject_id', 0),
            work_shop_name=data.get('work_shop_name', ''),
            work_shop_level=data.get('work_shop_level', 0),
            like_score=data.get('like_score', 0),
            collect_score=data.get('collect_score', 0),
            fork_score=data.get('fork_score', 0)
        )