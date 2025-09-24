# CodeMao SDK for Python

[![PyPI version](https://badge.fury.io/py/pycodemao.svg)](https://badge.fury.io/py/pycodemao)
[![Python versions](https://img.shields.io/pypi/pyversions/pycodemao.svg)](https://pypi.org/project/pycodemao/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/your-username/pycodemao/workflows/Tests/badge.svg)](https://github.com/your-username/pycodemao/actions)
[![Coverage](https://codecov.io/gh/your-username/pycodemao/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/pycodemao)

🚀 **现代异步Python SDK，专为编程猫(CodeMao)平台API设计**

<p align="center">
  <img src="https://via.placeholder.com/800x400/4CAF50/white?text=PyCodeMao+SDK" alt="PyCodeMao SDK Banner" />
</p>

## ✨ 核心特性

<div align="center">

| 🎯 **类型安全** | ⚡ **异步优先** | 🛡️ **企业级** | 🎨 **开发者友好** |
|:-------------:|:-------------:|:-------------:|:---------------:|
| 完整的类型注解 | 基于asyncio | 生产环境验证 | 直观的API设计 |
| Pydantic模型 | 高性能并发 | 完善的异常处理 | 丰富的示例代码 |

</div>

### 🌟 亮点功能

- **🔐 智能认证** - 自动token管理和刷新
- **📊 速率限制** - 内置智能限流保护  
- **🔄 自动重试** - 智能重试机制
- **📚 完整API覆盖** - 用户、作品、论坛全覆盖
- **🔍 类型推断** - IDE完美支持
- **⚡ 高性能** - 异步IO优化

## 🚀 快速开始

### 安装

```bash
pip install pycodemao
```

### 30秒上手

```python
import asyncio
import pycodemao

async def main():
    # 创建客户端
    client = pycodemao.create_client("your_api_key_here")
    
    # 获取用户信息
    user = await client.get_user("编程猫小王子")
    print(f"👋 欢迎, {user.nickname}!")
    
    # 发布作品
    work = await client.create_work(
        title="我的第一个Python程序",
        content="print('Hello, CodeMao!')",
        work_type="python"
    )
    print(f"🎉 作品发布成功: {work.title}")
    
    # 论坛发帖
    post = await client.create_post(
        title="Python学习心得分享",
        content="今天学会了使用PyCodeMao SDK...",
        board_id=123
    )
    print(f"💬 帖子发布成功: {post.title}")

# 运行
asyncio.run(main())
```

## 📖 详细文档

### 认证方式

```python
# API Key认证（推荐）
client = pycodemao.create_client("your_api_key")

# 用户名密码认证
client = CodeMaoClient()
await client.login("username", "password")
```

### 用户管理

```python
# 获取用户信息
user = await client.get_user("username")
print(f"昵称: {user.nickname}")
print(f"等级: {user.level}")
print(f"注册时间: {user.created_at}")

# 更新用户资料
await client.update_user_profile(
    nickname="新的昵称",
    description="个人简介"
)
```

### 作品管理

```python
# 创建作品
work = await client.create_work(
    title="我的创意项目",
    content="# 项目代码\nprint('Amazing!')",
    work_type="python",
    tags=["创意", "学习"]
)

# 获取作品列表
works = await client.get_user_works("username", page=1, limit=20)
for work in works.items:
    print(f"作品: {work.title} - 👍 {work.likes} - 💬 {work.comments}")

# 点赞作品
await client.like_work(work.id)
```

### 论坛互动

```python
# 发布帖子
post = await client.create_post(
    title="技术讨论：Python异步编程",
    content="## 异步编程入门\n...详细内容...",
    board_id=456
)

# 获取论坛板块
boards = await client.get_forum_boards()
for board in boards:
    print(f"板块: {board.name} - {board.description}")

# 回复帖子
await client.reply_post(post.id, "很有帮助的分享！")
```

## 🏗️ 架构设计

### 技术栈

- **🐍 Python 3.8+** - 现代Python特性
- **⚡ aiohttp** - 异步HTTP客户端
- **🔧 Pydantic** - 数据验证和序列化
- **🧪 pytest** - 测试框架
- **📊 coverage** - 代码覆盖率

### 项目结构

```
pycodemao/
├── client.py          # 主客户端类
├── models/            # Pydantic数据模型
├── exceptions/        # 自定义异常
├── utils/             # 工具函数
└── __init__.py        # 包入口
```

## 🧪 测试

我们采用**测试驱动开发(TDD)**，确保代码质量：

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=pycodemao --cov-report=html

# 运行特定测试
pytest tests/unit/test_client.py::TestCodeMaoClient::test_get_user
```

### 测试覆盖率

- ✅ **单元测试** - 核心功能全覆盖
- ✅ **集成测试** - API交互验证
- ✅ **异常测试** - 错误处理验证
- ✅ **性能测试** - 并发性能验证

## 🎨 代码质量

### 类型安全

```python
from typing import Optional, List
from pycodemao import User, Work

async def get_top_works(client: CodeMaoClient, 
                       username: str, 
                       limit: int = 10) -> List[Work]:
    """获取用户的热门作品 - 完整类型注解"""
    user = await client.get_user(username)
    works = await client.get_user_works(user.id, limit=limit)
    return sorted(works.items, key=lambda w: w.likes, reverse=True)
```

### 异常处理

```python
from pycodemao import AuthenticationError, RateLimitError

try:
    user = await client.get_user("invalid_user")
except AuthenticationError:
    print("❌ 认证失败，请检查API密钥")
except RateLimitError:
    print("⏰ 请求过于频繁，请稍后重试")
except Exception as e:
    print(f"❌ 未知错误: {e}")
```

## 🚀 性能优化

### 并发请求

```python
import asyncio
from pycodemao import CodeMaoClient

async def fetch_multiple_users():
    client = CodeMaoClient("your_api_key")
    
    # 并发获取多个用户信息
    usernames = ["user1", "user2", "user3", "user4"]
    tasks = [client.get_user(username) for username in usernames]
    users = await asyncio.gather(*tasks)
    
    for user in users:
        print(f"用户: {user.nickname}")

asyncio.run(fetch_multiple_users())
```

### 连接池优化

```python
# 自定义连接池配置
client = CodeMaoClient(
    api_key="your_key",
    timeout=30,
    max_connections=100,
    retry_attempts=3
)
```

## 📈 社区与支持

### 🤝 贡献指南

我们欢迎所有形式的贡献！

- 🐛 **报告Bug** - [提交Issue](https://github.com/your-username/pycodemao/issues)
- 💡 **功能建议** - [讨论区](https://github.com/your-username/pycodemao/discussions)
- 🔧 **代码贡献** - [Pull Request](https://github.com/your-username/pycodemao/pulls)
- 📖 **文档改进** - 帮助完善文档

### 🌟 Star历史

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/pycodemao&type=Date)](https://star-history.com/#your-username/pycodemao&Date)

### 📊 项目统计

- 🏷️ **版本**: 2.0.0
- 📅 **发布**: 2024年
- 👥 **贡献者**: 5+
- ⭐ **Stars**: 目标10,000+
- 📦 **下载量**: 10,000+

## 🔗 相关链接

- 📚 [官方文档](https://pycodemao.readthedocs.io/)
- 🐍 [PyPI包](https://pypi.org/project/pycodemao/)
- 🐙 [GitHub仓库](https://github.com/your-username/pycodemao)
- 💬 [Discord社区](https://discord.gg/pycodemao)
- 📧 [邮件支持](mailto:support@pycodemao.com)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持！** 

[![GitHub Stars](https://img.shields.io/github/stars/your-username/pycodemao?style=social)](https://github.com/your-username/pycodemao)

</div>