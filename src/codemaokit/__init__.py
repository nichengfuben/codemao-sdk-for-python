"""
CodeMao SDK for Python

编程猫Python SDK - 最全的编程猫API封装

:author: nichengfuben
:license: MIT
:version: 1.0.0
"""

from .client import CodeMaoClient
from .models import User, Post, Board, Work
from .exceptions import CodeMaoError, AuthenticationError, APIError

__version__ = "1.0.0"
__author__ = "nichengfuben"
__license__ = "MIT"

__all__ = [
    "CodeMaoClient",
    "User", 
    "Post",
    "Board", 
    "Work",
    "CodeMaoError",
    "AuthenticationError",
    "APIError"
]