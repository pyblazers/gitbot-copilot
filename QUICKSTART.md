# GitBot - Quick Start Guide

## Prerequisites
- macOS 10.14+
- GitHub account with repository access

## Installation (5 minutes)

### 1. Clone and Setup
```bash
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot
./setup_macos.sh
```

### 2. Configure
1. Get a GitHub token: https://github.com/settings/tokens
   - Required scopes: `repo`, `admin:repo_hook`

2. Edit `.env`:
```bash
GITHUB_TOKEN=your_token_here
GITHUB_REPO=owner/repository
```

### 3. Test
```bash
source venv/bin/activate
export $(cat .env | xargs)
python cli.py analytics stats
```

## Common Commands

### List Issues
```bash
python cli.py issues list --state open
```

### Create Issue
```bash
python cli.py issues create --title "Bug fix" --labels bug
```

### List Pull Requests
```bash
python cli.py pr list
```

### Get Repository Stats
```bash
python cli.py analytics stats
python cli.py analytics commits --days 7
```

### Start Webhook Listener
```bash
python cli.py webhook
```

## Examples

Run example scripts:
```bash
python examples/basic_usage.py
python examples/issue_management.py
```

## Need Help?

See the full README.md for:
- Detailed API documentation
- Webhook configuration
- Running as a service
- Custom automation examples

## Quick Links

- GitHub Token: https://github.com/settings/tokens
- PyGithub Docs: https://pygithub.readthedocs.io/
- GitHub API: https://docs.github.com/rest
