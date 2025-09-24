"""
Basic PyCodeMao SDK Usage Examples

This module contains simple, beginner-friendly examples of using the PyCodeMao SDK.
Perfect for getting started quickly!
"""

import asyncio
import pycodemao


async def simple_user_lookup():
    """Simple user lookup example."""
    print("👤 Simple User Lookup")
    print("-" * 30)
    
    # Create client with your API key
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Get user information
        username = "编程猫小王子"
        user = await client.get_user(username)
        
        print(f"Found user: {user.nickname}")
        print(f"Level: {user.level}")
        print(f"Followers: {user.followers}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always close the client
        await client.close()


async def create_simple_work():
    """Create a simple programming work."""
    print("\n🎨 Create Simple Work")
    print("-" * 30)
    
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Create a simple Python program
        work = await client.create_work(
            title="我的第一个程序",
            content="print('你好，编程猫！')",
            work_type="python"
        )
        
        print(f"Created work: {work.title}")
        print(f"Work ID: {work.id}")
        print(f"Created at: {work.created_at}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


async def post_to_forum():
    """Post a message to the forum."""
    print("\n💬 Post to Forum")
    print("-" * 30)
    
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Get available boards
        boards = await client.get_forum_boards()
        if boards:
            first_board = boards[0]
            print(f"Posting to board: {first_board.name}")
            
            # Create a forum post
            post = await client.create_post(
                title="大家好！",
                content="我是新来的，请多多关照！",
                board_id=first_board.id
            )
            
            print(f"Posted: {post.title}")
            print(f"Post ID: {post.id}")
        else:
            print("No forum boards available")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


async def like_user_works():
    """Like some user works."""
    print("\n❤️ Like User Works")
    print("-" * 30)
    
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Get user's works
        username = "编程猫小王子"
        works = await client.get_user_works(username, limit=3)
        
        print(f"Found {len(works.items)} works by {username}")
        
        for work in works.items:
            print(f"Liking: {work.title}")
            
            # Like the work
            await client.like_work(work.id)
            print(f"  ✅ Liked!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


async def simple_search():
    """Simple search example."""
    print("\n🔍 Simple Search")
    print("-" * 30)
    
    client = pycodemao.create_client("your_api_key_here")
    
    try:
        # Search for Python-related works
        results = await client.search_works(
            query="python",
            limit=5
        )
        
        print(f"Found {results.total} results for 'python'")
        
        for i, work in enumerate(results.items, 1):
            print(f"{i}. {work.title} by {work.author}")
            print(f"   👍 {work.likes} likes")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


# Helper function to run examples
async def run_example(example_func, name):
    """Run an example with error handling."""
    try:
        print(f"\n🚀 Running: {name}")
        await example_func()
    except Exception as e:
        print(f"❌ {name} failed: {e}")


async def main():
    """Run all basic examples."""
    print("🎯 PyCodeMao Basic Examples")
    print("=" * 40)
    print("Replace 'your_api_key_here' with your actual API key to run these examples.\n")
    
    # List of examples to run
    examples = [
        (simple_user_lookup, "User Lookup"),
        (create_simple_work, "Create Work"),
        (post_to_forum, "Forum Post"),
        (like_user_works, "Like Works"),
        (simple_search, "Search Works")
    ]
    
    # Run each example
    for example_func, name in examples:
        await run_example(example_func, name)
        await asyncio.sleep(1)  # Small delay between examples
    
    print("\n🎉 All basic examples completed!")
    print("Try modifying the code to create your own projects!")


# For quick testing
if __name__ == "__main__":
    # Note: Replace "your_api_key_here" with your actual API key
    asyncio.run(main())