# 快速入门指南

## 安装

### 使用 pip 安装

```bash
pip install pycodemao
```

### 从源码安装

```bash
git clone https://github.com/your-username/pycodemao.git
cd pycodemao
pip install -e .
```

### 开发安装

```bash
git clone https://github.com/your-username/pycodemao.git
cd pycodemao
pip install -e ".[dev]"
```

## 基本使用

### 1. 创建客户端

```python
import asyncio
from pycodemao import create_client

async def main():
    # 创建客户端
    client = create_client("your_api_key_here")
    
    # 使用完毕后关闭客户端
    await client.close()

# 运行异步函数
asyncio.run(main())
```

### 2. 使用上下文管理器

```python
import asyncio
from pycodemao import create_client

async def main():
    # 使用上下文管理器自动管理连接
    async with create_client("your_api_key_here") as client:
        # 在这里使用客户端
        pass

asyncio.run(main())
```

### 3. 获取用户信息

```python
import asyncio
from pycodemao import create_client, UserNotFoundError

async def main():
    async with create_client("your_api_key_here") as client:
        try:
            # 获取用户信息
            user = await client.get_user("test_user")
            
            print(f"用户名: {user.username}")
            print(f"昵称: {user.nickname}")
            print(f"等级: {user.level}")
            print(f"粉丝数: {user.followers}")
            print(f"作品数: {user.works}")
            print(f"创建时间: {user.created_at}")
            
        except UserNotFoundError:
            print("用户未找到")
        except Exception as e:
            print(f"发生错误: {e}")

asyncio.run(main())
```

### 4. 创建作品

```python
import asyncio
from pycodemao import create_client

async def main():
    async with create_client("your_api_key_here") as client:
        # 创建新作品
        work = await client.create_work(
            title="我的第一个Python程序",
            content="print('Hello, CodeMao!')",
            work_type="python",
            tags=["python", "tutorial", "beginner"],
            description="这是一个简单的Python程序"
        )
        
        print(f"作品创建成功！")
        print(f"作品ID: {work.id}")
        print(f"标题: {work.title}")
        print(f"类型: {work.work_type}")
        print(f"点赞数: {work.likes}")
        print(f"查看数: {work.views}")
        print(f"创建时间: {work.created_at}")

asyncio.run(main())
```

### 5. 搜索作品

```python
import asyncio
from pycodemao import create_client

async def main():
    async with create_client("your_api_key_here") as client:
        # 搜索作品
        results = await client.list_works(
            work_type="python",
            page=1,
            per_page=10,
            sort_by="likes",
            sort_order="desc"
        )
        
        print(f"找到 {results.total} 个作品")
        print(f"当前第 {results.page} 页，共 {results.total_pages} 页")
        
        for work in results.items:
            print(f"\n作品ID: {work.id}")
            print(f"标题: {work.title}")
            print(f"作者: {work.author_name}")
            print(f"点赞数: {work.likes}")
            print(f"查看数: {work.views}")
            print(f"标签: {', '.join(work.tags)}")

asyncio.run(main())
```

### 6. 论坛互动

```python
import asyncio
from pycodemao import create_client

async def main():
    async with create_client("your_api_key_here") as client:
        # 获取论坛板块
        boards = await client.list_forum_boards()
        
        print("可用的论坛板块:")
        for board in boards.items:
            print(f"- {board.name} (ID: {board.id})")
            print(f"  描述: {board.description}")
            print(f"  帖子数: {board.post_count}")
        
        # 创建帖子
        if boards.items:
            first_board = boards.items[0]
            post = await client.create_post(
                title="Python学习心得分享",
                content="""
                大家好！我想分享一些学习Python的心得：
                
                1. 从基础语法开始
                2. 多练习，多写代码
                3. 参与开源项目
                4. 加入社区讨论
                
                希望对大家有帮助！
                """,
                board_id=first_board.id,
                tags=["python", "learning", "sharing"]
            )
            
            print(f"\n帖子创建成功！")
            print(f"帖子ID: {post.id}")
            print(f"标题: {post.title}")
            print(f"板块: {post.board_name}")
            print(f"点赞数: {post.likes}")
            print(f"回复数: {post.replies}")

asyncio.run(main())
```

### 7. 错误处理

```python
import asyncio
from pycodemao import (
    create_client,
    UserNotFoundError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

async def main():
    try:
        async with create_client("your_api_key_here") as client:
            # 尝试获取不存在的用户
            user = await client.get_user("non_existent_user")
            
    except UserNotFoundError as e:
        print(f"用户未找到: {e}")
        
    except AuthenticationError as e:
        print(f"认证失败: {e}")
        print("请检查你的API密钥是否正确")
        
    except RateLimitError as e:
        print(f"速率限制: {e}")
        print("请稍后再试")
        
    except ValidationError as e:
        print(f"参数验证失败: {e}")
        
    except Exception as e:
        print(f"发生未知错误: {e}")

asyncio.run(main())
```

### 8. 并发操作

```python
import asyncio
from pycodemao import create_client

async def fetch_user_data(client, username):
    """获取用户数据"""
    try:
        user = await client.get_user(username)
        works = await client.list_works(user_id=user.id, per_page=5)
        return {
            "user": user,
            "works": works.items,
            "work_count": len(works.items)
        }
    except Exception as e:
        return {"error": str(e), "username": username}

async def main():
    async with create_client("your_api_key_here") as client:
        # 要查询的用户列表
        usernames = ["user1", "user2", "user3", "user4", "user5"]
        
        # 并发获取所有用户数据
        tasks = [fetch_user_data(client, username) for username in usernames]
        results = await asyncio.gather(*tasks)
        
        # 处理结果
        for result in results:
            if "error" in result:
                print(f"获取 {result['username']} 失败: {result['error']}")
            else:
                user = result["user"]
                print(f"\n用户: {user.username}")
                print(f"等级: {user.level}")
                print(f"作品数: {result['work_count']}")
                
                if result["works"]:
                    print("最新作品:")
                    for work in result["works"][:3]:  # 显示前3个作品
                        print(f"  - {work.title} (点赞: {work.likes})")

asyncio.run(main())
```

### 9. 速率限制处理

```python
import asyncio
import time
from pycodemao import create_client, RateLimitError

async def main():
    async with create_client("your_api_key_here") as client:
        request_count = 0
        
        for i in range(20):  # 尝试20个请求
            try:
                # 获取速率限制状态
                rate_status = await client.get_rate_limit_status()
                print(f"速率限制状态: {rate_status}")
                
                # 执行请求
                user = await client.get_user(f"test_user_{i}")
                request_count += 1
                print(f"请求 {request_count}: 成功获取 {user.username}")
                
            except RateLimitError as e:
                print(f"遇到速率限制: {e}")
                print("等待5秒后重试...")
                await asyncio.sleep(5)
                
                # 重试一次
                try:
                    user = await client.get_user(f"test_user_{i}")
                    request_count += 1
                    print(f"重试成功: {user.username}")
                except RateLimitError:
                    print("重试仍然失败，跳过后续请求")
                    break
            
            # 小延迟避免过快请求
            await asyncio.sleep(0.1)
        
        print(f"\n总共完成 {request_count} 个请求")

asyncio.run(main())
```

## 高级功能

### 自定义超时和重试

```python
import asyncio
from pycodemao import CodeMaoClient

async def main():
    # 创建自定义配置的客户端
    client = CodeMaoClient(
        api_key="your_api_key_here",
        timeout=60,          # 60秒超时
        max_retries=5,       # 最多重试5次
        retry_delay=2.0      # 重试延迟2秒
    )
    
    try:
        user = await client.get_user("test_user")
        print(f"用户: {user.username}")
        
    finally:
        await client.close()

asyncio.run(main())
```

### 使用自定义会话

```python
import asyncio
import aiohttp
from pycodemao import CodeMaoClient

async def main():
    # 创建自定义会话
    connector = aiohttp.TCPConnector(
        limit=100,              # 总连接数限制
        limit_per_host=30,      # 单主机连接数限制
        ttl_dns_cache=300,      # DNS缓存时间
        use_dns_cache=True,     # 启用DNS缓存
    )
    
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:
        
        # 使用自定义会话创建客户端
        client = CodeMaoClient(
            api_key="your_api_key_here",
            session=session
        )
        
        user = await client.get_user("test_user")
        print(f"用户: {user.username}")
        
        # 会话会在退出上下文时自动关闭

asyncio.run(main())
```

## 最佳实践

### 1. 错误处理

```python
import asyncio
from pycodemao import create_client, CodeMaoError

async def safe_api_call(client, func, *args, **kwargs):
    """安全的API调用包装"""
    try:
        return await func(*args, **kwargs)
    except CodeMaoError as e:
        print(f"CodeMao API错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

async def main():
    async with create_client("your_api_key_here") as client:
        # 安全地获取用户信息
        user = await safe_api_call(client, client.get_user, "test_user")
        if user:
            print(f"用户: {user.username}")
        
        # 安全地创建作品
        work = await safe_api_call(
            client,
            client.create_work,
            title="测试作品",
            content="print('test')",
            work_type="python"
        )
        if work:
            print(f"作品创建成功: {work.id}")

asyncio.run(main())
```

### 2. 日志记录

```python
import asyncio
import logging
from pycodemao import create_client

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    logger.info("开始CodeMao SDK示例")
    
    async with create_client("your_api_key_here") as client:
        try:
            logger.info("获取用户信息...")
            user = await client.get_user("test_user")
            logger.info(f"成功获取用户: {user.username}")
            
            logger.info("创建作品...")
            work = await client.create_work(
                title="日志测试作品",
                content="print('Hello from logging!')",
                work_type="python"
            )
            logger.info(f"作品创建成功: {work.id}")
            
        except Exception as e:
            logger.error(f"操作失败: {e}")
            raise

asyncio.run(main())
```

### 3. 配置管理

```python
import os
import asyncio
from pycodemao import create_client

# 从环境变量获取配置
API_KEY = os.getenv("CODEMAO_API_KEY")
if not API_KEY:
    raise ValueError("请设置 CODEMAO_API_KEY 环境变量")

# 可选配置
TIMEOUT = int(os.getenv("CODEMAO_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("CODEMAO_MAX_RETRIES", "3"))
RETRY_DELAY = float(os.getenv("CODEMAO_RETRY_DELAY", "1.0"))

async def main():
    # 使用环境变量配置创建客户端
    client = create_client(
        api_key=API_KEY,
        timeout=TIMEOUT,
        max_retries=MAX_RETRIES,
        retry_delay=RETRY_DELAY
    )
    
    try:
        user = await client.get_user("test_user")
        print(f"用户: {user.username}")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```