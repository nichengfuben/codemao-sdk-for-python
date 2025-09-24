# 💡 示例代码

这里提供了丰富的示例代码，帮助您快速上手 CodeMao SDK。

## 🚀 基础示例

### 1. 完整的登录流程

```python
from codemaokit import CodeMaoClient
from codemaokit.exceptions import AuthenticationError, APIError

def main():
    # 创建客户端
    client = CodeMaoClient()
    
    try:
        # 尝试登录
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        
        if client.login(username, password):
            print("✅ 登录成功!")
            
            # 获取用户信息
            user_info = client.get_user_info()
            print(f"👋 欢迎, {user_info.nickname}!")
            print(f"📊 等级: {user_info.level}")
            print(f"👥 粉丝数: {user_info.followers_count}")
            print(f"📝 发帖数: {user_info.posts_count}")
            
        else:
            print("❌ 登录失败")
            
    except AuthenticationError as e:
        print(f"🔒 认证错误: {e.message}")
    except APIError as e:
        print(f"🌐 API 错误: {e.status_code} - {e.message}")
    except Exception as e:
        print(f"💥 意外错误: {e}")
    finally:
        # 确保登出
        client.logout()

if __name__ == "__main__":
    main()
```

### 2. 板块浏览和帖子发布

```python
from codemaokit import CodeMaoClient

def browse_and_post():
    client = CodeMaoClient()
    
    try:
        # 登录
        client.login("your_username", "your_password")
        
        # 获取所有板块
        print("📋 可用板块:")
        boards = client.get_boards()
        for i, board in enumerate(boards, 1):
            print(f"{i}. {board.name} - {board.description}")
            print(f"   💬 帖子数: {board.post_count}")
        
        # 选择板块
        board_choice = int(input("\n选择板块编号: ")) - 1
        if 0 <= board_choice < len(boards):
            selected_board = boards[board_choice]
            print(f"\n✅ 选择了板块: {selected_board.name}")
            
            # 显示该板块的热门帖子
            print(f"\n🔥 {selected_board.name} 的热门帖子:")
            posts = client.get_board_posts(
                selected_board.id, 
                sort_by="likes", 
                limit=5
            )
            
            for post in posts:
                print(f"• {post.title} (👍 {post.likes} | 💬 {post.replies})")
                print(f"  作者: {post.author.nickname}")
                print()
            
            # 创建新帖子
            create_post = input("是否创建新帖子? (y/n): ").lower()
            if create_post == 'y':
                title = input("帖子标题: ")
                content = input("帖子内容: ")
                
                new_post = client.create_post(
                    board_id=selected_board.id,
                    title=title,
                    content=content,
                    tags=["讨论", "分享"]
                )
                
                print(f"✅ 帖子创建成功! ID: {new_post.id}")
                
    finally:
        client.logout()

if __name__ == "__main__":
    browse_and_post()
```

### 3. 用户作品分析

```python
from codemaokit import CodeMaoClient
import matplotlib.pyplot as plt
from collections import Counter

def analyze_user_works():
    client = CodeMaoClient()
    
    try:
        client.login("your_username", "your_password")
        
        # 获取目标用户信息
        target_user_id = int(input("输入要分析的用户ID: "))
        
        # 获取用户作品
        works = client.get_user_works(target_user_id, limit=50)
        
        if not works:
            print("该用户没有作品")
            return
        
        print(f"📊 找到 {len(works)} 个作品")
        
        # 分析数据
        work_types = Counter()
        likes_data = []
        views_data = []
        dates_data = []
        
        for work in works:
            work_types[work.type] += 1
            likes_data.append(work.likes)
            views_data.append(work.views)
            dates_data.append(work.created_at)
        
        # 显示统计信息
        print(f"\n📈 作品类型分布:")
        for work_type, count in work_types.items():
            print(f"  {work_type}: {count} 个")
        
        print(f"\n📊 互动数据统计:")
        print(f"  总点赞数: {sum(likes_data)}")
        print(f"  总浏览数: {sum(views_data)}")
        print(f"  平均点赞数: {sum(likes_data) / len(likes_data):.1f}")
        print(f"  平均浏览数: {sum(views_data) / len(views_data):.1f}")
        
        # 可视化数据（可选）
        try:
            plt.figure(figsize=(12, 8))
            
            # 子图1: 作品类型分布
            plt.subplot(2, 2, 1)
            plt.pie(work_types.values(), labels=work_types.keys(), autopct='%1.1f%%')
            plt.title('作品类型分布')
            
            # 子图2: 点赞数分布
            plt.subplot(2, 2, 2)
            plt.hist(likes_data, bins=10, alpha=0.7)
            plt.title('点赞数分布')
            plt.xlabel('点赞数')
            plt.ylabel('作品数')
            
            # 子图3: 浏览数 vs 点赞数
            plt.subplot(2, 2, 3)
            plt.scatter(views_data, likes_data, alpha=0.6)
            plt.title('浏览数 vs 点赞数')
            plt.xlabel('浏览数')
            plt.ylabel('点赞数')
            
            # 子图4: 作品发布时间趋势
            plt.subplot(2, 2, 4)
            dates = [d.date() for d in dates_data]
            date_counts = Counter(dates)
            sorted_dates = sorted(date_counts.items())
            
            if len(sorted_dates) > 1:
                dates_list, counts_list = zip(*sorted_dates)
                plt.plot(dates_list, counts_list, marker='o')
                plt.title('作品发布趋势')
                plt.xlabel('日期')
                plt.ylabel('作品数')
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("\n💡 安装 matplotlib 可以查看数据可视化")
            
    finally:
        client.logout()

if __name__ == "__main__":
    analyze_user_works()
```

## 🔄 高级示例

### 4. 自动回复机器人

```python
from codemaokit import CodeMaoClient
import time
import random
from datetime import datetime, timedelta

class AutoReplyBot:
    def __init__(self, username, password):
        self.client = CodeMaoClient()
        self.username = username
        self.password = password
        self.replied_posts = set()  # 记录已回复的帖子
        self.reply_templates = [
            "感谢分享！这个内容很有用。",
            "学到了新知识，谢谢！",
            "很有意思的观点，支持一下！",
            "写得很好，期待更多分享。",
            "这个问题我也遇到过，感谢解答！"
        ]
    
    def login(self):
        """登录并返回是否成功"""
        try:
            return self.client.login(self.username, self.password)
        except Exception as e:
            print(f"登录失败: {e}")
            return False
    
    def get_unreplied_posts(self, board_id, hours=24):
        """获取指定时间内的未回复帖子"""
        try:
            posts = self.client.get_board_posts(board_id, limit=20)
            
            # 过滤出未回复的帖子
            unreplied = []
            for post in posts:
                if post.id not in self.replied_posts:
                    # 检查发布时间是否在指定时间内
                    post_time = post.created_at
                    if datetime.now() - post_time < timedelta(hours=hours):
                        unreplied.append(post)
            
            return unreplied
            
        except Exception as e:
            print(f"获取帖子失败: {e}")
            return []
    
    def should_reply(self, post):
        """判断是否应该回复该帖子"""
        # 简单的规则：帖子内容长度适中，有一定互动
        return (
            len(post.content) > 50 and  # 内容不要太短
            post.likes >= 1 and         # 至少有一个点赞
            post.replies < 10           # 回复数不要太多
        )
    
    def generate_reply(self, post):
        """生成回复内容"""
        # 简单策略：随机选择模板
        template = random.choice(self.reply_templates)
        
        # 可以根据帖子内容做更智能的回复
        if "python" in post.content.lower():
            return f"关于Python的内容很棒！{template}"
        elif "问题" in post.title or "求助" in post.title:
            return f"这个问题很有意思，{template}"
        else:
            return template
    
    def reply_to_post(self, post):
        """回复指定帖子"""
        try:
            reply_content = self.generate_reply(post)
            reply = self.client.reply_to_post(post.id, reply_content)
            
            # 记录已回复
            self.replied_posts.add(post.id)
            
            print(f"✅ 回复了帖子 '{post.title}' (ID: {post.id})")
            print(f"💬 回复内容: {reply_content}")
            
            return True
            
        except Exception as e:
            print(f"回复失败: {e}")
            return False
    
    def run(self, board_id, interval_minutes=30, max_replies_per_session=5):
        """运行机器人"""
        print(f"🤖 自动回复机器人启动")
        print(f"⏰ 检查间隔: {interval_minutes} 分钟")
        print(f"📊 最大回复数: {max_replies_per_session}")
        
        if not self.login():
            print("❌ 登录失败，机器人停止")
            return
        
        reply_count = 0
        
        try:
            while reply_count < max_replies_per_session:
                print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] 检查新帖子...")
                
                # 获取未回复的帖子
                posts = self.get_unreplied_posts(board_id)
                
                if not posts:
                    print("📭 暂无合适的帖子")
                else:
                    print(f"📋 发现 {len(posts)} 个未回复帖子")
                    
                    # 尝试回复合适的帖子
                    for post in posts:
                        if self.should_reply(post):
                            if self.reply_to_post(post):
                                reply_count += 1
                                
                                # 回复后等待一段时间，避免过于频繁
                                time.sleep(random.randint(30, 90))
                                
                                if reply_count >= max_replies_per_session:
                                    break
                        
                        # 每个帖子之间也稍作等待
                        time.sleep(random.randint(5, 15))
                
                # 等待下一次检查
                if reply_count < max_replies_per_session:
                    print(f"⏰ 等待 {interval_minutes} 分钟后继续...")
                    time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 用户停止机器人")
        except Exception as e:
            print(f"💥 机器人运行出错: {e}")
        finally:
            self.client.logout()
            print(f"\n📈 本次会话共回复 {reply_count} 个帖子")
            print("👋 机器人停止")

# 使用示例
if __name__ == "__main__":
    bot = AutoReplyBot("your_username", "your_password")
    bot.run(
        board_id=123,  # 替换为实际的板块ID
        interval_minutes=30,
        max_replies_per_session=10
    )
```

### 5. 数据导出工具

```python
from codemaokit import CodeMaoClient
import json
import csv
from datetime import datetime
import os

class DataExporter:
    def __init__(self, username, password):
        self.client = CodeMaoClient()
        self.username = username
        self.password = password
        self.export_dir = f"codemao_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.export_dir, exist_ok=True)
    
    def login(self):
        """登录"""
        return self.client.login(self.username, self.password)
    
    def export_user_info(self, user_id):
        """导出用户信息"""
        try:
            user_info = self.client.get_user_info()
            
            data = {
                "user_id": user_info.id,
                "nickname": user_info.nickname,
                "level": user_info.level,
                "signature": user_info.signature,
                "followers_count": user_info.followers_count,
                "following_count": user_info.following_count,
                "posts_count": user_info.posts_count,
                "works_count": user_info.works_count,
                "created_at": user_info.created_at.isoformat(),
                "last_active_at": user_info.last_active_at.isoformat()
            }
            
            # 保存为JSON
            with open(f"{self.export_dir}/user_info.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存为CSV
            with open(f"{self.export_dir}/user_info.csv", 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writeheader()
                writer.writerow(data)
            
            print(f"✅ 用户信息导出成功")
            return data
            
        except Exception as e:
            print(f"❌ 用户信息导出失败: {e}")
            return None
    
    def export_boards(self):
        """导出所有板块信息"""
        try:
            boards = self.client.get_boards()
            
            data = []
            for board in boards:
                board_data = {
                    "board_id": board.id,
                    "name": board.name,
                    "description": board.description,
                    "post_count": board.post_count,
                    "follower_count": board.follower_count,
                    "moderator_count": board.moderator_count,
                    "created_at": board.created_at.isoformat()
                }
                data.append(board_data)
            
            # 保存为JSON
            with open(f"{self.export_dir}/boards.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存为CSV
            if data:
                with open(f"{self.export_dir}/boards.csv", 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            
            print(f"✅ 板块信息导出成功，共 {len(data)} 个板块")
            return data
            
        except Exception as e:
            print(f"❌ 板块信息导出失败: {e}")
            return []
    
    def export_posts(self, board_id, limit=100):
        """导出指定板块的帖子"""
        try:
            posts = self.client.get_board_posts(board_id, limit=limit)
            
            data = []
            for post in posts:
                post_data = {
                    "post_id": post.id,
                    "title": post.title,
                    "content": post.content[:500],  # 截取前500字符
                    "author_id": post.author.id,
                    "author_nickname": post.author.nickname,
                    "board_id": post.board.id,
                    "board_name": post.board.name,
                    "tags": ", ".join(post.tags),
                    "likes": post.likes,
                    "replies": post.replies,
                    "views": post.views,
                    "is_liked": post.is_liked,
                    "is_following": post.is_following,
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat()
                }
                data.append(post_data)
            
            # 保存为JSON
            with open(f"{self.export_dir}/posts_board_{board_id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存为CSV
            if data:
                with open(f"{self.export_dir}/posts_board_{board_id}.csv", 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            
            print(f"✅ 帖子导出成功，共 {len(data)} 个帖子")
            return data
            
        except Exception as e:
            print(f"❌ 帖子导出失败: {e}")
            return []
    
    def export_works(self, user_id, limit=50):
        """导出用户作品"""
        try:
            works = self.client.get_user_works(user_id, limit=limit)
            
            data = []
            for work in works:
                work_data = {
                    "work_id": work.id,
                    "title": work.title,
                    "description": work.description,
                    "thumbnail_url": work.thumbnail_url,
                    "type": work.type,
                    "author_id": work.author.id,
                    "author_nickname": work.author.nickname,
                    "likes": work.likes,
                    "views": work.views,
                    "comments": work.comments,
                    "is_liked": work.is_liked,
                    "created_at": work.created_at.isoformat(),
                    "updated_at": work.updated_at.isoformat()
                }
                data.append(work_data)
            
            # 保存为JSON
            with open(f"{self.export_dir}/works_user_{user_id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存为CSV
            if data:
                with open(f"{self.export_dir}/works_user_{user_id}.csv", 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            
            print(f"✅ 作品导出成功，共 {len(data)} 个作品")
            return data
            
        except Exception as e:
            print(f"❌ 作品导出失败: {e}")
            return []
    
    def generate_report(self):
        """生成导出报告"""
        report = {
            "export_time": datetime.now().isoformat(),
            "export_directory": self.export_dir,
            "files": []
        }
        
        # 统计导出的文件
        for filename in os.listdir(self.export_dir):
            filepath = os.path.join(self.export_dir, filename)
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                report["files"].append({
                    "filename": filename,
                    "size_bytes": file_size,
                    "size_human": self._format_file_size(file_size)
                })
        
        # 保存报告
        with open(f"{self.export_dir}/export_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 导出报告已生成")
        return report
    
    def _format_file_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def run_full_export(self, user_id=None, board_ids=None):
        """运行完整的数据导出"""
        print(f"📦 开始完整数据导出...")
        print(f"📁 导出目录: {self.export_dir}")
        
        if not self.login():
            print("❌ 登录失败")
            return
        
        try:
            # 导出用户信息
            if user_id:
                self.export_user_info(user_id)
            
            # 导出板块信息
            self.export_boards()
            
            # 导出指定板块的帖子
            if board_ids:
                for board_id in board_ids:
                    self.export_posts(board_id)
            
            # 导出用户作品
            if user_id:
                self.export_works(user_id)
            
            # 生成报告
            report = self.generate_report()
            
            print(f"\n🎉 数据导出完成!")
            print(f"📁 文件保存在: {self.export_dir}")
            print(f"📊 共导出 {len(report['files'])} 个文件")
            
        finally:
            self.client.logout()

# 使用示例
if __name__ == "__main__":
    exporter = DataExporter("your_username", "your_password")
    exporter.run_full_export(
        user_id=123,  # 可选：导出指定用户信息
        board_ids=[1, 2, 3]  # 可选：导出指定板块的帖子
    )
```

## 🎯 实用工具

### 6. 配置管理器

```python
import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, config_name="codemao_config"):
        self.config_dir = Path.home() / ".codemao_sdk"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / f"{config_name}.json"
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ 配置文件格式错误，使用默认配置")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "credentials": {
                "username": "",
                "password": ""
            },
            "client_settings": {
                "timeout": 30,
                "max_retries": 3,
                "connection_pool_size": 10
            },
            "auto_reply": {
                "enabled": False,
                "board_ids": [],
                "interval_minutes": 30,
                "max_replies_per_session": 5,
                "reply_templates": [
                    "感谢分享！",
                    "学到了新知识",
                    "很有意思的观点"
                ]
            },
            "export_settings": {
                "default_export_dir": "",
                "auto_backup": False,
                "backup_interval_days": 7
            },
            "logging": {
                "level": "INFO",
                "file": ""
            }
        }
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存到 {self.config_file}")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def get(self, key_path: str, default=None):
        """获取配置值（支持点号路径）"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value):
        """设置配置值（支持点号路径）"""
        keys = key_path.split('.')
        config = self.config
        
        # 遍历到倒数第二层
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置最终值
        config[keys[-1]] = value
        self.save_config()
    
    def update_credentials(self, username: str, password: str):
        """更新登录凭据"""
        self.set("credentials.username", username)
        self.set("credentials.password", password)
    
    def get_credentials(self):
        """获取登录凭据"""
        return self.get("credentials.username"), self.get("credentials.password")
    
    def display_config(self):
        """显示当前配置"""
        print("📋 当前配置:")
        print(json.dumps(self.config, ensure_ascii=False, indent=2))

# 使用示例
if __name__ == "__main__":
    config = ConfigManager()
    
    # 显示当前配置
    config.display_config()
    
    # 更新配置
    config.update_credentials("your_username", "your_password")
    config.set("auto_reply.enabled", True)
    config.set("auto_reply.interval_minutes", 60)
    
    # 获取配置
    username, password = config.get_credentials()
    print(f"用户名: {username}")
    
    reply_enabled = config.get("auto_reply.enabled")
    print(f"自动回复: {'开启' if reply_enabled else '关闭'}")
```

---

**更多示例** 请查看我们的 [GitHub 仓库](https://github.com/nichengfuben/codemao-sdk-for-python/tree/main/examples) 中的完整示例集合！