#!/usr/bin/env python3
"""
Example: Webhook Listener with GitBot
"""

from gitbot import GitBot
from gitbot.modules.webhook_listener import (
    handle_push_event,
    handle_pull_request_event,
    handle_issues_event
)


def custom_push_handler(payload):
    """Custom handler for push events"""
    repo_name = payload.get("repository", {}).get("full_name")
    commits = payload.get("commits", [])
    
    print(f"\n[PUSH EVENT] Repository: {repo_name}")
    print(f"Number of commits: {len(commits)}")
    
    for commit in commits:
        print(f"  - {commit['id'][:7]}: {commit['message']}")
    
    return {
        "status": "success",
        "message": f"Processed {len(commits)} commits"
    }


def custom_issue_handler(payload):
    """Custom handler for issue events"""
    action = payload.get("action")
    issue = payload.get("issue", {})
    
    print(f"\n[ISSUE EVENT] Action: {action}")
    print(f"Issue #{issue.get('number')}: {issue.get('title')}")
    print(f"User: {issue.get('user', {}).get('login')}")
    
    return {
        "status": "success",
        "message": f"Processed issue event: {action}"
    }


def main():
    # Initialize GitBot
    bot = GitBot()
    
    print("=" * 60)
    print("GitBot - Webhook Listener Example")
    print("=" * 60)
    print("\nRegistering custom event handlers...")
    
    # Register custom handlers
    bot.webhook_listener.register_handler("push", custom_push_handler)
    bot.webhook_listener.register_handler("pull_request", handle_pull_request_event)
    bot.webhook_listener.register_handler("issues", custom_issue_handler)
    
    print("\nStarting webhook listener...")
    print("Configure your GitHub webhook to point to:")
    print(f"  URL: http://your-server:{bot.webhook_listener.port}/webhook")
    print("  Content type: application/json")
    print("  Events: Choose 'push', 'pull_request', 'issues' or 'Send me everything'")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Start the webhook listener
    bot.webhook_listener.start(debug=True)


if __name__ == "__main__":
    main()
