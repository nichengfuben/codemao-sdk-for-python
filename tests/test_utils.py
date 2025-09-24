"""
工具函数测试
"""

import pytest
from datetime import datetime
from codemaokit.utils import (
    validate_email, validate_phone, validate_username,
    validate_password, validate_post_title, validate_post_content,
    validate_nickname, timestamp_to_datetime, format_file_size,
    truncate_text, strip_html_tags, validate_work_type
)


class TestValidation:
    """测试验证函数"""
    
    def test_validate_email_valid(self):
        """测试有效的邮箱地址"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.com",
            "user+tag@example.co.uk",
            "123@example.com",
            "test_email@subdomain.example.com"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"邮箱应该有效: {email}"
    
    def test_validate_email_invalid(self):
        """测试无效的邮箱地址"""
        invalid_emails = [
            "invalid.email",  # 缺少@
            "@example.com",   # 缺少用户名
            "test@",          # 缺少域名
            "test @example.com", # 空格
            "test@example",    # 缺少顶级域名
            "",               # 空字符串
            None              # None值
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False, f"邮箱应该无效: {email}"
    
    def test_validate_phone_valid(self):
        """测试有效的手机号"""
        valid_phones = [
            "13800138000",
            "15912345678",
            "17612345678",
            "19912345678"
        ]
        
        for phone in valid_phones:
            assert validate_phone(phone) is True, f"手机号应该有效: {phone}"
    
    def test_validate_phone_invalid(self):
        """测试无效的手机号"""
        invalid_phones = [
            "1380013800",     # 少一位
            "138001380000",   # 多一位
            "23800138000",    # 无效号段
            "1380013800a",    # 包含字母
            "138-0013-8000",  # 包含特殊字符
            "",               # 空字符串
            None              # None值
        ]
        
        for phone in invalid_phones:
            assert validate_phone(phone) is False, f"手机号应该无效: {phone}"
    
    def test_validate_username_valid(self):
        """测试有效的用户名"""
        valid_usernames = [
            "testuser",
            "user123",
            "test_user",
            "user.name",
            "a",              # 最小长度
            "a" * 20          # 最大长度
        ]
        
        for username in valid_usernames:
            assert validate_username(username) is True, f"用户名应该有效: {username}"
    
    def test_validate_username_invalid(self):
        """测试无效的用户名"""
        invalid_usernames = [
            "",               # 空字符串
            "a" * 21,         # 超过最大长度
            "test user",      # 包含空格
            "test@user",      # 包含特殊字符
            "TestUser",       # 包含大写字母
            "123user",        # 以数字开头
            None              # None值
        ]
        
        for username in invalid_usernames:
            assert validate_username(username) is False, f"用户名应该无效: {username}"
    
    def test_validate_password_valid(self):
        """测试有效的密码"""
        valid_passwords = [
            "password123",
            "test_password",
            "123456",
            "a" * 6,          # 最小长度
            "a" * 20          # 最大长度
        ]
        
        for password in valid_passwords:
            assert validate_password(password) is True, f"密码应该有效: {password}"
    
    def test_validate_password_invalid(self):
        """测试无效的密码"""
        invalid_passwords = [
            "",               # 空字符串
            "a" * 5,          # 小于最小长度
            "a" * 21,         # 超过最大长度
            "pass word",      # 包含空格
            None              # None值
        ]
        
        for password in invalid_passwords:
            assert validate_password(password) is False, f"密码应该无效: {password}"
    
    def test_validate_post_title_valid(self):
        """测试有效的帖子标题"""
        valid_titles = [
            "这是一个有效的标题",
            "测试标题",
            "a" * 5,          # 最小长度
            "a" * 50          # 最大长度
        ]
        
        for title in valid_titles:
            assert validate_post_title(title) is True, f"帖子标题应该有效: {title}"
    
    def test_validate_post_title_invalid(self):
        """测试无效的帖子标题"""
        invalid_titles = [
            "",               # 空字符串
            "a" * 4,          # 小于最小长度
            "a" * 51,         # 超过最大长度
            None              # None值
        ]
        
        for title in invalid_titles:
            assert validate_post_title(title) is False, f"帖子标题应该无效: {title}"
    
    def test_validate_post_content_valid(self):
        """测试有效的帖子内容"""
        valid_contents = [
            "这是一个足够长的帖子内容，应该通过验证",
            "测试内容测试内容测试内容测试内容",
            "a" * 10,         # 最小长度
            "a" * 1000        # 最大长度
        ]
        
        for content in valid_contents:
            assert validate_post_content(content) is True, f"帖子内容应该有效: {content}"
    
    def test_validate_post_content_invalid(self):
        """测试无效的帖子内容"""
        invalid_contents = [
            "",               # 空字符串
            "a" * 9,          # 小于最小长度
            "a" * 1001,       # 超过最大长度
            None              # None值
        ]
        
        for content in invalid_contents:
            assert validate_post_content(content) is False, f"帖子内容应该无效: {content}"
    
    def test_validate_nickname_valid(self):
        """测试有效的昵称"""
        valid_nicknames = [
            "测试用户",
            "user123",
            "test_user",
            "a",              # 最小长度
            "a" * 20          # 最大长度
        ]
        
        for nickname in valid_nicknames:
            assert validate_nickname(nickname) is True, f"昵称应该有效: {nickname}"
    
    def test_validate_nickname_invalid(self):
        """测试无效的昵称"""
        invalid_nicknames = [
            "",               # 空字符串
            "a" * 21,         # 超过最大长度
            "test user",      # 包含空格
            "test@user",      # 包含特殊字符
            None              # None值
        ]
        
        for nickname in invalid_nicknames:
            assert validate_nickname(nickname) is False, f"昵称应该无效: {nickname}"
    
    def test_validate_work_type_valid(self):
        """测试有效的作品类型"""
        valid_types = [
            "game",
            "animation",
            "artwork",
            "music",
            "story",
            "tutorial"
        ]
        
        for work_type in valid_types:
            assert validate_work_type(work_type) is True, f"作品类型应该有效: {work_type}"
    
    def test_validate_work_type_invalid(self):
        """测试无效的作品类型"""
        invalid_types = [
            "invalid_type",
            "game123",
            "",               # 空字符串
            None              # None值
        ]
        
        for work_type in invalid_types:
            assert validate_work_type(work_type) is False, f"作品类型应该无效: {work_type}"


class TestTextProcessing:
    """测试文本处理函数"""
    
    def test_timestamp_to_datetime(self):
        """测试时间戳转换"""
        # 测试2021年1月1日的时间戳
        timestamp = 1609459200  # 2021-01-01 00:00:00 UTC
        dt = timestamp_to_datetime(timestamp)
        
        assert isinstance(dt, datetime)
        assert dt.year == 2021
        assert dt.month == 1
        assert dt.day == 1
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        test_cases = [
            (0, "0 B"),
            (1023, "1023 B"),
            (1024, "1.00 KB"),
            (1536, "1.50 KB"),
            (1048576, "1.00 MB"),
            (1073741824, "1.00 GB"),
            (1099511627776, "1.00 TB")
        ]
        
        for size, expected in test_cases:
            result = format_file_size(size)
            assert result == expected, f"文件大小格式化失败: {size} -> {result}, 期望: {expected}"
    
    def test_truncate_text(self):
        """测试文本截断"""
        # 测试不需要截断的情况
        text = "短文本"
        result = truncate_text(text, 10)
        assert result == text
        
        # 测试需要截断的情况
        long_text = "这是一个很长的文本，需要被截断"
        result = truncate_text(long_text, 10)
        assert result == "这是一个很长的文本..."
        assert len(result) == 13  # 10个字符 + "..."
        
        # 测试边界情况
        exact_text = "正好十个字"
        result = truncate_text(exact_text, 10)
        assert result == exact_text
    
    def test_strip_html_tags(self):
        """测试HTML标签清除"""
        test_cases = [
            ("<p>纯文本</p>", "纯文本"),
            ("<div><p>嵌套标签</p></div>", "嵌套标签"),
            ("文本<img src='test.jpg'>中间", "文本中间"),
            ("<br/>换行<br/>", "换行"),
            ("&lt;转义字符&gt;", "<转义字符>"),
            ("普通文本", "普通文本"),
            ("", ""),
            (None, None)
        ]
        
        for html, expected in test_cases:
            result = strip_html_tags(html)
            assert result == expected, f"HTML标签清除失败: {html} -> {result}, 期望: {expected}"
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 测试None值处理
        assert validate_email(None) is False
        assert validate_phone(None) is False
        assert validate_username(None) is False
        assert validate_password(None) is False
        assert validate_post_title(None) is False
        assert validate_post_content(None) is False
        assert validate_nickname(None) is False
        assert validate_work_type(None) is False
        
        # 测试空字符串处理
        assert validate_email("") is False
        assert validate_phone("") is False
        assert validate_username("") is False
        assert validate_password("") is False
        assert validate_post_title("") is False
        assert validate_post_content("") is False
        assert validate_nickname("") is False
        assert validate_work_type("") is False
        
        # 测试特殊字符处理
        assert validate_username("user@123") is False
        assert validate_username("user 123") is False
        assert validate_username("USER123") is False
        assert validate_nickname("user@123") is False
        assert validate_nickname("user 123") is False
        
        # 测试长度边界
        assert validate_username("a" * 21) is False  # 超过20字符
        assert validate_username("a" * 5) is True   # 5字符应该有效
        assert validate_nickname("a" * 21) is False  # 超过20字符
        assert validate_nickname("a" * 5) is True   # 5字符应该有效
        assert validate_post_title("a" * 51) is False  # 超过50字符
        assert validate_post_title("a" * 5) is True    # 5字符应该有效
        assert validate_post_content("a" * 1001) is False  # 超过1000字符
        assert validate_post_content("a" * 10) is True     # 10字符应该有效