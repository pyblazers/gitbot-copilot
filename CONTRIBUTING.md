# Contributing to GitBot

Thank you for your interest in contributing to GitBot! This document provides guidelines and instructions for contributing.

## Project Structure

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
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/gitbot-copilot.git
cd gitbot-copilot
```

3. Set up development environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create a `.env` file for testing:
```bash
cp .env.example .env
# Edit .env with your test credentials
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Write Code

- Follow existing code style and patterns
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Use type hints where appropriate

### 3. Test Your Changes

```bash
# Run installation test
python3 test_installation.py

# Test CLI commands
python3 cli.py --help
python3 cli.py issues --help

# Test your feature with real GitHub repo (optional)
export GITHUB_TOKEN=your_token
export GITHUB_REPO=test/repo
python3 cli.py analytics stats
```

### 4. Update Documentation

- Update README.md if adding new features
- Add examples to the `examples/` directory
- Update QUICKSTART.md for user-facing changes

### 5. Commit Changes

```bash
git add .
git commit -m "Add feature: description of your changes"
```

## Code Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add comments for complex logic

Example:

```python
def create_issue(
    self,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new issue.
    
    Args:
        title: Issue title
        body: Optional issue description
        labels: Optional list of label names
        
    Returns:
        Dictionary with issue details
    """
    # Implementation here
```

## Adding New Features

### Adding a New Manager Module

1. Create a new file in `gitbot/` (e.g., `gitbot/project_manager.py`)
2. Follow the existing manager pattern:

```python
from .github_client import GitHubClient

class ProjectManager:
    """Handles GitHub Projects operations."""
    
    def __init__(self, client: GitHubClient):
        self.client = client
        self.repo = client.connect()
    
    def list_projects(self):
        """List projects in the repository."""
        # Implementation
```

3. Import and initialize in `gitbot/bot.py`:

```python
from .project_manager import ProjectManager

class GitBot:
    def __init__(self, config: Optional[Config] = None):
        # ... existing code ...
        self.projects = ProjectManager(self.client)
```

4. Add CLI commands in `cli.py`
5. Add examples in `examples/`
6. Update README.md

### Adding Webhook Handlers

Add new event handlers in your code:

```python
bot = GitBot()

def handle_my_event(payload):
    """Handle my custom event."""
    # Process payload
    return {'status': 'processed'}

bot.webhook_listener.register_handler('my_event', handle_my_event)
```

## Testing Guidelines

- Test all new features manually
- Ensure existing features still work
- Test edge cases and error conditions
- Verify CLI commands work as expected
- Test with different repository types

## Pull Request Process

1. Update documentation
2. Test thoroughly
3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request with:
   - Clear description of changes
   - Why the change is needed
   - How to test the changes
   - Any breaking changes

## Feature Ideas

Looking for ideas? Here are some features to implement:

### High Priority
- [ ] Unit tests with pytest
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Docker support
- [ ] Error handling improvements
- [ ] Rate limit handling

### Medium Priority
- [ ] Slack/Discord notifications
- [ ] GitHub Projects support
- [ ] Automated issue triage
- [ ] PR review automation
- [ ] Code review bot comments
- [ ] Scheduled tasks (cron-like)

### Low Priority
- [ ] Web dashboard
- [ ] Custom command parser (@bot commands)
- [ ] Metrics and reporting
- [ ] Multi-repository support
- [ ] GitHub App support
- [ ] Custom workflows

## Code Review Checklist

Before submitting, ensure:

- [ ] Code follows project style
- [ ] All functions have docstrings
- [ ] New features are documented
- [ ] Examples are provided
- [ ] Manual testing completed
- [ ] No hardcoded credentials
- [ ] Error handling is robust
- [ ] CLI commands work correctly
- [ ] README updated if needed

## Getting Help

- Check existing issues and PRs
- Review the examples in `examples/`
- Read the full README.md
- Open an issue for questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or reach out to the maintainers!
