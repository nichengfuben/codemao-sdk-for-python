"""
CodeMao SDK 工具函数
"""

import re
from typing import Optional, Union
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        是否有效
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 手机号
        
    Returns:
        是否有效
    """
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_username(username: str) -> bool:
    """
    验证用户名格式
    
    Args:
        username: 用户名
        
    Returns:
        是否有效
    """
    # 用户名：3-20个字符，支持字母、数字、下划线
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None


def validate_password(password: str) -> bool:
    """
    验证密码强度
    
    Args:
        password: 密码
        
    Returns:
        是否有效（至少6位）
    """
    return len(password) >= 6


def validate_post_title(title: str) -> Optional[str]:
    """
    验证帖子标题
    
    Args:
        title: 标题
        
    Returns:
        错误信息，如果有效返回None
    """
    if len(title) < 5:
        return "标题长度不能少于5个字符"
    if len(title) > 50:
        return "标题长度不能超过50个字符"
    return None


def validate_post_content(content: str) -> Optional[str]:
    """
    验证帖子内容
    
    Args:
        content: 内容
        
    Returns:
        错误信息，如果有效返回None
    """
    if len(content) < 10:
        return "内容长度不能少于10个字符"
    if len(content) > 10000:
        return "内容长度不能超过10000个字符"
    return None


def validate_nickname(nickname: str) -> Optional[str]:
    """
    验证用户昵称
    
    Args:
        nickname: 昵称
        
    Returns:
        错误信息，如果有效返回None
    """
    if len(nickname) < 2:
        return "昵称长度不能少于2个字符"
    if len(nickname) > 20:
        return "昵称长度不能超过20个字符"
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\-]+$', nickname):
        return "昵称只能包含中文、字母、数字、下划线和连字符"
    return None


def timestamp_to_datetime(timestamp: Union[int, float]) -> datetime:
    """
    时间戳转datetime
    
    Args:
        timestamp: 时间戳（秒或毫秒）
        
    Returns:
        datetime对象
    """
    # 如果是毫秒时间戳，转换为秒
    if timestamp > 1e10:
        timestamp = timestamp / 1000
    
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt: datetime) -> int:
    """
    datetime转时间戳
    
    Args:
        dt: datetime对象
        
    Returns:
        时间戳（秒）
    """
    return int(dt.timestamp())


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的字符串
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    截断文本
    
    Args:
        text: 原文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def clean_html_tags(html_text: str) -> str:
    """
    清除HTML标签
    
    Args:
        html_text: 包含HTML的文本
        
    Returns:
        纯文本
    """
    clean_pattern = re.compile('<.*?>')
    return re.sub(clean_pattern, '', html_text)


def is_valid_work_type(work_type: int) -> bool:
    """
    验证作品类型是否有效
    
    Args:
        work_type: 作品类型ID
        
    Returns:
        是否有效
    """
    # 编程猫常见的作品类型
    valid_types = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    return work_type in valid_types