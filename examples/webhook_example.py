"""Example: Webhook listener with custom handlers."""

from gitbot.bot import GitBot
from gitbot.config import Config

# Initialize GitBot
config = Config()
bot = GitBot(config)


# Define custom webhook handlers
def handle_issue_event(payload):
    """Handle issue events."""
    action = payload.get('action')
    issue = payload.get('issue', {})
    
    print(f"Issue Event: {action}")
    print(f"Issue #{issue.get('number')}: {issue.get('title')}")
    
    # You can add custom logic here
    # For example, auto-label issues, notify team members, etc.
    
    return {'processed': True, 'action': action}


def handle_pull_request_event(payload):
    """Handle pull request events."""
    action = payload.get('action')
    pr = payload.get('pull_request', {})
    
    print(f"Pull Request Event: {action}")
    print(f"PR #{pr.get('number')}: {pr.get('title')}")
    
    # You can add custom logic here
    # For example, auto-merge PRs that pass checks, notify reviewers, etc.
    
    return {'processed': True, 'action': action}


def handle_push_event(payload):
    """Handle push events."""
    ref = payload.get('ref')
    commits = payload.get('commits', [])
    
    print(f"Push Event to {ref}")
    print(f"Number of commits: {len(commits)}")
    
    for commit in commits:
        print(f"  - {commit.get('id')[:7]}: {commit.get('message')}")
    
    return {'processed': True, 'commits': len(commits)}


# Register webhook handlers
bot.webhook_listener.register_handler('issues', handle_issue_event)
bot.webhook_listener.register_handler('pull_request', handle_pull_request_event)
bot.webhook_listener.register_handler('push', handle_push_event)

# Start the webhook listener
print("Starting webhook listener...")
print("Configure your GitHub webhook to point to: http://your-server:5000/webhook")
print("Recommended events: issues, pull_request, push")
bot.start_webhook_listener()
