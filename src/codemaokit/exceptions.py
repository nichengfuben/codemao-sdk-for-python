"""
CodeMao SDK 异常定义
"""

from typing import Optional, Dict, Any


class CodeMaoError(Exception):
    """CodeMao SDK 基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.response_data = response_data
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class AuthenticationError(CodeMaoError):
    """认证异常 - 登录失败、token过期等"""
    pass


class APIError(CodeMaoError):
    """API调用异常 - 服务器返回错误"""
    pass


class ValidationError(CodeMaoError):
    """参数验证异常 - 输入参数不符合要求"""
    pass


class ResourceNotFoundError(CodeMaoError):
    """资源不存在异常"""
    pass


class RateLimitError(CodeMaoError):
    """请求频率限制异常"""
    pass


class NetworkError(CodeMaoError):
    """网络异常 - 连接失败、超时等"""
    pass