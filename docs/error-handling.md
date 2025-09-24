# 🐛 错误处理指南

CodeMao SDK 提供了完善的错误处理机制，帮助您更好地调试和处理各种异常情况。

## 📋 异常层次结构

```
CodeMaoError (基类)
├── AuthenticationError     # 认证相关错误
├── APIError               # API 请求错误
├── ValidationError        # 数据验证错误
├── RateLimitError         # 速率限制错误
├── NetworkError           # 网络连接错误
├── ResourceNotFoundError  # 资源未找到错误
└── ServerError            # 服务器内部错误
```

## 🔍 常见错误场景

### 1. 认证错误 (AuthenticationError)

```python
from codemaokit import CodeMaoClient
from codemaokit.exceptions import AuthenticationError

def safe_login():
    client = CodeMaoClient()
    
    try:
        # 尝试登录
        success = client.login("wrong_username", "wrong_password")
        
        if not success:
            print("❌ 登录失败：用户名或密码错误")
            
    except AuthenticationError as e:
        # 处理认证错误
        print(f"🔒 认证错误详情:")
        print(f"   错误消息: {e.message}")
        print(f"   错误代码: {e.error_code}")
        print(f"   建议操作: 检查用户名和密码是否正确")
        
        # 根据错误代码采取不同措施
        if e.error_code == "INVALID_CREDENTIALS":
            print("   💡 提示: 请确认您的登录凭据")
        elif e.error_code == "ACCOUNT_LOCKED":
            print("   💡 提示: 账户已被锁定，请联系客服")
        elif e.error_code == "VERIFICATION_REQUIRED":
            print("   💡 提示: 需要进行额外的安全验证")
```

### 2. API 错误 (APIError)

```python
from codemaokit import CodeMaoClient
from codemaokit.exceptions import APIError

def handle_api_errors():
    client = CodeMaoClient()
    
    try:
        client.login("valid_user", "valid_password")
        
        # 尝试获取不存在的用户
        user_info = client.get_user_info(user_id=999999)
        
    except APIError as e:
        print(f"🌐 API 错误详情:")
        print(f"   状态码: {e.status_code}")
        print(f"   错误消息: {e.message}")
        print(f"   请求URL: {e.response_data.get('url', '未知')}")
        
        # 根据HTTP状态码处理
        if e.status_code == 404:
            print("   💡 提示: 请求的资源不存在")
        elif e.status_code == 403:
            print("   💡 提示: 没有权限访问此资源")
        elif e.status_code == 429:
            print("   💡 提示: 请求过于频繁，请稍后再试")
        elif e.status_code >= 500:
            print("   💡 提示: 服务器内部错误，请稍后重试")
        
        # 查看响应数据
        if e.response_data:
            print(f"   响应数据: {e.response_data}")
```

### 3. 网络错误 (NetworkError)

```python
import time
from codemaokit import CodeMaoClient
from codemaokit.exceptions import NetworkError

def handle_network_errors():
    client = CodeMaoClient(timeout=10)  # 设置较短的超时时间
    
    max_retries = 3
    retry_delay = 2  # 秒
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 尝试连接 (第 {attempt + 1} 次)...")
            client.login("user", "password")
            print("✅ 连接成功!")
            break
            
        except NetworkError as e:
            print(f"🌐 网络错误: {e.message}")
            
            if attempt < max_retries - 1:
                print(f"⏰ {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                retry_delay *= 2  # 指数退避
            else:
                print("❌ 已达到最大重试次数")
                
        except Exception as e:
            print(f"💥 意外错误: {e}")
            break
```

### 4. 速率限制错误 (RateLimitError)

```python
import time
from codemaokit import CodeMaoClient
from codemaokit.exceptions import RateLimitError

def handle_rate_limit():
    client = CodeMaoClient()
    client.login("user", "password")
    
    request_count = 0
    
    while True:
        try:
            # 执行API请求
            posts = client.get_board_posts(board_id=1, limit=10)
            request_count += 1
            
            print(f"✅ 成功获取 {len(posts)} 个帖子 (请求 #{request_count})")
            
            # 处理帖子数据
            for post in posts:
                print(f"   - {post.title}")
            
            # 添加小延迟，避免触发速率限制
            time.sleep(0.5)
            
        except RateLimitError as e:
            print(f"⏰ 触发速率限制!")
            print(f"   需要等待: {e.retry_after} 秒")
            print(f"   限制信息: {e.message}")
            
            # 等待指定时间
            if e.retry_after:
                print(f"💤 等待 {e.retry_after} 秒...")
                time.sleep(e.retry_after)
                print("🔄 继续执行...")
            else:
                # 如果没有指定等待时间，使用默认退避策略
                wait_time = 60  # 默认等待1分钟
                print(f"💤 等待 {wait_time} 秒...")
                time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("\n🛑 用户停止")
            break
        except Exception as e:
            print(f"💥 错误: {e}")
            break
```

## 🛡️ 最佳实践

### 1. 统一的错误处理装饰器

```python
from functools import wraps
from codemaokit.exceptions import CodeMaoError
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(func):
    """统一的错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CodeMaoError as e:
            # 记录错误日志
            logger.error(f"CodeMao错误 in {func.__name__}: {e}")
            
            # 根据错误类型返回适当的错误信息
            if isinstance(e, AuthenticationError):
                return {"error": "认证失败", "code": "AUTH_FAILED"}
            elif isinstance(e, RateLimitError):
                return {"error": "请求过于频繁", "retry_after": e.retry_after}
            elif isinstance(e, NetworkError):
                return {"error": "网络连接失败", "code": "NETWORK_ERROR"}
            else:
                return {"error": "API错误", "message": str(e)}
                
        except Exception as e:
            # 处理非CodeMao错误
            logger.error(f"意外错误 in {func.__name__}: {e}")
            return {"error": "内部错误", "message": str(e)}
    
    return wrapper

# 使用装饰器
@handle_errors
def get_user_data(client, user_id):
    """获取用户数据（带错误处理）"""
    user_info = client.get_user_info(user_id)
    return {"success": True, "data": user_info}

@handle_errors
def create_post_safe(client, board_id, title, content):
    """安全地创建帖子"""
    post = client.create_post(board_id, title, content)
    return {"success": True, "post_id": post.id}
```

### 2. 重试机制

```python
import time
from functools import wraps
from codemaokit.exceptions import NetworkError, RateLimitError

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except (NetworkError, RateLimitError) as e:
                    if attempt == max_retries - 1:
                        # 最后一次尝试失败，抛出异常
                        raise
                    
                    print(f"🔄 尝试 {attempt + 1} 失败，{current_delay} 秒后重试...")
                    time.sleep(current_delay)
                    current_delay *= backoff  # 指数退避
                    
                except Exception as e:
                    # 其他异常不重试
                    raise
            
            return None
        
        return wrapper
    return decorator

# 使用重试装饰器
@retry_on_failure(max_retries=3, delay=2)
def fetch_user_with_retry(client, user_id):
    """获取用户信息（带重试）"""
    return client.get_user_info(user_id)
```

### 3. 错误日志记录

```python
import logging
import traceback
from datetime import datetime
from codemaokit.exceptions import CodeMaoError

class ErrorLogger:
    """错误日志记录器"""
    
    def __init__(self, log_file="codemao_errors.log"):
        self.logger = logging.getLogger("CodeMaoErrorLogger")
        self.logger.setLevel(logging.ERROR)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_error(self, error, context=None):
        """记录错误信息"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "traceback": traceback.format_exc() if not isinstance(error, CodeMaoError) else None
        }
        
        if isinstance(error, CodeMaoError):
            error_info.update({
                "error_code": getattr(error, 'error_code', None),
                "status_code": getattr(error, 'status_code', None),
                "response_data": getattr(error, 'response_data', None)
            })
        
        # 记录到文件
        self.logger.error(f"CodeMao错误: {error_info}")
        
        # 控制台输出简要信息
        print(f"❌ 错误已记录: {type(error).__name__}: {error}")
        
        return error_info

# 使用示例
error_logger = ErrorLogger()

def safe_api_call(func_name, func, *args, **kwargs):
    """安全的API调用包装"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        context = {
            "function": func_name,
            "args": args,
            "kwargs": kwargs
        }
        error_logger.log_error(e, context)
        return None

# 使用示例
client = CodeMaoClient()
result = safe_api_call("login", client.login, "username", "password")
```

## 🔧 调试技巧

### 1. 启用详细日志

```python
import logging
from codemaokit import CodeMaoClient

# 启用详细日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建客户端并启用调试模式
client = CodeMaoClient(debug=True)

# 现在所有的API请求和响应都会被记录
client.login("username", "password")
```

### 2. 网络请求调试

```python
from codemaokit import CodeMaoClient
import requests

# 启用请求调试
client = CodeMaoClient()

# 打印请求详情
def debug_request_hook(response, *args, **kwargs):
    print(f"📤 请求: {response.request.method} {response.request.url}")
    print(f"📥 响应: {response.status_code} {response.reason}")
    print(f"📄 响应头: {dict(response.headers)}")
    if response.text:
        print(f"📝 响应体: {response.text[:200]}...")  # 只显示前200字符

# 添加调试钩子
client.session.hooks['response'].append(debug_request_hook)

# 执行请求
client.login("username", "password")
```

### 3. 性能监控

```python
import time
from functools import wraps
from codemaokit import CodeMaoClient

def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"⏱️ {func.__name__} 执行时间: {duration:.3f} 秒")
            
            if duration > 5.0:  # 超过5秒的请求
                print(f"⚠️ 警告: {func.__name__} 执行时间过长")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"❌ {func.__name__} 失败 (耗时: {duration:.3f} 秒): {e}")
            raise
    
    return wrapper

# 使用性能监控
@performance_monitor
def fetch_posts_with_monitoring(client, board_id):
    return client.get_board_posts(board_id, limit=50)

# 使用示例
client = CodeMaoClient()
client.login("user", "password")
posts = fetch_posts_with_monitoring(client, 1)
```

## 📊 错误统计和分析

```python
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json

class ErrorAnalyzer:
    """错误分析器"""
    
    def __init__(self):
        self.errors = []
    
    def add_error(self, error, context=None):
        """添加错误记录"""
        error_record = {
            "timestamp": datetime.now(),
            "type": type(error).__name__,
            "message": str(error),
            "context": context or {}
        }
        
        if hasattr(error, 'status_code'):
            error_record["status_code"] = error.status_code
        if hasattr(error, 'error_code'):
            error_record["error_code"] = error.error_code
            
        self.errors.append(error_record)
    
    def get_statistics(self, hours=24):
        """获取错误统计"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self.errors if e["timestamp"] > cutoff_time]
        
        if not recent_errors:
            return {"message": "最近24小时没有错误"}
        
        # 错误类型统计
        error_types = Counter(e["type"] for e in recent_errors)
        
        # HTTP状态码统计
        status_codes = Counter(
            e["status_code"] for e in recent_errors 
            if "status_code" in e
        )
        
        # 错误趋势（按小时）
        hourly_errors = defaultdict(int)
        for error in recent_errors:
            hour = error["timestamp"].strftime("%Y-%m-%d %H:00")
            hourly_errors[hour] += 1
        
        return {
            "total_errors": len(recent_errors),
            "error_types": dict(error_types),
            "status_codes": dict(status_codes),
            "hourly_trend": dict(hourly_errors),
            "most_common_errors": error_types.most_common(5)
        }
    
    def generate_report(self):
        """生成错误报告"""
        stats = self.get_statistics()
        
        report = f"""
# CodeMao SDK 错误分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 统计摘要
- 总错误数: {stats.get('total_errors', 0)}
- 监控时间段: 最近24小时

## 错误类型分布
"""
        
        for error_type, count in stats.get('error_types', {}).items():
            report += f"- {error_type}: {count} 次\n"
        
        if stats.get('status_codes'):
            report += "\n## HTTP状态码分布\n"
            for status_code, count in stats['status_codes'].items():
                report += f"- {status_code}: {count} 次\n"
        
        if stats.get('most_common_errors'):
            report += "\n## 最常见的错误\n"
            for error_type, count in stats['most_common_errors']:
                report += f"1. {error_type}: {count} 次\n"
        
        return report

# 使用示例
error_analyzer = ErrorAnalyzer()

# 在代码中添加错误记录
try:
    client.login("user", "password")
except Exception as e:
    error_analyzer.add_error(e, {"operation": "login"})

# 生成报告
report = error_analyzer.generate_report()
print(report)
```

## 🚨 常见错误及解决方案

| 错误类型 | 常见原因 | 解决方案 |
|---------|---------|----------|
| `AuthenticationError` | 用户名/密码错误 | 检查登录凭据，确认账户状态 |
| `NetworkError` | 网络连接问题 | 检查网络连接，设置合适的超时时间 |
| `RateLimitError` | 请求过于频繁 | 降低请求频率，实现指数退避重试 |
| `ValidationError` | 参数格式错误 | 检查输入参数，使用验证函数 |
| `ResourceNotFoundError` | 资源不存在 | 确认资源ID是否正确 |
| `ServerError` | 服务器内部错误 | 稍后重试，联系技术支持 |

---

**记住**: 良好的错误处理是稳定应用的基础！始终为您的代码添加适当的错误处理机制。