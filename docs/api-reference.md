# 📚 API 参考

CodeMao SDK 的完整 API 文档。

## 🎯 核心类

### CodeMaoClient

主客户端类，用于与 CodeMao 平台交互。

#### 构造函数

```python
CodeMaoClient(
    base_url: str = "https://api.codemao.cn",
    timeout: int = 30,
    max_retries: int = 3,
    user_agent: str = "CodeMaoSDK/1.0.0",
    connection_pool_size: int = 10,
    connection_pool_maxsize: int = 20
)
```

**参数**：
- `base_url` (str): API 基础 URL
- `timeout` (int): 请求超时时间（秒）
- `max_retries` (int): 最大重试次数
- `user_agent` (str): 自定义 User-Agent
- `connection_pool_size` (int): 连接池大小
- `connection_pool_maxsize` (int): 连接池最大大小

#### 方法

##### login(username: str, password: str) → bool

用户登录。

**参数**：
- `username` (str): 用户名
- `password` (str): 密码

**返回**：
- `bool`: 登录成功返回 True

**抛出**：
- `AuthenticationError`: 认证失败
- `APIError`: API 错误

**示例**：
```python
client = CodeMaoClient()
success = client.login("username", "password")
```

##### logout() → bool

用户登出。

**返回**：
- `bool`: 登出成功返回 True

**示例**：
```python
client.logout()
```

##### is_authenticated() → bool

检查用户是否已认证。

**返回**：
- `bool`: 已认证返回 True

**示例**：
```python
if client.is_authenticated():
    print("已登录")
```

##### get_user_info() → User

获取当前用户信息。

**返回**：
- `User`: 用户信息对象

**抛出**：
- `AuthenticationError`: 未认证
- `APIError`: API 错误

**示例**：
```python
user_info = client.get_user_info()
print(f"昵称: {user_info.nickname}")
```

##### update_user_info(**kwargs) → bool

更新用户信息。

**参数**：
- `nickname` (str, optional): 新昵称
- `signature` (str, optional): 新签名
- `avatar_url` (str, optional): 新头像 URL

**返回**：
- `bool`: 更新成功返回 True

**示例**：
```python
client.update_user_info(nickname="新昵称", signature="新签名")
```

##### get_boards() → List[Board]

获取所有板块列表。

**返回**：
- `List[Board]`: 板块列表

**示例**：
```python
boards = client.get_boards()
for board in boards:
    print(f"{board.name}: {board.description}")
```

##### get_board_by_id(board_id: int) → Optional[Board]

根据 ID 获取板块。

**参数**：
- `board_id` (int): 板块 ID

**返回**：
- `Optional[Board]`: 板块对象，不存在返回 None

**示例**：
```python
board = client.get_board_by_id(123)
if board:
    print(f"板块名称: {board.name}")
```

##### get_board_by_name(name: str) → Optional[Board]

根据名称获取板块。

**参数**：
- `name` (str): 板块名称

**返回**：
- `Optional[Board]`: 板块对象，不存在返回 None

**示例**：
```python
board = client.get_board_by_name("Python")
if board:
    print(f"板块ID: {board.id}")
```

##### create_post(board_id: int, title: str, content: str, tags: List[str] = None) → Post

创建新帖子。

**参数**：
- `board_id` (int): 板块 ID
- `title` (str): 帖子标题
- `content` (str): 帖子内容（支持 Markdown）
- `tags` (List[str], optional): 标签列表

**返回**：
- `Post`: 创建的帖子对象

**抛出**：
- `ValidationError`: 参数验证失败
- `APIError`: API 错误

**示例**：
```python
post = client.create_post(
    board_id=123,
    title="我的第一个帖子",
    content="这是内容，支持 **Markdown**",
    tags=["python", "编程"]
)
```

##### reply_to_post(post_id: int, content: str) → Post

回复帖子。

**参数**：
- `post_id` (int): 要回复的帖子 ID
- `content` (str): 回复内容

**返回**：
- `Post`: 回复的帖子对象

**示例**：
```python
reply = client.reply_to_post(456, "这是一条回复")
```

##### delete_post(post_id: int) → bool

删除帖子。

**参数**：
- `post_id` (int): 要删除的帖子 ID

**返回**：
- `bool`: 删除成功返回 True

**示例**：
```python
success = client.delete_post(456)
if success:
    print("帖子删除成功")
```

##### get_post(post_id: int) → Post

获取帖子详情。

**参数**：
- `post_id` (int): 帖子 ID

**返回**：
- `Post`: 帖子对象

**示例**：
```python
post = client.get_post(456)
print(f"标题: {post.title}")
print(f"作者: {post.author}")
```

##### get_message_stats() → MessageStats

获取消息统计信息。

**返回**：
- `MessageStats`: 消息统计对象

**示例**：
```python
stats = client.get_message_stats()
print(f"未读消息: {stats.unread_count}")
```

##### search_posts(keyword: str, board_id: int = None, sort_by: str = "relevance", limit: int = 20) → List[Post]

搜索帖子。

**参数**：
- `keyword` (str): 搜索关键词
- `board_id` (int, optional): 板块 ID（可选）
- `sort_by` (str): 排序方式 ("relevance", "time", "likes")
- `limit` (int): 返回结果数量限制

**返回**：
- `List[Post]`: 匹配的帖子列表

**示例**：
```python
results = client.search_posts("Python", sort_by="likes", limit=10)
```

##### get_board_posts(board_id: int, sort_by: str = "time", order: str = "desc", limit: int = 20) → List[Post]

获取板块中的帖子。

**参数**：
- `board_id` (int): 板块 ID
- `sort_by` (str): 排序字段 ("time", "likes", "replies")
- `order` (str): 排序顺序 ("asc", "desc")
- `limit` (int): 返回结果数量限制

**返回**：
- `List[Post]`: 帖子列表

**示例**：
```python
posts = client.get_board_posts(123, sort_by="likes", limit=10)
```

##### get_users_batch(user_ids: List[int]) → List[User]

批量获取用户信息。

**参数**：
- `user_ids` (List[int]): 用户 ID 列表

**返回**：
- `List[User]`: 用户信息列表

**示例**：
```python
users = client.get_users_batch([1, 2, 3, 4, 5])
```

##### get_user_works(user_id: int, limit: int = 20) → List[Work]

获取用户的作品。

**参数**：
- `user_id` (int): 用户 ID
- `limit` (int): 返回结果数量限制

**返回**：
- `List[Work]`: 作品列表

**示例**：
```python
works = client.get_user_works(123, limit=10)
for work in works:
    print(f"作品: {work.title} (点赞: {work.likes})")
```

##### get_user_honor(user_id: int) → UserHonor

获取用户荣誉信息。

**参数**：
- `user_id` (int): 用户 ID

**返回**：
- `UserHonor`: 用户荣誉对象

**示例**：
```python
honor = client.get_user_honor(123)
print(f"荣誉等级: {honor.level}")
print(f"获得徽章: {len(honor.badges)}")
```

## 📊 数据模型

### User

用户数据模型。

```python
@dataclass
class User:
    id: int
    nickname: str
    avatar_url: str
    level: int
    signature: str
    followers_count: int
    following_count: int
    posts_count: int
    works_count: int
    created_at: datetime
    last_active_at: datetime
```

### Board

板块数据模型。

```python
@dataclass
class Board:
    id: int
    name: str
    description: str
    icon_url: str
    post_count: int
    follower_count: int
    moderator_count: int
    created_at: datetime
```

### Post

帖子数据模型。

```python
@dataclass
class Post:
    id: int
    title: str
    content: str
    author: User
    board: Board
    tags: List[str]
    likes: int
    replies: int
    views: int
    is_liked: bool
    is_following: bool
    created_at: datetime
    updated_at: datetime
```

### Work

作品数据模型。

```python
@dataclass
class Work:
    id: int
    title: str
    description: str
    thumbnail_url: str
    author: User
    type: str
    likes: int
    views: int
    comments: int
    is_liked: bool
    created_at: datetime
    updated_at: datetime
```

### MessageStats

消息统计数据模型。

```python
@dataclass
class MessageStats:
    unread_count: int
    system_notifications: int
    reply_notifications: int
    like_notifications: int
    follow_notifications: int
    total_count: int
```

### UserHonor

用户荣誉数据模型。

```python
@dataclass
class UserHonor:
    user_id: int
    level: int
    badges: List[str]
    achievements: List[str]
    points: int
    rank: int
    joined_at: datetime
```

## 🚨 异常处理

### CodeMaoError

所有 SDK 异常的基类。

```python
class CodeMaoError(Exception):
    def __init__(self, message: str, error_code: int = None, response_data: dict = None):
        self.message = message
        self.error_code = error_code
        self.response_data = response_data
```

### AuthenticationError

认证相关异常。

```python
class AuthenticationError(CodeMaoError):
    """当用户认证失败时抛出"""
```

### APIError

API 相关异常。

```python
class APIError(CodeMaoError):
    """当 API 返回错误时抛出"""
```

### ValidationError

参数验证异常。

```python
class ValidationError(CodeMaoError):
    """当参数验证失败时抛出"""
```

### RateLimitError

速率限制异常。

```python
class RateLimitError(CodeMaoError):
    """当达到 API 速率限制时抛出"""
```

### NetworkError

网络相关异常。

```python
class NetworkError(CodeMaoError):
    """当网络请求失败时抛出"""
```

### TimeoutError

超时异常。

```python
class TimeoutError(CodeMaoError):
    """当请求超时时抛出"""
```

## 🔧 工具函数

### 验证函数

#### validate_email(email: str) → bool

验证邮箱格式。

**参数**：
- `email` (str): 要验证的邮箱地址

**返回**：
- `bool`: 格式正确返回 True

**示例**：
```python
from codemaokit.utils import validate_email

is_valid = validate_email("user@example.com")  # True
is_valid = validate_email("invalid-email")     # False
```

#### validate_phone(phone: str) → bool

验证手机号格式。

**参数**：
- `phone` (str): 要验证的手机号

**返回**：
- `bool`: 格式正确返回 True

#### validate_username(username: str) → bool

验证用户名格式。

**参数**：
- `username` (str): 要验证的用户名

**返回**：
- `bool`: 格式正确返回 True

#### validate_password(password: str) → bool

验证密码强度。

**参数**：
- `password` (str): 要验证的密码

**返回**：
- `bool`: 强度足够返回 True

#### validate_post_title(title: str) → bool

验证帖子标题。

**参数**：
- `title` (str): 要验证的标题

**返回**：
- `bool`: 格式正确返回 True

#### validate_post_content(content: str) → bool

验证帖子内容。

**参数**：
- `content` (str): 要验证的内容

**返回**：
- `bool`: 格式正确返回 True

### 文本处理函数

#### truncate_text(text: str, max_length: int = 100, suffix: str = "...") → str

截断文本。

**参数**：
- `text` (str): 要截断的文本
- `max_length` (int): 最大长度
- `suffix` (str): 后缀字符串

**返回**：
- `str`: 截断后的文本

**示例**：
```python
from codemaokit.utils import truncate_text

short_text = truncate_text("这是一个很长的文本", max_length=10)
# 输出: "这是一个很..."
```

#### strip_html_tags(html: str) → str

移除 HTML 标签。

**参数**：
- `html` (str): 包含 HTML 的字符串

**返回**：
- `str`: 纯文本

**示例**：
```python
from codemaokit.utils import strip_html_tags

text = strip_html_tags("<p>Hello <strong>World</strong></p>")
# 输出: "Hello World"
```

### 时间函数

#### timestamp_to_datetime(timestamp: int) → datetime

时间戳转换为 datetime。

**参数**：
- `timestamp` (int): Unix 时间戳

**返回**：
- `datetime`: datetime 对象

#### datetime_to_timestamp(dt: datetime) → int

datetime 转换为时间戳。

**参数**：
- `dt` (datetime): datetime 对象

**返回**：
- `int`: Unix 时间戳

### 文件函数

#### format_file_size(size_bytes: int) → str

格式化文件大小。

**参数**：
- `size_bytes` (int): 文件大小（字节）

**返回**：
- `str`: 格式化的大小字符串

**示例**：
```python
from codemaokit.utils import format_file_size

size = format_file_size(1024)      # "1.0 KB"
size = format_file_size(1048576)   # "1.0 MB"
```

---

**需要更多帮助？** 查看 [用户指南](user-guide.md) 或 [示例代码](examples.md)！