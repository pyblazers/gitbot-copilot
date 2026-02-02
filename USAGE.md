# GitBot Usage Guide

This guide demonstrates the key features and usage patterns of GitBot.

## Quick Start

### 1. Setup Environment

```bash
# Copy and configure environment file
cp .env.example .env
nano .env  # Add your GitHub token and repository details
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Command-Line Usage

### User Information

Get information about the authenticated user:

```bash
python gitbot_cli.py user
```

Example output:
```json
{
  "login": "username",
  "name": "Full Name",
  "email": "user@example.com",
  "public_repos": 42,
  "followers": 100,
  "following": 50
}
```

### Issue Management

List all open issues:
```bash
python gitbot_cli.py issues --list --owner pyblazers --repo gitbot-copilot
```

Create a new issue:
```bash
python gitbot_cli.py issues --create \
  --title "Add feature X" \
  --body "We need feature X because..." \
  --labels enhancement feature \
  --assignees username
```

List closed issues:
```bash
python gitbot_cli.py issues --list --state closed
```

### Pull Request Management

List all open pull requests:
```bash
python gitbot_cli.py pr --list --owner pyblazers --repo gitbot-copilot
```

Get details of a specific PR:
```bash
python gitbot_cli.py pr --get 123
```

Merge a pull request:
```bash
python gitbot_cli.py pr --merge 123 --method squash
```

### Repository Analytics

Get basic repository statistics:
```bash
python gitbot_cli.py analytics --stats --owner pyblazers --repo gitbot-copilot
```

Get commit statistics for the last 30 days:
```bash
python gitbot_cli.py analytics --commits --days 30
```

Get contributor information:
```bash
python gitbot_cli.py analytics --contributors
```

Get recent activity:
```bash
python gitbot_cli.py analytics --activity
```

Get programming language breakdown:
```bash
python gitbot_cli.py analytics --languages
```

Get release information:
```bash
python gitbot_cli.py analytics --releases
```

### Webhook Listener

Start the webhook listener on default port (5000):
```bash
python gitbot_cli.py webhook
```

Start with custom port and host:
```bash
python gitbot_cli.py webhook --port 8080 --host 0.0.0.0
```

Start in debug mode:
```bash
python gitbot_cli.py webhook --debug
```

## Python API Usage

### Basic Example

```python
from gitbot import GitBot

# Initialize with credentials from .env
bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# Get repository stats
stats = bot.analytics.get_basic_stats()
print(f"Repository: {stats['full_name']}")
print(f"Stars: {stats['stars']}")
print(f"Forks: {stats['forks']}")
```

### Issue Management Example

```python
from gitbot import GitBot

bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# List open issues
issues = bot.issue_manager.list_open_issues()
for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")

# Create a new issue
new_issue = bot.issue_manager.create_issue(
    title="Bug report",
    body="Description of the bug",
    labels=["bug", "priority-high"]
)
print(f"Created issue #{new_issue['number']}")

# Assign users to an issue
bot.issue_manager.assign_issue(
    issue_number=123,
    assignees=["username1", "username2"]
)

# Close an issue
bot.issue_manager.close_issue(
    issue_number=123,
    comment="Fixed in PR #456"
)
```

### Pull Request Management Example

```python
from gitbot import GitBot

bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# List pull requests
prs = bot.pr_manager.list_pull_requests(state="open")
for pr in prs:
    print(f"#{pr['number']}: {pr['title']} - Mergeable: {pr['mergeable']}")

# Get PR details
pr = bot.pr_manager.get_pull_request(123)
print(f"PR #{pr['number']}: {pr['title']}")
print(f"Author: {pr['user']}")
print(f"State: {pr['state']}")
print(f"Mergeable: {pr['mergeable']}")

# Merge a pull request
result = bot.pr_manager.merge_pull_request(
    pr_number=123,
    commit_message="Merge PR #123: Add new feature",
    merge_method="squash"
)
if result['success']:
    print(f"Successfully merged! SHA: {result['sha']}")
else:
    print(f"Merge failed: {result['message']}")

# Create a new pull request
new_pr = bot.pr_manager.create_pull_request(
    title="Add new feature",
    head="feature-branch",
    base="main",
    body="This PR adds a new feature..."
)
print(f"Created PR #{new_pr['number']}")
```

### Analytics Example

```python
from gitbot import GitBot

bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# Get basic stats
stats = bot.analytics.get_basic_stats()
print(f"Stars: {stats['stars']}, Forks: {stats['forks']}")

# Get commit statistics
commit_stats = bot.analytics.get_commit_stats(since_days=7)
print(f"Commits in last 7 days: {commit_stats['total_commits']}")
print("Top contributors:")
for author, count in commit_stats['commits_by_author'].items():
    print(f"  {author}: {count} commits")

# Get contributor stats
contributors = bot.analytics.get_contributor_stats()
for contributor in contributors[:5]:
    print(f"{contributor['login']}: {contributor['contributions']} contributions")

# Get recent activity
activity = bot.analytics.get_recent_activity(limit=5)
print("\nRecent commits:")
for commit in activity['recent_commits']:
    print(f"  {commit['sha']}: {commit['message']}")

# Get language stats
languages = bot.analytics.get_language_stats()
for lang, stats in languages.items():
    print(f"{lang}: {stats['percentage']}%")
```

### Webhook Listener Example

```python
from gitbot import GitBot

bot = GitBot()

# Define custom event handler
def on_push(payload):
    repo = payload['repository']['full_name']
    commits = len(payload['commits'])
    print(f"Received push to {repo} with {commits} commits")
    return {"status": "success", "message": f"Processed {commits} commits"}

def on_issue_opened(payload):
    if payload['action'] == 'opened':
        issue = payload['issue']
        print(f"New issue #{issue['number']}: {issue['title']}")
        # Auto-label new issues
        # bot.issue_manager.add_labels(issue['number'], ['needs-triage'])
    return {"status": "success"}

# Register handlers
bot.webhook_listener.register_handler("push", on_push)
bot.webhook_listener.register_handler("issues", on_issue_opened)

# Start listening
bot.webhook_listener.start(debug=True)
```

## Advanced Usage

### Working with Multiple Repositories

```python
from gitbot import GitBot

# Initialize without repository
bot = GitBot(github_token="your_token")

# Work with first repository
bot.set_repository("owner1", "repo1")
issues_repo1 = bot.issue_manager.list_open_issues()

# Switch to another repository
bot.set_repository("owner2", "repo2")
issues_repo2 = bot.issue_manager.list_open_issues()
```

### Error Handling

```python
from gitbot import GitBot

bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

try:
    # Try to merge a PR
    result = bot.pr_manager.merge_pull_request(123)
    if not result['success']:
        print(f"Merge failed: {result['message']}")
        if 'mergeable_state' in result:
            print(f"Mergeable state: {result['mergeable_state']}")
except Exception as e:
    print(f"Error: {e}")
```

### Filtering and Searching

```python
from gitbot import GitBot

bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# List issues with specific labels
bug_issues = bot.issue_manager.list_open_issues(labels=["bug"])

# List closed issues
closed_issues = bot.issue_manager.list_open_issues(state="closed")

# List all issues
all_issues = bot.issue_manager.list_open_issues(state="all")

# Sort pull requests
recent_prs = bot.pr_manager.list_pull_requests(
    state="open",
    sort="updated",
    direction="desc"
)
```

## Tips and Best Practices

1. **Use Environment Variables**: Store credentials in `.env` file, never commit them
2. **Error Handling**: Always check return values and handle errors gracefully
3. **Rate Limiting**: GitHub API has rate limits - use responsibly
4. **Webhook Security**: Always use webhook secrets in production
5. **Testing**: Test on a test repository before using on production repositories
6. **Logging**: Enable debug mode for troubleshooting
7. **HTTPS**: Always use HTTPS for webhook endpoints in production
8. **Reverse Proxy**: Run webhook listener behind nginx/Apache in production

## Common Issues

### Authentication Errors
- Verify your GitHub token is valid and has required permissions
- Check that the token is properly set in `.env` file

### Rate Limiting
- GitHub API has rate limits (5000 requests/hour for authenticated users)
- Use conditional requests and caching when possible

### Webhook Not Receiving Events
- Ensure webhook URL is publicly accessible
- Verify webhook secret matches
- Check firewall settings
- Review webhook delivery logs in GitHub

## Next Steps

- Explore the `examples/` directory for more usage examples
- Read the main README for deployment instructions
- Check out the API documentation in the source code
- Contribute improvements via pull requests

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/pyblazers/gitbot-copilot/issues
