# 📚 CodeMao SDK 文档

欢迎使用 CodeMao SDK 文档！这里是您开始使用我们的 SDK 所需的一切信息。

## 🚀 快速开始

### 安装

```bash
pip install codemao-sdk
```

### 基本使用

```python
from codemaokit import CodeMaoClient

# 创建客户端
client = CodeMaoClient()

# 登录
client.login("your_username", "your_password")

# 获取用户信息
user_info = client.get_user_info()
print(f"欢迎, {user_info.nickname}!")
```

## 📖 文档结构

### [用户指南](user-guide.md)
- SDK 安装和配置
- 认证和用户管理
- 板块和帖子操作
- 高级功能使用

### [API 参考](api-reference.md)
- 完整的 API 文档
- 所有类和方法的详细说明
- 代码示例

### [示例代码](examples.md)
- 常见用例的完整示例
- 最佳实践
- 故障排除

### [贡献指南](../CONTRIBUTING.md)
- 如何为项目做贡献
- 开发环境设置
- 代码风格指南

## 🎯 核心功能

### 🔐 用户认证
- 用户名/密码登录
- 自动会话管理
- 用户信息获取和更新

### 📋 板块管理
- 获取所有板块
- 按 ID 或名称查找板块
- 板块信息统计

### 📝 帖子操作
- 创建新帖子
- 回复帖子
- 删除帖子
- 帖子搜索和过滤

### 📊 数据统计
- 消息统计
- 用户活跃度
- 作品分析

## 🔧 高级功能

### 🔄 异步支持
```python
import asyncio
from codemaokit import AsyncCodeMaoClient

async def main():
    async with AsyncCodeMaoClient() as client:
        await client.login("username", "password")
        # 异步操作...

asyncio.run(main())
```

### 🛡️ 错误处理
```python
from codemaokit import CodeMaoError, AuthenticationError

try:
    client.login("username", "wrong_password")
except AuthenticationError as e:
    print(f"登录失败: {e}")
except CodeMaoError as e:
    print(f"SDK 错误: {e}")
```

### ⚙️ 配置选项
```python
from codemaokit import CodeMaoClient

client = CodeMaoClient(
    timeout=30,  # 请求超时时间
    max_retries=3,  # 最大重试次数
    user_agent="MyApp/1.0"  # 自定义 User-Agent
)
```

## 📊 性能优化

### 连接池
```python
from codemaokit import CodeMaoClient

# 使用连接池提高性能
client = CodeMaoClient(
    connection_pool_size=10,
    connection_pool_maxsize=20
)
```

### 批量操作
```python
# 批量获取用户信息
user_ids = [1, 2, 3, 4, 5]
users = client.get_users_batch(user_ids)
```

## 🔍 调试和监控

### 日志配置
```python
import logging

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('codemaokit')
logger.setLevel(logging.DEBUG)
```

### 性能监控
```python
import time

start = time.time()
result = client.some_operation()
end = time.time()

print(f"操作耗时: {end - start:.2f}秒")
```

## 🆘 获取帮助

### 遇到问题？

1. **查看文档** - 确保您已阅读相关文档
2. **搜索 Issues** - 查看是否有人遇到类似问题
3. **提问** - 在 [GitHub Discussions](https://github.com/nichengfuben/codemao-sdk-for-python/discussions) 提问
4. **报告 Bug** - 在 [GitHub Issues](https://github.com/nichengfuben/codemao-sdk-for-python/issues) 报告

### 联系方式

- 📧 邮件: [contact@codemao-sdk.com](mailto:contact@codemao-sdk.com)
- 💬 Discord: [加入我们的 Discord](https://discord.gg/codemao-sdk)
- 🐦 Twitter: [@codemao_sdk](https://twitter.com/codemao_sdk)

## 📈 版本历史

查看 [CHANGELOG.md](../CHANGELOG.md) 了解完整的版本历史。

## 🎉 致谢

感谢所有 [贡献者](https://github.com/nichengfuben/codemao-sdk-for-python/graphs/contributors) 让这个项目变得更好！

---

**准备好了吗？** 开始探索 [用户指南](user-guide.md) 吧！