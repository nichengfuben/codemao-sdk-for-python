# PyCodeMao - 编程猫 Python SDK

[![PyPI version](https://badge.fury.io/py/pycodemao.svg)](https://badge.fury.io/py/pycodemao)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🐱‍💻 现代化的编程猫(CodeMao) Python SDK，支持异步操作、类型注解和企业级架构

[English](./README.md) | 简体中文

## ✨ 特性

| 特性 | 描述 |
|------|------|
| 🚀 **异步支持** | 基于 `asyncio` 和 `aiohttp` 的高性能异步客户端 |
| 📝 **类型注解** | 完整的类型注解，提供优秀的 IDE 支持 |
| 🏗️ **DDD 架构** | 领域驱动设计，代码结构清晰可维护 |
| 🧪 **TDD 开发** | 测试驱动开发，保证代码质量 |
| 🛡️ **错误处理** | 完善的异常体系和错误恢复机制 |
| ⚡ **并发优化** | 支持并发请求和速率限制 |
| 📊 **数据分析** | 内置数据分析和趋势发现功能 |
| 🤖 **自动化** | 支持机器人和自动化任务 |

## 🚀 快速开始

### 安装

```bash
pip install pycodemao
```

### 基础使用

```python
import asyncio
import pycodemao

async def main():
    # 创建客户端
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # 获取用户信息
        user = await client.get_user("编程猫小王子")
        print(f"👤 用户: {user.nickname}, 等级: {user.level}")
        
        # 创建作品
        work = await client.create_work(
            title="我的Python程序",
            content="print('Hello, CodeMao!')",
            work_type="python"
        )
        print(f"🎨 作品创建成功: {work.title}")
        
        # 点赞作品
        await client.like_work(work.id)
        print("❤️ 作品已点赞")
        
    finally:
        await client.close()

# 运行示例
asyncio.run(main())
```

### 高级用法

```python
import asyncio
import pycodemao

async def advanced_example():
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # 并发获取多个用户信息
        usernames = ["编程猫小王子", "Python大师", "代码小能手"]
        users = await asyncio.gather(*[
            client.get_user(username) for username in usernames
        ])
        
        # 批量创建作品
        works = await asyncio.gather(*[
            client.create_work(
                title=f"并发作品 {i}",
                content=f"print('Hello {i}')",
                work_type="python"
            ) for i in range(1, 6)
        ])
        
        # 数据分析
        analyzer = pycodemao.CodeMaoAnalyzer(client)
        stats = await analyzer.analyze_user_activity("编程猫小王子", days=30)
        
        print(f"📊 分析结果: {stats['activity_level']} 活跃度")
        
    finally:
        await client.close()

asyncio.run(advanced_example())
```

## 📚 详细文档

### 客户端初始化

```python
import pycodemao

# 基础初始化
client = pycodemao.create_client("your_api_key_here")

# 自定义配置
client = pycodemao.CodeMaoClient(
    api_key="your_api_key_here",
    base_url="https://api.codemao.net",
    timeout=30,
    max_retries=3
)
```

### 用户管理

```python
# 获取用户信息
user = await client.get_user("username")

# 更新用户资料
await client.update_user_profile(
    nickname="新昵称",
    description="个人简介"
)

# 关注用户
await client.follow_user("username")

# 获取用户作品
works = await client.get_user_works("username", page=1, limit=10)
```

### 作品管理

```python
# 创建作品
work = await client.create_work(
    title="作品标题",
    content="print('Hello World')",
    work_type="python",
    tags=["标签1", "标签2"]
)

# 获取作品详情
work_detail = await client.get_work(work_id)

# 搜索作品
results = await client.search_works(
    query="python",
    sort_by="likes",
    limit=20
)

# 点赞作品
await client.like_work(work_id)

# 评论作品
await client.comment_work(work_id, "很棒的作品！")
```

### 论坛互动

```python
# 获取论坛板块
boards = await client.get_forum_boards()

# 创建帖子
post = await client.create_post(
    title="帖子标题",
    content="帖子内容",
    board_id=boards[0].id
)

# 回复帖子
await client.reply_post(post_id, "回复内容")

# 获取帖子列表
posts = await client.get_board_posts(board_id, page=1)
```

### 高级功能

```python
# 数据分析
analyzer = pycodemao.CodeMaoAnalyzer(client)
stats = await analyzer.analyze_user_activity("username", days=30)
trending = await analyzer.find_trending_keywords(limit=100)

# 自动化机器人
bot = pycodemao.CodeMaoBot(client)
await bot.auto_like_mentor_works("mentor_username", limit=10)
await bot.auto_follow_similar_users("target_user", limit=5)
```

## 🏗️ 架构设计

### 项目结构

```
pycodemao/
├── __init__.py           # 包入口和便利函数
├── client.py            # 主要客户端类
├── models/              # 数据模型
│   └── __init__.py
├── exceptions/          # 自定义异常
│   └── __init__.py
├── utils/               # 工具函数
│   └── __init__.py
└── _version.py          # 版本信息
```

### 核心组件

- **CodeMaoClient**: 主客户端类，提供所有API接口
- **数据模型**: 基于Pydantic的类型安全模型
- **异常体系**: 细粒度的错误处理和恢复
- **工具模块**: 重试、速率限制、验证等功能

### 设计原则

- **领域驱动设计 (DDD)**: 清晰的领域边界和业务逻辑分离
- **测试驱动开发 (TDD)**: 高覆盖率的自动化测试
- **类型安全**: 完整的类型注解和静态检查
- **异步优先**: 基于asyncio的高性能设计
- **错误恢复**: 健壮的错误处理和重试机制

## 🧪 测试

运行测试套件：

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_client.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 类型检查
mypy src/

# 代码格式化检查
black src/
isort src/
```

## 📖 示例

项目包含丰富的示例代码：

- [`examples/quick_start.py`](./examples/quick_start.py) - 快速入门示例
- [`examples/basic_examples.py`](./examples/basic_examples.py) - 基础用法示例
- [`examples/advanced_examples.py`](./examples/advanced_examples.py) - 高级功能示例

运行示例：

```bash
# 运行快速入门示例
python examples/quick_start.py

# 运行高级示例
python examples/advanced_examples.py
```

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/your-username/pycodemao.git
cd pycodemao

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest

# 代码格式化
black src/
isort src/
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [编程猫](https://www.codemao.cn/) 提供优秀的编程教育平台
- [Python](https://www.python.org/) 社区提供强大的编程语言
- 所有贡献者和支持者

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 📧 邮箱: support@pycodemao.com
- 💬 Discord: [PyCodeMao Community](https://discord.gg/pycodemao)
- 🐛 问题反馈: [GitHub Issues](https://github.com/your-username/pycodemao/issues)

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！

Made with ❤️ by the PyCodeMao Team