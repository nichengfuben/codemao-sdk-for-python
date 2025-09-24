"""
Quick Start Guide for PyCodeMao SDK

This example shows the most common use cases in just a few lines of code.
Perfect for getting started quickly!
"""

import asyncio
import pycodemao


async def quick_start():
    """Complete quick start example."""
    
    # 1. Create client (replace with your actual API key)
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # 2. Get user info
        user = await client.get_user("编程猫小王子")
        print(f"🎉 Found user: {user.nickname} (Level {user.level})")
        
        # 3. Create a work
        work = await client.create_work(
            title="我的第一个Python程序",
            content="print('Hello, CodeMao!')",
            work_type="python"
        )
        print(f"📝 Created work: {work.title}")
        
        # 4. Like someone's work
        await client.like_work(work.id)
        print(f"❤️ Liked the work")
        
        # 5. Search for works
        results = await client.search_works("python", limit=3)
        print(f"🔍 Found {results.total} Python works:")
        for work in results.items:
            print(f"   - {work.title} by {work.author}")
            
    finally:
        # Always close the client
        await client.close()


async def simple_user_stats():
    """Get user statistics quickly."""
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Get user and their stats
        user = await client.get_user("编程猫小王子")
        
        print(f"👤 User Stats for {user.nickname}:")
        print(f"   Level: {user.level}")
        print(f"   Followers: {user.followers}")
        print(f"   Works: {user.works_count}")
        print(f"   Joined: {user.created_at}")
        
        # Get their recent works
        works = await client.get_user_works(user.username, limit=3)
        print(f"\n📝 Recent Works:")
        for work in works.items:
            print(f"   - {work.title} ({work.likes} likes)")
            
    finally:
        await client.close()


async def create_and_share():
    """Create a work and share it."""
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Create a fun Python program
        code = '''
import turtle

# 创建画布
t = turtle.Turtle()
t.speed(5)

# 画一个彩色螺旋
colors = ['red', 'blue', 'green', 'purple', 'orange']
for i in range(50):
    t.color(colors[i % len(colors)])
    t.forward(i * 2)
    t.right(144)

turtle.done()
'''
        
        # Create the work
        work = await client.create_work(
            title="彩色螺旋图案",
            content=code,
            work_type="python",
            description="使用Python的turtle库绘制彩色螺旋图案"
        )
        
        print(f"🎨 Created work: {work.title}")
        print(f"   ID: {work.id}")
        print(f"   URL: https://codemao.net/work/{work.id}")
        
        # Get forum boards to share
        boards = await client.get_forum_boards()
        if boards:
            # Share on first board
            post = await client.create_post(
                title=f"新作品: {work.title}",
                content=f"我刚创建了一个Python turtle作品！\n\n"
                        f"这个程序可以绘制彩色螺旋图案，很适合初学者学习。\n"
                        f"作品链接: https://codemao.net/work/{work.id}",
                board_id=boards[0].id
            )
            print(f"💬 Shared on forum: {post.title}")
            
    finally:
        await client.close()


# Run the examples
if __name__ == "__main__":
    print("🚀 PyCodeMao Quick Start Examples")
    print("=" * 40)
    print("Replace 'your_api_key_here' with your actual API key!\n")
    
    # Run quick start
    asyncio.run(quick_start())
    
    print("\n" + "="*40 + "\n")
    
    # Run user stats
    asyncio.run(simple_user_stats())
    
    print("\n" + "="*40 + "\n")
    
    # Run create and share
    asyncio.run(create_and_share())
    
    print("\n🎉 Quick start completed!")
    print("Check the examples folder for more advanced usage!")