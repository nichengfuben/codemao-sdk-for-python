"""
Advanced PyCodeMao SDK Usage Examples

This module contains sophisticated examples showing advanced features:
- Concurrent operations
- Error handling and recovery
- Batch processing
- Data analysis
- Custom workflows
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pycodemao
from pycodemao import CodeMaoClient, Work, User, Post


class CodeMaoAnalyzer:
    """Advanced data analysis and processing utilities."""
    
    def __init__(self, client: CodeMaoClient):
        self.client = client
    
    async def analyze_user_activity(self, username: str, days: int = 7) -> Dict:
        """Analyze user activity over specified days."""
        user = await self.client.get_user(username)
        
        # Get works from the specified period
        all_works = await self.client.get_user_works(username, limit=100)
        
        # Filter works by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_works = [
            work for work in all_works.items 
            if work.created_at.replace(tzinfo=None) > cutoff_date.replace(tzinfo=None)
        ]
        
        # Calculate statistics
        stats = {
            "username": username,
            "total_works": len(all_works.items),
            "recent_works": len(recent_works),
            "avg_likes": sum(work.likes for work in recent_works) / len(recent_works) if recent_works else 0,
            "most_popular_work": max(recent_works, key=lambda w: w.likes) if recent_works else None,
            "activity_level": "high" if len(recent_works) > days * 0.5 else "medium" if recent_works else "low"
        }
        
        return stats
    
    async def batch_process_works(self, work_ids: List[int]) -> Dict:
        """Process multiple works concurrently."""
        tasks = [self.client.get_work(work_id) for work_id in work_ids]
        works = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Separate successful and failed operations
        successful = []
        failed = []
        
        for i, result in enumerate(works):
            if isinstance(result, Exception):
                failed.append((work_ids[i], str(result)))
            else:
                successful.append(result)
        
        return {
            "successful": successful,
            "failed": failed,
            "success_rate": len(successful) / len(work_ids)
        }
    
    async def find_trending_keywords(self, limit: int = 100) -> Dict[str, int]:
        """Find trending keywords from recent works."""
        # Get recent works
        works = await self.client.search_works("", limit=limit)
        
        # Extract and count keywords
        keywords = {}
        for work in works.items:
            # Simple keyword extraction from title and description
            text = f"{work.title} {work.description or ''}".lower()
            words = text.split()
            
            for word in words:
                # Filter out common words and short words
                if len(word) > 3 and word not in ["the", "and", "for", "you", "with"]:
                    keywords[word] = keywords.get(word, 0) + 1
        
        # Sort by frequency
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:20])


class CodeMaoBot:
    """Automated bot for various tasks."""
    
    def __init__(self, client: CodeMaoClient):
        self.client = client
    
    async def auto_like_mentor_works(self, mentor_username: str, limit: int = 10):
        """Automatically like works from a mentor user."""
        works = await self.client.get_user_works(mentor_username, limit=limit)
        
        liked_count = 0
        for work in works.items:
            try:
                await self.client.like_work(work.id)
                liked_count += 1
                print(f"❤️ Liked: {work.title}")
                await asyncio.sleep(1)  # Be respectful with rate limiting
            except Exception as e:
                print(f"⚠️ Failed to like {work.title}: {e}")
        
        print(f"✅ Liked {liked_count}/{len(works.items)} works from {mentor_username}")
    
    async def auto_follow_similar_users(self, target_user: str, limit: int = 5):
        """Find and follow users with similar interests."""
        # Get target user's works to understand their interests
        target_works = await self.client.get_user_works(target_user, limit=10)
        
        # Extract common tags/themes
        themes = set()
        for work in target_works.items:
            if hasattr(work, 'tags') and work.tags:
                themes.update(work.tags)
        
        # Search for users with similar themes
        similar_users = []
        for theme in list(themes)[:3]:  # Check top 3 themes
            try:
                results = await self.client.search_works(theme, limit=20)
                for work in results.items:
                    if work.author != target_user and work.author not in similar_users:
                        similar_users.append(work.author)
            except Exception as e:
                print(f"⚠️ Search failed for theme '{theme}': {e}")
        
        # Follow similar users
        followed = 0
        for username in similar_users[:limit]:
            try:
                await self.client.follow_user(username)
                followed += 1
                print(f"👥 Followed: {username}")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"⚠️ Failed to follow {username}: {e}")
        
        print(f"✅ Followed {followed} similar users")
    
    async def daily_content_creation(self):
        """Create daily programming content."""
        today = datetime.now()
        
        # Programming challenges for different days
        challenges = [
            {
                "title": f"每日挑战 - {today.strftime('%m月%d日')}",
                "content": f'''# 今日编程挑战

print("今天是 {today.strftime('%Y年%m月%d日')}")
print("完成这个简单的挑战！")

# 挑战：打印1到10的平方数
for i in range(1, 11):
    print(f"{{i}} 的平方是 {{i**2}}")

print("挑战完成！🎉")
''',
                "work_type": "python",
                "description": f"{today.strftime('%m月%d日')} 的每日编程挑战"
            }
        ]
        
        # Create the challenge
        challenge = challenges[today.weekday() % len(challenges)]
        
        try:
            work = await self.client.create_work(**challenge)
            print(f"📝 Created daily challenge: {work.title}")
            
            # Share on forum
            boards = await self.client.get_forum_boards()
            if boards:
                post = await self.client.create_post(
                    title=f"🚀 {challenge['title']}",
                    content=f"今天的编程挑战来了！\n\n"
                            f"{challenge['description']}\n\n"
                            f"作品链接: https://codemao.net/work/{work.id}\n"
                            f"快来试试吧！",
                    board_id=boards[0].id
                )
                print(f"💬 Shared on forum: {post.title}")
                
        except Exception as e:
            print(f"⚠️ Daily content creation failed: {e}")


async def concurrent_operations_example():
    """Demonstrate concurrent API operations."""
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        print("🚀 Concurrent Operations Demo")
        print("-" * 40)
        
        # Get multiple users concurrently
        usernames = ["编程猫小王子", "Python大师", "代码小能手"]
        
        start_time = asyncio.get_event_loop().time()
        
        # Concurrent user lookup
        user_tasks = [client.get_user(username) for username in usernames]
        users = await asyncio.gather(*user_tasks, return_exceptions=True)
        
        end_time = asyncio.get_event_loop().time()
        
        print(f"⏱️  Concurrent lookup took: {end_time - start_time:.2f}s")
        
        # Process results
        for username, result in zip(usernames, users):
            if isinstance(result, Exception):
                print(f"❌ {username}: Failed - {result}")
            else:
                print(f"✅ {username}: Level {result.level}, {result.followers} followers")
        
        # Concurrent work operations
        print("\n📊 Concurrent Work Operations")
        
        # Create multiple works concurrently
        works_data = [
            {"title": f"并发作品 {i}", "content": f"print('Hello {i}')", "work_type": "python"}
            for i in range(1, 4)
        ]
        
        work_tasks = [client.create_work(**data) for data in works_data]
        created_works = await asyncio.gather(*work_tasks, return_exceptions=True)
        
        successful_works = [w for w in created_works if not isinstance(w, Exception)]
        print(f"✅ Created {len(successful_works)} works concurrently")
        
        # Like all created works concurrently
        if successful_works:
            like_tasks = [client.like_work(work.id) for work in successful_works]
            await asyncio.gather(*like_tasks, return_exceptions=True)
            print(f"❤️  Liked all {len(successful_works)} works concurrently")
            
    finally:
        await client.close()


async def error_recovery_example():
    """Demonstrate error handling and recovery."""
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        print("🛡️ Error Recovery Demo")
        print("-" * 40)
        
        # Try to get non-existent user with retry
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                user = await client.get_user("不存在的用户_12345")
                print(f"✅ Found user on attempt {attempt + 1}")
                break
            except pycodemao.UserNotFoundError as e:
                print(f"⚠️ Attempt {attempt + 1}: User not found (expected)")
                break
            except Exception as e:
                print(f"❌ Attempt {attempt + 1}: {type(e).__name__} - {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying in {retry_delay}s...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("🚫 Max retries reached, giving up")
        
        # Batch operation with partial failure handling
        print("\n📦 Batch Operation with Error Handling")
        
        # Mix of valid and invalid work IDs
        work_ids = [12345, 999999999, 67890, -1, 54321]
        
        tasks = [client.get_work(work_id) for work_id in work_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = []
        failed = []
        
        for work_id, result in zip(work_ids, results):
            if isinstance(result, Exception):
                failed.append((work_id, str(result)))
                print(f"❌ Work {work_id}: {type(result).__name__}")
            else:
                successful.append(result)
                print(f"✅ Work {work_id}: {result.title}")
        
        print(f"📊 Results: {len(successful)} successful, {len(failed)} failed")
        
    finally:
        await client.close()


async def data_analysis_example():
    """Demonstrate data analysis capabilities."""
    client = pycodemao.create_client("your_api_key_here")
    analyzer = CodeMaoAnalyzer(client)
    
    try:
        print("📈 Data Analysis Demo")
        print("-" * 40)
        
        # Analyze user activity
        print("🔍 User Activity Analysis")
        stats = await analyzer.analyze_user_activity("编程猫小王子", days=30)
        
        print(f"User: {stats['username']}")
        print(f"Total works: {stats['total_works']}")
        print(f"Recent works (30d): {stats['recent_works']}")
        print(f"Average likes: {stats['avg_likes']:.1f}")
        print(f"Activity level: {stats['activity_level']}")
        
        if stats['most_popular_work']:
            print(f"Most popular: {stats['most_popular_work'].title} "
                  f"({stats['most_popular_work'].likes} likes)")
        
        # Find trending keywords
        print("\n🔥 Trending Keywords")
        keywords = await analyzer.find_trending_keywords(limit=50)
        
        print("Top 10 trending keywords:")
        for keyword, count in list(keywords.items())[:10]:
            print(f"   {keyword}: {count} occurrences")
        
        # Batch process works
        print("\n⚡ Batch Work Processing")
        work_ids = [12345, 67890, 54321, 98765, 13579]
        batch_results = await analyzer.batch_process_works(work_ids)
        
        print(f"Success rate: {batch_results['success_rate']:.1%}")
        print(f"Successful: {len(batch_results['successful'])}")
        print(f"Failed: {len(batch_results['failed'])}")
        
    finally:
        await client.close()


async def bot_automation_example():
    """Demonstrate bot automation features."""
    client = pycodemao.create_client("your_api_key_here")
    bot = CodeMaoBot(client)
    
    try:
        print("🤖 Bot Automation Demo")
        print("-" * 40)
        print("⚠️  This is a demo - adjust usernames and limits as needed")
        print()
        
        # Auto-like mentor works
        print("❤️ Auto-like Mentor Works")
        await bot.auto_like_mentor_works("编程猫小王子", limit=5)
        
        # Auto-follow similar users
        print("\n👥 Auto-follow Similar Users")
        await bot.auto_follow_similar_users("编程猫小王子", limit=3)
        
        # Daily content creation (disabled for demo)
        print("\n📝 Daily Content Creation (Demo - not creating)")
        print("Would create daily challenge for today")
        # await bot.daily_content_creation()  # Uncomment to enable
        
    finally:
        await client.close()


# Main function to run all examples
async def main():
    """Run all advanced examples."""
    print("🎯 PyCodeMao Advanced Examples")
    print("=" * 50)
    print("Replace 'your_api_key_here' with your actual API key!")
    print("Some examples may require specific usernames or data to work properly.\n")
    
    examples = [
        (concurrent_operations_example, "Concurrent Operations"),
        (error_recovery_example, "Error Recovery"),
        (data_analysis_example, "Data Analysis"),
        (bot_automation_example, "Bot Automation")
    ]
    
    for example_func, name in examples:
        try:
            print(f"\n🚀 Running: {name}")
            print("=" * 50)
            await example_func()
            print("\n" + "=" * 50)
            await asyncio.sleep(2)  # Delay between examples
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            print("=" * 50)
    
    print("\n🎉 All advanced examples completed!")
    print("Check the source code to understand the implementation details.")


if __name__ == "__main__":
    asyncio.run(main())