# API 参考文档

## CodeMaoClient

CodeMao API 的主要客户端类。

### 类定义

```python
class CodeMaoClient:
    """CodeMao API 客户端"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.codemao.net",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        """初始化客户端
        
        Args:
            api_key: API 密钥
            base_url: API 基础 URL
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            retry_delay: 重试延迟时间（秒）
            session: 可选的 aiohttp 会话
        """
```

### 用户管理

#### get_user

```python
async def get_user(self, username: str) -> User:
    """获取用户信息
    
    Args:
        username: 用户名
        
    Returns:
        User: 用户对象
        
    Raises:
        UserNotFoundError: 用户未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

**示例**:
```python
user = await client.get_user("test_user")
print(f"用户名: {user.username}")
print(f"等级: {user.level}")
print(f"粉丝数: {user.followers}")
```

#### get_user_by_id

```python
async def get_user_by_id(self, user_id: int) -> User:
    """通过ID获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        User: 用户对象
        
    Raises:
        UserNotFoundError: 用户未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### search_users

```python
async def search_users(
    self, 
    query: str, 
    page: int = 1, 
    per_page: int = 20
) -> PaginatedResponse[User]:
    """搜索用户
    
    Args:
        query: 搜索关键词
        page: 页码（从1开始）
        per_page: 每页数量
        
    Returns:
        PaginatedResponse[User]: 分页的用户响应
        
    Raises:
        ValidationError: 参数验证失败
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

### 作品管理

#### create_work

```python
async def create_work(
    self,
    title: str,
    content: str,
    work_type: str = "python",
    tags: Optional[List[str]] = None,
    description: Optional[str] = None,
    is_public: bool = True
) -> Work:
    """创建新作品
    
    Args:
        title: 作品标题
        content: 作品内容（代码）
        work_type: 作品类型 (python, javascript, html, etc.)
        tags: 标签列表
        description: 作品描述
        is_public: 是否公开
        
    Returns:
        Work: 创建的作品对象
        
    Raises:
        ValidationError: 参数验证失败
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

**示例**:
```python
work = await client.create_work(
    title="我的Python程序",
    content="print('Hello, CodeMao!')",
    work_type="python",
    tags=["python", "tutorial"],
    description="一个简单的Python程序"
)
print(f"作品ID: {work.id}")
print(f"创建时间: {work.created_at}")
```

#### get_work

```python
async def get_work(self, work_id: int) -> Work:
    """获取作品信息
    
    Args:
        work_id: 作品ID
        
    Returns:
        Work: 作品对象
        
    Raises:
        WorkNotFoundError: 作品未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### list_works

```python
async def list_works(
    self,
    user_id: Optional[int] = None,
    work_type: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> PaginatedResponse[Work]:
    """获取作品列表
    
    Args:
        user_id: 用户ID（可选，不指定则获取所有作品）
        work_type: 作品类型过滤（可选）
        page: 页码（从1开始）
        per_page: 每页数量
        sort_by: 排序字段 (created_at, likes, views)
        sort_order: 排序顺序 (asc, desc)
        
    Returns:
        PaginatedResponse[Work]: 分页的作品响应
        
    Raises:
        ValidationError: 参数验证失败
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### update_work

```python
async def update_work(
    self,
    work_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    description: Optional[str] = None,
    is_public: Optional[bool] = None
) -> Work:
    """更新作品
    
    Args:
        work_id: 作品ID
        title: 新标题（可选）
        content: 新内容（可选）
        tags: 新标签（可选）
        description: 新描述（可选）
        is_public: 新公开状态（可选）
        
    Returns:
        Work: 更新后的作品对象
        
    Raises:
        WorkNotFoundError: 作品未找到
        ValidationError: 参数验证失败
        AuthorizationError: 权限不足
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### delete_work

```python
async def delete_work(self, work_id: int) -> bool:
    """删除作品
    
    Args:
        work_id: 作品ID
        
    Returns:
        bool: 删除成功返回 True
        
    Raises:
        WorkNotFoundError: 作品未找到
        AuthorizationError: 权限不足
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### like_work

```python
async def like_work(self, work_id: int) -> bool:
    """点赞作品
    
    Args:
        work_id: 作品ID
        
    Returns:
        bool: 点赞成功返回 True
        
    Raises:
        WorkNotFoundError: 作品未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### unlike_work

```python
async def unlike_work(self, work_id: int) -> bool:
    """取消点赞作品
    
    Args:
        work_id: 作品ID
        
    Returns:
        bool: 取消点赞成功返回 True
        
    Raises:
        WorkNotFoundError: 作品未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

### 论坛互动

#### create_post

```python
async def create_post(
    self,
    title: str,
    content: str,
    board_id: int,
    tags: Optional[List[str]] = None,
    is_public: bool = True
) -> Post:
    """创建论坛帖子
    
    Args:
        title: 帖子标题
        content: 帖子内容
        board_id: 板块ID
        tags: 标签列表
        is_public: 是否公开
        
    Returns:
        Post: 创建的帖子对象
        
    Raises:
        ValidationError: 参数验证失败
        BoardNotFoundError: 板块未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

**示例**:
```python
post = await client.create_post(
    title="Python学习心得",
    content="分享一些Python学习的经验和技巧...",
    board_id=1,
    tags=["python", "tutorial", "learning"]
)
print(f"帖子ID: {post.id}")
print(f"创建时间: {post.created_at}")
```

#### get_post

```python
async def get_post(self, post_id: int) -> Post:
    """获取帖子信息
    
    Args:
        post_id: 帖子ID
        
    Returns:
        Post: 帖子对象
        
    Raises:
        PostNotFoundError: 帖子未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### list_posts

```python
async def list_posts(
    self,
    board_id: Optional[int] = None,
    page: int = 1,
    per_page: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> PaginatedResponse[Post]:
    """获取帖子列表
    
    Args:
        board_id: 板块ID（可选，不指定则获取所有帖子）
        page: 页码（从1开始）
        per_page: 每页数量
        sort_by: 排序字段 (created_at, likes, replies)
        sort_order: 排序顺序 (asc, desc)
        
    Returns:
        PaginatedResponse[Post]: 分页的帖子响应
        
    Raises:
        ValidationError: 参数验证失败
        BoardNotFoundError: 板块未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### update_post

```python
async def update_post(
    self,
    post_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    is_public: Optional[bool] = None
) -> Post:
    """更新帖子
    
    Args:
        post_id: 帖子ID
        title: 新标题（可选）
        content: 新内容（可选）
        tags: 新标签（可选）
        is_public: 新公开状态（可选）
        
    Returns:
        Post: 更新后的帖子对象
        
    Raises:
        PostNotFoundError: 帖子未找到
        ValidationError: 参数验证失败
        AuthorizationError: 权限不足
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### delete_post

```python
async def delete_post(self, post_id: int) -> bool:
    """删除帖子
    
    Args:
        post_id: 帖子ID
        
    Returns:
        bool: 删除成功返回 True
        
    Raises:
        PostNotFoundError: 帖子未找到
        AuthorizationError: 权限不足
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### like_post

```python
async def like_post(self, post_id: int) -> bool:
    """点赞帖子
    
    Args:
        post_id: 帖子ID
        
    Returns:
        bool: 点赞成功返回 True
        
    Raises:
        PostNotFoundError: 帖子未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### unlike_post

```python
async def unlike_post(self, post_id: int) -> bool:
    """取消点赞帖子
    
    Args:
        post_id: 帖子ID
        
    Returns:
        bool: 取消点赞成功返回 True
        
    Raises:
        PostNotFoundError: 帖子未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

### 论坛板块

#### get_forum_board

```python
async def get_forum_board(self, board_id: int) -> ForumBoard:
    """获取论坛板块信息
    
    Args:
        board_id: 板块ID
        
    Returns:
        ForumBoard: 论坛板块对象
        
    Raises:
        BoardNotFoundError: 板块未找到
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

#### list_forum_boards

```python
async def list_forum_boards(
    self,
    page: int = 1,
    per_page: int = 20
) -> PaginatedResponse[ForumBoard]:
    """获取论坛板块列表
    
    Args:
        page: 页码（从1开始）
        per_page: 每页数量
        
    Returns:
        PaginatedResponse[ForumBoard]: 分页的板块响应
        
    Raises:
        AuthenticationError: 认证失败
        RateLimitError: 速率限制
        NetworkError: 网络错误
    """
```

### 认证和授权

#### authenticate

```python
async def authenticate(self) -> Dict[str, Any]:
    """验证API密钥有效性
    
    Returns:
        Dict[str, Any]: 认证信息
        
    Raises:
        AuthenticationError: 认证失败
        NetworkError: 网络错误
    """
```

#### get_rate_limit_status

```python
async def get_rate_limit_status(self) -> Dict[str, Any]:
    """获取当前速率限制状态
    
    Returns:
        Dict[str, Any]: 速率限制信息
        
    Raises:
        AuthenticationError: 认证失败
        NetworkError: 网络错误
    """
```

### 上下文管理

#### __aenter__

```python
async def __aenter__(self) -> "CodeMaoClient":
    """异步上下文管理器入口"""
```

#### __aexit__

```python
async def __aexit__(
    self,
    exc_type: Optional[Type[BaseException]],
    exc_val: Optional[BaseException],
    exc_tb: Optional[TracebackType]
) -> None:
    """异步上下文管理器出口"""
```

### 工具方法

#### close

```python
async def close(self) -> None:
    """关闭客户端连接"""
```

#### is_authenticated

```python
@property
def is_authenticated(self) -> bool:
    """检查是否已认证"""
```

## 数据模型

### BaseCodeMaoModel

所有数据模型的基类。

```python
class BaseCodeMaoModel(BaseModel):
    """CodeMao 基础数据模型"""
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
```

### User

用户模型。

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
    updated_at: Optional[datetime] = None
```

**字段说明**:
- `id`: 用户ID
- `username`: 用户名
- `nickname`: 昵称
- `level`: 等级
- `followers`: 粉丝数量
- `works`: 作品数量
- `created_at`: 创建时间
- `updated_at`: 更新时间

### Work

作品模型。

```python
class Work(BaseCodeMaoModel):
    """作品模型"""
    
    id: int
    title: str
    content: str
    work_type: str
    author_id: int
    author_name: str
    likes: int
    views: int
    tags: List[str]
    description: Optional[str] = None
    is_public: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
```

**字段说明**:
- `id`: 作品ID
- `title`: 标题
- `content`: 内容（代码）
- `work_type`: 作品类型
- `author_id`: 作者ID
- `author_name`: 作者名
- `likes`: 点赞数
- `views`: 查看数
- `tags`: 标签列表
- `description`: 描述
- `is_public`: 是否公开
- `created_at`: 创建时间
- `updated_at`: 更新时间

### Post

帖子模型。

```python
class Post(BaseCodeMaoModel):
    """帖子模型"""
    
    id: int
    title: str
    content: str
    author_id: int
    author_name: str
    board_id: int
    board_name: str
    likes: int
    replies: int
    tags: List[str]
    is_public: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
```

**字段说明**:
- `id`: 帖子ID
- `title`: 标题
- `content`: 内容
- `author_id`: 作者ID
- `author_name`: 作者名
- `board_id`: 板块ID
- `board_name`: 板块名
- `likes`: 点赞数
- `replies`: 回复数
- `tags`: 标签列表
- `is_public`: 是否公开
- `created_at`: 创建时间
- `updated_at`: 更新时间

### ForumBoard

论坛板块模型。

```python
class ForumBoard(BaseCodeMaoModel):
    """论坛板块模型"""
    
    id: int
    name: str
    description: str
    post_count: int
    moderator_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
```

**字段说明**:
- `id`: 板块ID
- `name`: 板块名
- `description`: 描述
- `post_count`: 帖子数量
- `moderator_count`: 版主数量
- `created_at`: 创建时间
- `updated_at`: 更新时间

### APIResponse

API 响应包装模型。

```python
class APIResponse(BaseModel, Generic[T]):
    """API 响应包装"""
    
    success: bool
    data: T
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
```

**字段说明**:
- `success`: 是否成功
- `data`: 响应数据
- `message`: 消息
- `timestamp`: 时间戳

### PaginatedResponse

分页响应模型。

```python
class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
```

**字段说明**:
- `items`: 项目列表
- `total`: 总数量
- `page`: 当前页码
- `per_page`: 每页数量
- `total_pages`: 总页数
- `has_next`: 是否有下一页
- `has_prev`: 是否有上一页

## 异常处理

### 异常层次结构

```
CodeMaoError (基类)
├── AuthenticationError    # 认证错误
├── AuthorizationError   # 授权错误
├── ResourceNotFoundError # 资源未找到
│   ├── UserNotFoundError     # 用户未找到
│   ├── WorkNotFoundError     # 作品未找到
│   ├── PostNotFoundError     # 帖子未找到
│   └── BoardNotFoundError    # 板块未找到
├── ValidationError      # 验证错误
├── RateLimitError       # 速率限制
├── NetworkError         # 网络错误
└── ServerError          # 服务器错误
```

### 异常使用

```python
from pycodemao import CodeMaoClient, UserNotFoundError, AuthenticationError

client = CodeMaoClient("your_api_key")

try:
    user = await client.get_user("non_existent_user")
except UserNotFoundError as e:
    print(f"用户未找到: {e}")
except AuthenticationError as e:
    print(f"认证失败: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 工具函数

### retry_on_failure

```python
def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """失败重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始延迟时间（秒）
        backoff: 退避因子
        exceptions: 需要重试的异常类型
        
    Returns:
        Callable: 装饰器函数
    """
```

### rate_limit

```python
def rate_limit(
    calls: int = 10,
    period: int = 60,
    scope: str = "global"
) -> Callable:
    """速率限制装饰器
    
    Args:
        calls: 指定时间内的调用次数限制
        period: 时间周期（秒）
        scope: 作用域 (global, user, session)
        
    Returns:
        Callable: 装饰器函数
    """
```

### validate_data

```python
def validate_data(data: Any, model: Type[BaseModel]) -> BaseModel:
    """验证数据
    
    Args:
        data: 要验证的数据
        model: Pydantic 模型类
        
    Returns:
        BaseModel: 验证后的模型实例
        
    Raises:
        ValidationError: 验证失败
    """
```

### generate_signature

```python
def generate_signature(
    data: str,
    secret: str,
    algorithm: str = "sha256"
) -> str:
    """生成签名
    
    Args:
        data: 要签名的数据
        secret: 密钥
        algorithm: 哈希算法
        
    Returns:
        str: 签名
    """
```

### setup_logging

```python
def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    logger_name: Optional[str] = None
) -> logging.Logger:
    """设置日志
    
    Args:
        level: 日志级别
        format_string: 格式字符串
        logger_name: 日志器名称
        
    Returns:
        logging.Logger: 日志器实例
    """
```

## 便利函数

### create_client

```python
def create_client(
    api_key: str,
    **kwargs
) -> CodeMaoClient:
    """创建客户端实例
    
    Args:
        api_key: API 密钥
        **kwargs: 其他参数传递给 CodeMaoClient
        
    Returns:
        CodeMaoClient: 客户端实例
        
    Example:
        >>> client = create_client("your_api_key")
        >>> user = await client.get_user("test_user")
    """
```