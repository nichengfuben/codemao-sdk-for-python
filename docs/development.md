# 开发文档

## 项目架构

PyCodeMao SDK 采用现代化的领域驱动设计(DDD)架构，确保代码的可维护性和可扩展性。

### 核心架构原则

- **领域驱动设计 (DDD)**: 以业务领域为核心组织代码
- **测试驱动开发 (TDD)**: 先写测试，再实现功能
- **类型安全**: 完整的类型注解和静态检查
- **异步优先**: 基于 asyncio 的高性能设计
- **依赖注入**: 松耦合的组件设计

### 项目结构

```
codemao-sdk-for-python/
├── src/
│   └── pycodemao/
│       ├── __init__.py          # 包入口和便利函数
│       ├── _version.py           # 版本信息
│       ├── client.py            # 主要客户端类
│       ├── models/              # 数据模型层
│       │   └── __init__.py      # Pydantic 数据模型
│       ├── exceptions/          # 异常处理层
│       │   └── __init__.py      # 自定义异常类
│       └── utils/               # 工具层
│           └── __init__.py      # 工具函数和装饰器
├── tests/
│   ├── conftest.py             # 测试配置和 fixtures
│   ├── unit/                   # 单元测试
│   │   ├── test_client.py      # 客户端测试
│   │   ├── test_models.py      # 模型测试
│   │   └── test_exceptions.py  # 异常测试
│   └── integration/            # 集成测试
│       └── test_client_integration.py  # 客户端集成测试
├── examples/                   # 示例代码
│   ├── quick_start.py          # 快速入门
│   ├── basic_examples.py       # 基础示例
│   └── advanced_examples.py    # 高级示例
├── docs/                       # 文档
├── CHANGELOG.md                # 变更日志
├── README.md                   # 项目文档
├── README_zh.md                # 中文文档
├── LICENSE                     # 许可证
├── requirements.txt            # 项目依赖
└── pyproject.toml              # 项目配置
```

## 核心组件详解

### 1. 客户端层 (Client Layer)

**文件**: `src/pycodemao/client.py`

`CodeMaoClient` 是 SDK 的核心类，提供所有 API 接口的封装。

**主要功能**:
- HTTP 请求管理 (基于 aiohttp)
- 认证和授权
- 速率限制和重试机制
- 错误处理和异常转换
- 上下文管理器支持

**设计特点**:
```python
class CodeMaoClient:
    """CodeMao API 客户端"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.codemao.net",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        # 初始化配置
        pass
    
    # 用户管理
    async def get_user(self, username: str) -> User:
        """获取用户信息"""
        pass
    
    # 作品管理
    async def create_work(self, title: str, content: str, **kwargs) -> Work:
        """创建新作品"""
        pass
    
    # 论坛互动
    async def create_post(self, title: str, content: str, board_id: int) -> Post:
        """创建论坛帖子"""
        pass
```

### 2. 数据模型层 (Models Layer)

**文件**: `src/pycodemao/models/__init__.py`

基于 Pydantic 的类型安全数据模型，确保数据验证和序列化。

**核心模型**:
- `BaseCodeMaoModel`: 基础模型，包含公共字段
- `User`: 用户模型
- `Work`: 作品模型
- `Post`: 帖子模型
- `ForumBoard`: 论坛板块模型
- `APIResponse`: API 响应包装
- `PaginatedResponse`: 分页响应包装

**设计特点**:
```python
class User(BaseCodeMaoModel):
    """用户模型"""
    
    id: int
    username: str
    nickname: str
    level: int
    followers: int
    works: int
    created_at: datetime
    
    @validator('username')
    def username_must_be_valid(cls, v):
        """验证用户名格式"""
        if len(v) < 3:
            raise ValueError('用户名长度必须大于3')
        return v
```

### 3. 异常处理层 (Exceptions Layer)

**文件**: `src/pycodemao/exceptions/__init__.py`

层次化的异常体系，提供细粒度的错误处理。

**异常层次**:
```
CodeMaoError (基类)
├── AuthenticationError    # 认证错误
├── AuthorizationError   # 授权错误
├── ResourceNotFoundError # 资源未找到
├── ValidationError      # 验证错误
├── RateLimitError       # 速率限制
├── NetworkError         # 网络错误
└── ServerError          # 服务器错误
```

**使用示例**:
```python
try:
    user = await client.get_user("non_existent_user")
except UserNotFoundError as e:
    print(f"用户未找到: {e}")
except AuthenticationError as e:
    print(f"认证失败: {e}")
except RateLimitError as e:
    print(f"速率限制: {e}")
    await asyncio.sleep(5)  # 等待后重试
```

### 4. 工具层 (Utils Layer)

**文件**: `src/pycodemao/utils/__init__.py`

提供各种工具函数和装饰器。

**主要功能**:
- 日志配置
- 重试装饰器
- 速率限制器
- 数据验证
- 签名生成

**工具函数示例**:
```python
@retry_on_failure(max_retries=3, delay=1.0)
async def fetch_data_with_retry(url: str) -> dict:
    """带重试的数据获取"""
    pass

@rate_limit(calls=10, period=60)
async def rate_limited_api_call():
    """速率限制的API调用"""
    pass
```

## 开发流程

### 1. 测试驱动开发 (TDD)

遵循红-绿-重构循环：

1. **红**: 编写失败的测试
2. **绿**: 编写最小代码使测试通过
3. **重构**: 优化代码结构

**示例**:
```python
# 1. 先写测试 (test_models.py)
def test_user_creation():
    """测试用户创建"""
    user = User(
        id=1,
        username="test_user",
        nickname="测试用户",
        level=1,
        followers=0,
        works=0,
        created_at=datetime.now()
    )
    assert user.username == "test_user"
    assert user.level == 1

# 2. 实现功能 (models/__init__.py)
class User(BaseCodeMaoModel):
    """用户模型"""
    id: int
    username: str
    nickname: str
    level: int = 1  # 默认值
    followers: int = 0
    works: int = 0
    created_at: datetime

# 3. 重构优化
# 添加验证器、方法等
```

### 2. 代码质量保证

**静态检查**:
```bash
# 类型检查
mypy src/

# 代码格式化
black src/
isort src/

# 代码检查
pylint src/
flake8 src/
```

**测试覆盖**:
```bash
# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 目标覆盖率: >90%
```

### 3. 文档编写

**文档字符串规范** (遵循 PEP 257):
```python
def create_work(self, title: str, content: str, **kwargs) -> Work:
    """创建新作品
    
    Args:
        title: 作品标题
        content: 作品内容
        **kwargs: 其他参数
            - work_type: 作品类型 (python, javascript, etc.)
            - tags: 标签列表
            - description: 作品描述
    
    Returns:
        Work: 创建的作品对象
    
    Raises:
        ValidationError: 参数验证失败
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
    
    Example:
        >>> work = await client.create_work(
        ...     title="我的程序",
        ...     content="print('Hello')",
        ...     work_type="python"
        ... )
        >>> print(work.id)
        12345
    """
    pass
```

## 性能优化

### 1. 并发处理

```python
# 并发获取多个用户信息
usernames = ["user1", "user2", "user3"]
tasks = [client.get_user(username) for username in usernames]
users = await asyncio.gather(*tasks)
```

### 2. 连接池管理

```python
# 复用连接池
connector = aiohttp.TCPConnector(
    limit=100,              # 总连接数限制
    limit_per_host=30,      # 单主机连接数限制
    ttl_dns_cache=300,      # DNS缓存时间
    use_dns_cache=True,     # 启用DNS缓存
)

async with aiohttp.ClientSession(connector=connector) as session:
    client = CodeMaoClient(api_key, session=session)
    # 使用客户端...
```

### 3. 缓存策略

```python
# 简单的内存缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_user(username: str) -> User:
    """缓存用户信息的获取"""
    pass

# 或者使用专门的缓存库
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')
cache_key = f"user:{username}"
cached_data = await redis.get(cache_key)
```

## 错误处理和恢复

### 1. 重试策略

```python
@retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
async def resilient_api_call():
    """具有自动重试的API调用"""
    return await client.get_user("username")
```

### 2. 断路器模式

```python
class CircuitBreaker:
    """断路器实现"""
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise e
```

### 3. 优雅降级

```python
async def get_user_with_fallback(username: str) -> Optional[User]:
    """获取用户信息，失败时返回 None"""
    try:
        return await client.get_user(username)
    except UserNotFoundError:
        return None
    except Exception as e:
        logger.warning(f"Failed to get user {username}: {e}")
        return None
```

## 监控和日志

### 1. 结构化日志

```python
import structlog

logger = structlog.get_logger()

async def create_work_with_logging(title: str, content: str) -> Work:
    """带日志记录的作品创建"""
    logger.info(
        "creating_work",
        title=title,
        content_length=len(content),
        work_type="python"
    )
    
    try:
        work = await client.create_work(title, content)
        logger.info(
            "work_created",
            work_id=work.id,
            title=work.title,
            created_at=work.created_at
        )
        return work
    except Exception as e:
        logger.error(
            "work_creation_failed",
            title=title,
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

### 2. 性能监控

```python
import time
import functools

def monitor_performance(func_name: str):
    """性能监控装饰器"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                # 记录性能指标
                logger.info(
                    "api_performance",
                    function=func_name,
                    duration=duration,
                    status="success"
                )
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "api_performance",
                    function=func_name,
                    duration=duration,
                    status="error",
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator
```

## 部署和发布

### 1. 版本管理

使用语义化版本控制 (SemVer):
- MAJOR: 不兼容的API变更
- MINOR: 向下兼容的功能性新增
- PATCH: 向下兼容的问题修正

### 2. 发布流程

```bash
# 1. 更新版本号
# 修改 src/pycodemao/_version.py

# 2. 更新变更日志
# 修改 CHANGELOG.md

# 3. 运行完整测试
pytest
mypy src/
black src/

# 4. 构建包
python -m build

# 5. 发布到 PyPI
twine upload dist/*
```

### 3. 依赖管理

**requirements.txt**:
```
aiohttp>=3.8.0,<4.0.0
pydantic>=1.10.0,<2.0.0
typing-extensions>=4.0.0
```

**pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "pycodemao"
description = "Modern Python SDK for CodeMao API"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "PyCodeMao Team", email = "team@pycodemao.com"},
]
keywords = ["codemao", "api", "sdk", "education", "programming"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "aiohttp>=3.8.0,<4.0.0",
    "pydantic>=1.10.0,<2.0.0",
    "typing-extensions>=4.0.0",
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.20.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "mypy>=0.991",
    "pylint>=2.15.0",
    "flake8>=5.0.0",
]

[project.urls]
Homepage = "https://github.com/your-username/pycodemao"
Documentation = "https://pycodemao.readthedocs.io"
Repository = "https://github.com/your-username/pycodemao.git"
Issues = "https://github.com/your-username/pycodemao/issues"
```

这个开发文档提供了 PyCodeMao SDK 的完整架构设计和开发指南，涵盖了从基础架构到高级特性的所有方面。