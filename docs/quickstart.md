# 🚀 快速开始指南

欢迎来到 CodeMao SDK！本指南将帮助您在 5 分钟内快速上手。

## 📦 安装

### 使用 pip 安装（推荐）

```bash
pip install codemao-sdk
```

### 从源码安装

```bash
git clone https://github.com/nichengfuben/codemao-sdk-for-python.git
cd codemao-sdk-for-python
pip install -e .
```

### 验证安装

```python
import codemaokit
print(f"CodeMao SDK 版本: {codemaokit.__version__}")
```

## 🔑 第一个程序

让我们从一个简单的登录示例开始：

```python
from codemaokit import CodeMaoClient

# 创建客户端
client = CodeMaoClient()

# 登录
try:
    success = client.login("your_username", "your_password")
    if success:
        print("✅ 登录成功!")
        
        # 获取用户信息
        user_info = client.get_user_info()
        print(f"👋 欢迎, {user_info.nickname}!")
        print(f"📊 等级: {user_info.level}")
        print(f"👥 粉丝数: {user_info.followers_count}")
        
    else:
        print("❌ 登录失败")
        
finally:
    # 确保登出
    client.logout()
```

## 🎯 核心功能演示

### 1. 浏览板块和帖子

```python
from codemaokit import CodeMaoClient

client = CodeMaoClient()
client.login("your_username", "your_password")

try:
    # 获取所有板块
    boards = client.get_boards()
    print(f"发现 {len(boards)} 个板块")
    
    # 查看第一个板块的帖子
    if boards:
        first_board = boards[0]
        posts = client.get_board_posts(first_board.id, limit=5)
        
        print(f"\n🔥 {first_board.name} 的热门帖子:")
        for post in posts:
            print(f"• {post.title} (👍 {post.likes} | 💬 {post.replies})")
            print(f"  作者: {post.author.nickname}")
            print()
            
finally:
    client.logout()
```

### 2. 发布新帖子

```python
from codemaokit import CodeMaoClient

client = CodeMaoClient()
client.login("your_username", "your_password")

try:
    # 创建新帖子
    new_post = client.create_post(
        board_id=1,  # 替换为实际的板块ID
        title="我的第一个SDK帖子",
        content="大家好！这是我使用 CodeMao SDK 发布的第一条帖子。\n\n这个SDK真的很容易使用！",
        tags=["新手", "分享"]
    )
    
    print(f"✅ 帖子发布成功! ID: {new_post.id}")
    print(f"📖 标题: {new_post.title}")
    
finally:
    client.logout()
```

### 3. 使用上下文管理器

```python
from codemaokit import CodeMaoClient

# 使用上下文管理器自动处理登录/登出
with CodeMaoClient() as client:
    client.login("your_username", "your_password")
    
    # 获取消息统计
    stats = client.get_message_stats()
    print(f"📊 未读消息: {stats.unread_count}")
    print(f"🔔 总消息数: {stats.total_count}")
    
    # 获取用户荣誉
    honors = client.get_user_honors()
    print(f"🏆 获得荣誉: {len(honors)} 个")
```

## 🔧 错误处理

始终添加适当的错误处理：

```python
from codemaokit import CodeMaoClient
from codemaokit.exceptions import AuthenticationError, APIError

client = CodeMaoClient()

try:
    client.login("username", "password")
    
    # 尝试获取用户信息
    user_info = client.get_user_info()
    print(f"用户: {user_info.nickname}")
    
except AuthenticationError as e:
    print(f"🔒 认证失败: {e.message}")
    
except APIError as e:
    print(f"🌐 API 错误: {e.status_code} - {e.message}")
    
except Exception as e:
    print(f"💥 意外错误: {e}")
    
finally:
    client.logout()
```

## 📊 数据导出示例

```python
from codemaokit import CodeMaoClient
import json

with CodeMaoClient() as client:
    client.login("your_username", "your_password")
    
    # 获取用户作品
    works = client.get_user_works(limit=10)
    
    # 导出为JSON
    works_data = []
    for work in works:
        works_data.append({
            "id": work.id,
            "title": work.title,
            "type": work.type,
            "likes": work.likes,
            "views": work.views,
            "created_at": work.created_at.isoformat()
        })
    
    with open("my_works.json", "w", encoding="utf-8") as f:
        json.dump(works_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已导出 {len(works_data)} 个作品到 my_works.json")
```

## 🚀 下一步

恭喜！您已经成功使用了 CodeMao SDK 的核心功能。

### 📚 继续学习

- 📖 [完整API文档](api-reference.md) - 查看所有可用方法
- 💡 [示例代码](examples.md) - 更多实用示例
- 🛡️ [错误处理](error-handling.md) - 学习如何处理各种错误
- 📋 [用户指南](user-guide.md) - 深入了解所有功能

### 🛠️ 高级功能

- **异步支持**: 使用 `asyncio` 进行异步操作
- **批量处理**: 高效处理大量数据
- **自定义配置**: 调整超时、重试等参数
- **插件系统**: 扩展SDK功能

### 🤝 获取帮助

- 🐛 [报告问题](https://github.com/nichengfuben/codemao-sdk-for-python/issues)
- 💬 [讨论区](https://github.com/nichengfuben/codemao-sdk-for-python/discussions)
- 📧 邮件: support@codemao-sdk.com

### ⭐ 支持项目

如果这个项目对您有帮助，请给我们一个 ⭐ Star！

```bash
git clone https://github.com/nichengfuben/codemao-sdk-for-python.git
cd codemao-sdk-for-python
pip install -e .
```

---

**准备好了吗？** 开始构建您的 CodeMao 应用吧！ 🎉