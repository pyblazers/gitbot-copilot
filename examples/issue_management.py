#!/usr/bin/env python3
"""
Example: Issue Management with GitBot
"""

from gitbot import GitBot
import sys


def main():
    # Initialize GitBot
    bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")
    
    print("=" * 60)
    print("GitBot - Issue Management Example")
    print("=" * 60)
    
    # List all open issues
    print("\n1. Listing all open issues...")
    try:
        issues = bot.issue_manager.list_open_issues()
        print(f"   Found {len(issues)} open issues:")
        for issue in issues:
            print(f"   - #{issue['number']}: {issue['title']}")
            print(f"     State: {issue['state']}, Created by: {issue['user']}")
            print(f"     Labels: {', '.join(issue['labels']) if issue['labels'] else 'None'}")
            print()
    except Exception as e:
        print(f"   Error: {e}")
        sys.exit(1)
    
    # Example: Create a new issue (commented out to avoid creating test issues)
    print("\n2. Creating a new issue (example - commented out)...")
    print("   # Uncomment the code below to create an issue:")
    print("   # new_issue = bot.issue_manager.create_issue(")
    print("   #     title='Test issue from GitBot',")
    print("   #     body='This is an automated test issue created by GitBot.',")
    print("   #     labels=['bot', 'test']")
    print("   # )")
    print("   # print(f'Created issue #{new_issue['number']}: {new_issue['title']}')")
    
    # Example: List issues with specific labels
    print("\n3. Listing issues with specific labels...")
    try:
        labeled_issues = bot.issue_manager.list_open_issues(labels=["bug"])
        print(f"   Found {len(labeled_issues)} issues with 'bug' label")
    except Exception as e:
        print(f"   Note: {e}")
    
    print("\n" + "=" * 60)
    print("Issue Management Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
