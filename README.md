# GitBot - GitHub Automation Bot

GitBot is a powerful Python-based automation tool that streamlines GitHub repository management. Designed for deployment on macOS (Mac Mini server) and other platforms, it provides comprehensive features for managing issues, pull requests, repository analytics, and webhook event handling.

## Features

### 🎯 Issue Management
- List open/closed issues with filtering options
- Create new issues with labels and assignees
- Assign users to existing issues
- Add labels to issues
- Close issues with optional comments

### 🔀 Pull Request Management
- List pull requests with various filters
- Get detailed PR information
- Merge pull requests after validation
- Create new pull requests
- Add review comments

### 📊 Repository Analytics
- Basic repository statistics (stars, forks, watchers)
- Commit statistics and analysis
- Contributor statistics
- Recent activity tracking
- Programming language breakdown
- Release information

### 🎣 Webhook Listener
- Real-time GitHub event handling
- Support for push, pull request, and issue events
- Customizable event handlers
- Secure webhook validation with HMAC

## Prerequisites

### macOS Setup

1. **Install Homebrew** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python 3.9+**:
```bash
brew install python@3.11
```

3. **Verify Python installation**:
```bash
python3 --version
```

### GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with the following scopes:
   - `repo` (Full control of private repositories)
   - `admin:repo_hook` (Full control of repository hooks)
   - `user` (Read user profile data)
3. Save the token securely

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and edit it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your favorite editor:

```bash
nano .env
```

Set the following variables:

```bash
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repository_name
WEBHOOK_SECRET=your_webhook_secret_optional
WEBHOOK_PORT=5000
```

## Usage

### Command-Line Interface

GitBot provides a comprehensive CLI for all operations:

#### Get User Information
```bash
python gitbot_cli.py user
```

#### Issue Management

List open issues:
```bash
python gitbot_cli.py issues --list --owner pyblazers --repo gitbot-copilot
```

Create a new issue:
```bash
python gitbot_cli.py issues --create --title "Bug fix needed" --body "Description" --labels bug enhancement
```

#### Pull Request Management

List pull requests:
```bash
python gitbot_cli.py pr --list --owner pyblazers --repo gitbot-copilot
```

Get PR details:
```bash
python gitbot_cli.py pr --get 123
```

Merge a pull request:
```bash
python gitbot_cli.py pr --merge 123 --method squash
```

#### Analytics

Get basic repository stats:
```bash
python gitbot_cli.py analytics --stats --owner pyblazers --repo gitbot-copilot
```

Get commit statistics:
```bash
python gitbot_cli.py analytics --commits --days 30
```

Get contributor stats:
```bash
python gitbot_cli.py analytics --contributors
```

Get recent activity:
```bash
python gitbot_cli.py analytics --activity
```

Get language statistics:
```bash
python gitbot_cli.py analytics --languages
```

Get release information:
```bash
python gitbot_cli.py analytics --releases
```

#### Webhook Listener

Start the webhook listener:
```bash
python gitbot_cli.py webhook --port 5000
```

### Python API

Use GitBot directly in your Python code:

```python
from gitbot import GitBot

# Initialize
bot = GitBot(owner="pyblazers", repo_name="gitbot-copilot")

# Get repository stats
stats = bot.analytics.get_basic_stats()
print(f"Stars: {stats['stars']}, Forks: {stats['forks']}")

# List issues
issues = bot.issue_manager.list_open_issues()
for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")

# List pull requests
prs = bot.pr_manager.list_pull_requests()
for pr in prs:
    print(f"#{pr['number']}: {pr['title']}")
```

### Example Scripts

Several example scripts are provided in the `examples/` directory:

```bash
# Basic usage example
python examples/basic_usage.py

# Issue management example
python examples/issue_management.py

# Webhook listener example
python examples/webhook_listener.py
```

## Webhook Configuration

To set up GitHub webhooks:

1. Start the webhook listener:
   ```bash
   python gitbot_cli.py webhook --port 5000
   ```

2. Configure your GitHub repository webhook:
   - Go to repository Settings → Webhooks → Add webhook
   - Payload URL: `http://your-server-ip:5000/webhook`
   - Content type: `application/json`
   - Secret: (use the value from WEBHOOK_SECRET in .env)
   - Events: Select individual events or "Send me everything"

3. For local development, use a tunnel service like [ngrok](https://ngrok.com/):
   ```bash
   brew install ngrok
   ngrok http 5000
   ```

## Project Structure

```
gitbot-copilot/
├── gitbot/
│   ├── __init__.py          # Package initialization
│   ├── gitbot.py            # Main GitBot class
│   └── modules/
│       ├── __init__.py
│       ├── issue_manager.py     # Issue management
│       ├── pr_manager.py        # Pull request management
│       ├── analytics.py         # Repository analytics
│       └── webhook_listener.py  # Webhook event handling
├── examples/
│   ├── basic_usage.py           # Basic usage example
│   ├── issue_management.py      # Issue management example
│   └── webhook_listener.py      # Webhook listener example
├── gitbot_cli.py            # Command-line interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Deployment on macOS (Mac Mini Server)

### As a Launch Daemon

1. Create a launch daemon plist file:

```bash
sudo nano /Library/LaunchDaemons/com.gitbot.webhook.plist
```

Add the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gitbot.webhook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/gitbot-copilot/gitbot_cli.py</string>
        <string>webhook</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/gitbot-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/gitbot-stderr.log</string>
</dict>
</plist>
```

2. Load and start the daemon:

```bash
sudo launchctl load /Library/LaunchDaemons/com.gitbot.webhook.plist
sudo launchctl start com.gitbot.webhook
```

3. Check status:

```bash
sudo launchctl list | grep gitbot
```

### As a Background Service (Alternative)

Use `screen` or `tmux` for a simpler setup:

```bash
# Using screen
screen -S gitbot
python gitbot_cli.py webhook
# Press Ctrl+A, then D to detach

# Reattach later
screen -r gitbot
```

## Dependencies

The project uses the following Python packages (see `requirements.txt` for specific versions):

- **PyGithub** - GitHub API wrapper for Python
- **Flask** - Lightweight web framework for webhooks
- **python-dotenv** - Environment variable management
- **requests** - HTTP library for API requests

## Security Considerations

- Never commit your `.env` file with real credentials
- Use webhook secrets for production deployments
- Limit GitHub token permissions to only what's needed
- Run webhook listener behind a reverse proxy (nginx, Apache) in production
- Use HTTPS for webhook endpoints in production
- Consider rate limiting for webhook endpoints

## Future Enhancements

- Slack/Discord notifications integration
- CI/CD pipeline integration
- Advanced filtering and search capabilities
- Dashboard UI for monitoring
- Multi-repository support
- Scheduled task automation
- Custom workflow automation

## Troubleshooting

### Issue: "Repository not set" error
**Solution**: Make sure you set the repository using `--owner` and `--repo` flags or set them in `.env` file.

### Issue: "Authentication failed"
**Solution**: Verify your GitHub token has the correct permissions and is properly set in `.env` file.

### Issue: Webhook not receiving events
**Solution**: 
- Check that the webhook URL is publicly accessible
- Verify webhook secret matches
- Check firewall settings on your Mac Mini
- Review webhook delivery logs in GitHub

### Issue: Port already in use
**Solution**: Change the `WEBHOOK_PORT` in `.env` or specify a different port with `--port` flag.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

Built with ❤️ using Python and the GitHub API.