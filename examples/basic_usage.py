#!/usr/bin/env python3
"""
Example usage of GitBot
"""

from gitbot import GitBot


def main():
    # Initialize GitBot (credentials from .env file)
    bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")
    
    print("=" * 60)
    print("GitBot Example Usage")
    print("=" * 60)
    
    # 1. Get user information
    print("\n1. Getting authenticated user information...")
    try:
        user_info = bot.get_user_info()
        print(f"   Logged in as: {user_info['login']}")
        print(f"   Public repos: {user_info['public_repos']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 2. Get repository analytics
    print("\n2. Getting repository statistics...")
    try:
        stats = bot.analytics.get_basic_stats()
        print(f"   Repository: {stats['full_name']}")
        print(f"   Stars: {stats['stars']}")
        print(f"   Forks: {stats['forks']}")
        print(f"   Open Issues: {stats['open_issues']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 3. List open issues
    print("\n3. Listing open issues...")
    try:
        issues = bot.issue_manager.list_open_issues()
        print(f"   Found {len(issues)} open issues")
        for issue in issues[:3]:  # Show first 3
            print(f"   - #{issue['number']}: {issue['title']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 4. List pull requests
    print("\n4. Listing pull requests...")
    try:
        prs = bot.pr_manager.list_pull_requests()
        print(f"   Found {len(prs)} open pull requests")
        for pr in prs[:3]:  # Show first 3
            print(f"   - #{pr['number']}: {pr['title']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 5. Get recent activity
    print("\n5. Getting recent activity...")
    try:
        activity = bot.analytics.get_recent_activity(limit=3)
        print(f"   Recent commits: {len(activity['recent_commits'])}")
        for commit in activity['recent_commits']:
            print(f"   - {commit['sha']}: {commit['message']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
