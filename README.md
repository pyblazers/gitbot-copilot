# 🤖 GitBot - GitHub Repository Automation Bot

GitBot is a powerful, modular automation bot for GitHub repositories designed to streamline common repository tasks. It provides comprehensive features for issue management, pull request handling, repository analytics, and real-time webhook processing.

## ✨ Features

### 1. **Issue Management**
- List open, closed, or all issues with flexible filtering
- Create new issues with custom labels and assignees
- Assign/reassign users to issues
- Add labels dynamically
- Close issues programmatically

### 2. **Pull Request Management**
- List pull requests with state filtering
- Get detailed PR information including diff stats
- Merge PRs after validation with multiple merge strategies (merge, squash, rebase)
- Check PR reviews and approval status
- Approve pull requests programmatically

### 3. **Repository Analytics**
- Basic repository statistics (stars, forks, watchers, size)
- Commit statistics with author breakdown
- Contributor analytics
- Recent activity tracking
- Programming language distribution
- Branch statistics

### 4. **Webhook Listener**
- Real-time GitHub event processing
- Secure webhook signature verification
- Extensible handler registration system
- Support for all GitHub webhook events
- Built-in Flask server for production deployment

### 5. **Modular Architecture**
- Clean separation of concerns
- Easy to extend with new features
- Reusable components
- Production-ready code structure

## 🍎 macOS Installation

GitBot is designed to work seamlessly on macOS systems, especially Mac Mini servers. Follow these steps to get started:

### Prerequisites

- macOS 10.14 or later
- Internet connection
- GitHub account with repository access

### Automated Setup

The quickest way to set up GitBot on macOS is using the automated setup script:

```bash
# Clone the repository
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot

# Run the setup script
./setup_macos.sh
```

The setup script will:
- Install Homebrew (if not already installed)
- Install Python 3 (if not already installed)
- Create a Python virtual environment
- Install all required dependencies
- Create a `.env` configuration file

### Manual Setup

If you prefer to set up manually:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3

# Clone the repository
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create configuration file
cp .env.example .env
```

## ⚙️ Configuration

### 1. GitHub Personal Access Token

Create a GitHub personal access token with the following scopes:

1. Go to GitHub Settings → Developer settings → Personal access tokens → [Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select the following scopes:
   - `repo` - Full control of private repositories
   - `admin:repo_hook` - Full control of repository hooks
   - `admin:org_hook` - Full control of organization hooks (if working with org repos)
4. Generate and copy the token

### 2. Environment Variables

Edit the `.env` file with your configuration:

```bash
# Required
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=owner/repository

# Optional (for webhook listener)
WEBHOOK_SECRET=your_webhook_secret
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0
```

### 3. Load Environment

Before using GitBot, activate the virtual environment and load environment variables:

```bash
source venv/bin/activate
export $(cat .env | xargs)  # Load environment variables
```

Or use a tool like `python-dotenv` (already included in requirements):

```python
from dotenv import load_dotenv
load_dotenv()
```

## 🚀 Usage

### Command-Line Interface

GitBot provides a comprehensive CLI for all operations:

```bash
# Activate virtual environment
source venv/bin/activate

# Get help
python cli.py --help

# Issue Management
python cli.py issues list --state open
python cli.py issues create --title "Bug fix needed" --labels bug enhancement
python cli.py issues assign --number 42 --assignees user1 user2

# Pull Request Management
python cli.py pr list --state open
python cli.py pr get --number 15
python cli.py pr merge --number 15 --method squash

# Repository Analytics
python cli.py analytics stats
python cli.py analytics commits --days 30
python cli.py analytics contributors
python cli.py analytics activity --limit 10
python cli.py analytics languages

# Webhook Listener
python cli.py webhook --host 0.0.0.0 --port 5000
```

### Python API

Use GitBot programmatically in your Python scripts:

```python
from gitbot.bot import GitBot

# Initialize GitBot
bot = GitBot()

# List open issues
issues = bot.issues.list_issues(state='open')
for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")

# Get repository stats
stats = bot.analytics.get_basic_stats()
print(f"Stars: {stats['stars']}, Forks: {stats['forks']}")

# List pull requests
prs = bot.pull_requests.list_pull_requests()
for pr in prs:
    print(f"PR #{pr['number']}: {pr['title']} - {pr['state']}")
```

### Example Scripts

The `examples/` directory contains ready-to-use scripts:

```bash
# Basic usage example
python examples/basic_usage.py

# Issue management example
python examples/issue_management.py

# PR automation example
python examples/pr_automation.py

# Webhook listener example
python examples/webhook_example.py
```

## 🔔 Webhook Configuration

To enable real-time event processing, configure GitHub webhooks:

### 1. Start Webhook Listener

```bash
python cli.py webhook --host 0.0.0.0 --port 5000
```

Or use the example script with custom handlers:

```bash
python examples/webhook_example.py
```

### 2. Configure GitHub Webhook

1. Go to your repository → Settings → Webhooks → Add webhook
2. Set Payload URL: `http://your-server-ip:5000/webhook`
3. Set Content type: `application/json`
4. Set Secret: (use the value from `WEBHOOK_SECRET` in `.env`)
5. Select events:
   - Issues
   - Pull requests
   - Push
   - Or choose "Send me everything"
6. Ensure "Active" is checked
7. Click "Add webhook"

### 3. Expose Your Server (for local testing)

If running on your Mac Mini behind a firewall, use a tunneling service like ngrok:

```bash
# Install ngrok via Homebrew
brew install ngrok

# Start tunnel
ngrok http 5000

# Use the provided URL (e.g., https://abc123.ngrok.io/webhook) in GitHub webhook config
```

## 📁 Project Structure

```
gitbot-copilot/
├── gitbot/                 # Main package
│   ├── __init__.py        # Package initialization
│   ├── bot.py             # Main GitBot class
│   ├── config.py          # Configuration management
│   ├── github_client.py   # GitHub API client
│   ├── issue_manager.py   # Issue operations
│   ├── pr_manager.py      # Pull request operations
│   ├── analytics.py       # Repository analytics
│   └── webhook_listener.py # Webhook server
├── examples/              # Example scripts
│   ├── basic_usage.py     # Basic usage examples
│   ├── issue_management.py # Issue management examples
│   ├── pr_automation.py   # PR automation examples
│   └── webhook_example.py # Webhook listener example
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── setup_macos.sh        # macOS setup script
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## 🔧 Advanced Usage

### Running as a Background Service (macOS)

To run GitBot as a background service on your Mac Mini server, create a Launch Agent:

1. Create a plist file at `~/Library/LaunchAgents/com.gitbot.webhook.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gitbot.webhook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/gitbot-copilot/venv/bin/python</string>
        <string>/path/to/gitbot-copilot/cli.py</string>
        <string>webhook</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/gitbot-webhook.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/gitbot-webhook.error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>GITHUB_TOKEN</key>
        <string>your_token_here</string>
        <key>GITHUB_REPO</key>
        <string>owner/repo</string>
    </dict>
</dict>
</plist>
```

2. Load the service:

```bash
launchctl load ~/Library/LaunchAgents/com.gitbot.webhook.plist
```

3. Control the service:

```bash
# Start
launchctl start com.gitbot.webhook

# Stop
launchctl stop com.gitbot.webhook

# Unload
launchctl unload ~/Library/LaunchAgents/com.gitbot.webhook.plist
```

### Custom Webhook Handlers

Create custom handlers for specific events:

```python
from gitbot.bot import GitBot

bot = GitBot()

def handle_issue_comment(payload):
    """Auto-respond to issue comments"""
    action = payload['action']
    comment = payload['comment']['body']
    
    if '@gitbot' in comment:
        # Process command
        issue_number = payload['issue']['number']
        # Add your custom logic here
        
    return {'processed': True}

bot.webhook_listener.register_handler('issue_comment', handle_issue_comment)
bot.start_webhook_listener()
```

### Automated PR Merging

Set up automated PR merging with validation:

```python
from gitbot.bot import GitBot

bot = GitBot()

def auto_merge_prs():
    """Merge PRs that meet criteria"""
    prs = bot.pull_requests.list_pull_requests(state='open')
    
    for pr in prs:
        # Get reviews
        reviews = bot.pull_requests.get_pending_reviews(pr['number'])
        
        # Check if approved
        approved = any(r['state'] == 'APPROVED' for r in reviews)
        
        if approved and pr['mergeable']:
            try:
                result = bot.pull_requests.merge_pull_request(
                    pr['number'],
                    merge_method='squash'
                )
                print(f"Merged PR #{pr['number']}")
            except Exception as e:
                print(f"Failed to merge PR #{pr['number']}: {e}")

# Run periodically or via webhook
auto_merge_prs()
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use webhook secrets** - Always configure `WEBHOOK_SECRET` for production
3. **Restrict token scopes** - Only grant necessary permissions
4. **Use HTTPS** - For production webhooks, always use HTTPS
5. **Validate webhook signatures** - The webhook listener verifies signatures automatically
6. **Keep dependencies updated** - Regularly update packages with `pip install --upgrade -r requirements.txt`

## 🚀 Future Enhancements

GitBot's modular architecture makes it easy to add new features:

- **Slack/Discord Notifications** - Send notifications to team channels
- **CI/CD Integration** - Trigger builds and deployments
- **Automated Issue Triage** - Label and assign issues based on content
- **PR Review Automation** - Auto-request reviews based on file changes
- **Scheduled Tasks** - Periodic cleanup and maintenance tasks
- **GitHub Projects Integration** - Manage project boards
- **Custom Commands** - Bot commands via issue/PR comments
- **Metrics Dashboard** - Web-based analytics dashboard

## 📖 API Documentation

### Core Classes

#### `GitBot`
Main bot class integrating all modules.

```python
bot = GitBot()
bot.issues         # IssueManager instance
bot.pull_requests  # PullRequestManager instance
bot.analytics      # RepositoryAnalytics instance
bot.webhook_listener  # WebhookListener instance
```

#### `IssueManager`
Handles issue operations.

- `list_issues(state='open', labels=None)` - List issues
- `create_issue(title, body=None, labels=None, assignees=None)` - Create issue
- `assign_issue(issue_number, assignees)` - Assign users
- `add_labels(issue_number, labels)` - Add labels
- `close_issue(issue_number)` - Close issue

#### `PullRequestManager`
Handles PR operations.

- `list_pull_requests(state='open')` - List PRs
- `get_pull_request(pr_number)` - Get PR details
- `merge_pull_request(pr_number, commit_title=None, commit_message=None, merge_method='merge')` - Merge PR
- `get_pending_reviews(pr_number)` - Get reviews
- `approve_pull_request(pr_number, body=None)` - Approve PR

#### `RepositoryAnalytics`
Provides repository analytics.

- `get_basic_stats()` - Basic statistics
- `get_commit_stats(days=30)` - Commit statistics
- `get_contributor_stats()` - Contributor information
- `get_recent_activity(limit=10)` - Recent activity
- `get_language_stats()` - Language distribution
- `get_branch_stats()` - Branch information

#### `WebhookListener`
Handles GitHub webhooks.

- `register_handler(event_type, handler)` - Register event handler
- `start()` - Start webhook server

## 🤝 Contributing

Contributions are welcome! The modular architecture makes it easy to add new features.

1. Fork the repository
2. Create a feature branch
3. Add your feature or fix
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues, questions, or feature requests:

1. Check the examples in the `examples/` directory
2. Review this README thoroughly
3. Open an issue on GitHub
4. Consult the PyGithub documentation for advanced API usage

## 🙏 Acknowledgments

- Built with [PyGithub](https://github.com/PyGithub/PyGithub) - Python library for GitHub API
- Webhook server powered by [Flask](https://flask.palletsprojects.com/)
- Designed for macOS deployment with ease of use in mind

---

**Happy Automating! 🤖**