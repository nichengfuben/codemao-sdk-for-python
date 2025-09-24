# 📖 用户指南

本指南将帮助您了解如何使用 CodeMao SDK 的所有功能。

## 🚀 安装和配置

### 系统要求

- Python 3.8+
- pip 包管理器

### 安装 SDK

```bash
# 从 PyPI 安装
pip install codemao-sdk

# 或者从源码安装
git clone https://github.com/nichengfuben/codemao-sdk-for-python.git
cd codemao-sdk-for-python
pip install -e .
```

### 验证安装

```python
import codemaokit
print(codemaokit.__version__)
```

## 🔐 认证和用户管理

### 基本认证

```python
from codemaokit import CodeMaoClient

# 创建客户端实例
client = CodeMaoClient()

# 使用用户名和密码登录
client.login("your_username", "your_password")

# 登录成功后，可以获取用户信息
user_info = client.get_user_info()
print(f"用户ID: {user_info.id}")
print(f"昵称: {user_info.nickname}")
print(f"等级: {user_info.level}")
```

### 会话管理

```python
# 检查是否已登录
if client.is_authenticated():
    print("已登录")
else:
    print("未登录")

# 登出
client.logout()
```

### 用户信息更新

```python
# 更新用户信息
client.update_user_info(
    nickname="新昵称",
    signature="新签名",
    avatar_url="https://example.com/avatar.jpg"
)
```

## 📋 板块管理

### 获取所有板块

```python
# 获取所有板块列表
boards = client.get_boards()

for board in boards:
    print(f"板块ID: {board.id}")
    print(f"板块名称: {board.name}")
    print(f"描述: {board.description}")
    print(f"帖子数: {board.post_count}")
    print("---")
```

### 查找特定板块

```python
# 按ID查找板块
board = client.get_board_by_id(123)
if board:
    print(f"找到板块: {board.name}")

# 按名称查找板块
board = client.get_board_by_name("Python")
if board:
    print(f"找到板块: {board.name}")
```

## 📝 帖子操作

### 创建帖子

```python
# 在指定板块创建帖子
post = client.create_post(
    board_id=123,
    title="我的第一个帖子",
    content="这是帖子内容，支持 **Markdown** 格式。",
    tags=["python", "编程"]
)

print(f"帖子创建成功！ID: {post.id}")
```

### 回复帖子

```python
# 回复指定帖子
reply = client.reply_to_post(
    post_id=456,
    content="这是一条回复内容。"
)

print(f"回复成功！ID: {reply.id}")
```

### 获取帖子信息

```python
# 获取帖子详情
post = client.get_post(456)
print(f"标题: {post.title}")
print(f"作者: {post.author}")
print(f"发布时间: {post.created_at}")
print(f"点赞数: {post.likes}")
print(f"回复数: {post.reply_count}")
```

### 删除帖子

```python
# 删除自己的帖子
success = client.delete_post(456)
if success:
    print("帖子删除成功")
```

## 📊 数据统计

### 消息统计

```python
# 获取消息统计信息
stats = client.get_message_stats()
print(f"未读消息: {stats.unread_count}")
print(f"系统通知: {stats.system_notifications}")
print(f"回复通知: {stats.reply_notifications}")
print(f"点赞通知: {stats.like_notifications}")
```

### 用户活跃度

```python
# 获取用户活跃度数据
activity = client.get_user_activity()
print(f"今日发帖: {activity.posts_today}")
print(f"本周发帖: {activity.posts_this_week}")
print(f"总发帖数: {activity.total_posts}")
```

## 🔧 高级功能

### 错误处理

```python
from codemaokit import CodeMaoError, AuthenticationError, APIError

try:
    client.login("wrong_username", "wrong_password")
except AuthenticationError as e:
    print(f"认证失败: {e.message}")
except APIError as e:
    print(f"API 错误: {e.status_code} - {e.message}")
except CodeMaoError as e:
    print(f"SDK 错误: {e}")
```

### 批量操作

```python
# 批量获取用户信息
user_ids = [1, 2, 3, 4, 5]
users = client.get_users_batch(user_ids)

for user in users:
    print(f"用户: {user.nickname} (等级: {user.level})")
```

### 搜索功能

```python
# 搜索帖子
results = client.search_posts(
    keyword="Python",
    board_id=123,  # 可选：在特定板块搜索
    sort_by="relevance",  # relevance, time, likes
    limit=10
)

for post in results:
    print(f"帖子: {post.title} (作者: {post.author})")
```

### 过滤和排序

```python
# 获取帖子列表并排序
posts = client.get_board_posts(
    board_id=123,
    sort_by="likes",  # time, likes, replies
    order="desc",  # asc, desc
    limit=20
)
```

## 🛡️ 最佳实践

### 1. 使用上下文管理器

```python
# 推荐：使用上下文管理器自动管理连接
with CodeMaoClient() as client:
    client.login("username", "password")
    # 执行操作...
# 自动清理资源
```

### 2. 缓存结果

```python
# 对于不经常变化的数据，考虑缓存
import time

class CachedClient:
    def __init__(self):
        self.client = CodeMaoClient()
        self._boards_cache = None
        self._cache_time = 0
        self._cache_duration = 300  # 5分钟
    
    def get_boards(self):
        now = time.time()
        if self._boards_cache is None or (now - self._cache_time) > self._cache_duration:
            self._boards_cache = self.client.get_boards()
            self._cache_time = now
        return self._boards_cache
```

### 3. 处理速率限制

```python
import time

class RateLimitedClient:
    def __init__(self, max_requests=100, time_window=60):
        self.client = CodeMaoClient()
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_times = []
    
    def make_request(self, func, *args, **kwargs):
        now = time.time()
        
        # 清理过期的请求记录
        self.request_times = [t for t in self.request_times if now - t < self.time_window]
        
        # 检查是否超过限制
        if len(self.request_times) >= self.max_requests:
            sleep_time = self.time_window - (now - self.request_times[0])
            if sleep_time > 0:
                print(f"达到速率限制，等待 {sleep_time:.1f} 秒...")
                time.sleep(sleep_time)
        
        # 执行请求
        result = func(*args, **kwargs)
        self.request_times.append(time.time())
        return result
```

### 4. 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 在代码中使用日志
def create_post_with_logging(client, title, content):
    logger.info(f"创建帖子: {title}")
    try:
        post = client.create_post(title=title, content=content)
        logger.info(f"帖子创建成功: ID={post.id}")
        return post
    except Exception as e:
        logger.error(f"帖子创建失败: {e}")
        raise
```

## 🆘 常见问题

### Q: 登录失败怎么办？

A: 检查以下几点：
- 用户名和密码是否正确
- 网络连接是否正常
- 是否需要验证码（某些情况下）

### Q: 如何处理超时错误？

A: 可以增加超时时间：
```python
client = CodeMaoClient(timeout=60)  # 60秒超时
```

### Q: 如何获取更多的调试信息？

A: 启用调试日志：
```python
import logging
logging.getLogger('codemaokit').setLevel(logging.DEBUG)
```

### Q: 支持代理吗？

A: 是的，可以通过设置环境变量：
```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'https://proxy.example.com:8080'
```

## 📞 获取帮助

如果您遇到问题或有疑问：

1. 查看 [API 参考](api-reference.md) 获取详细信息
2. 在 [GitHub Issues](https://github.com/nichengfuben/codemao-sdk-for-python/issues) 报告问题
3. 加入我们的 [Discord 社区](https://discord.gg/codemao-sdk) 讨论

---

**下一步**：查看 [API 参考](api-reference.md) 了解所有可用功能！