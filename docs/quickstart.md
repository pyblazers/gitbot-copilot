# Quick Start Guide

This guide will help you get GitBot Copilot up and running on your macOS system in less than 15 minutes.

## Prerequisites

- macOS 10.15 or higher
- Command-line access (Terminal)
- OpenAI API key
- GitHub personal access token

## Installation Steps

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3.11

```bash
brew install python@3.11
```

### 3. Clone and Setup

```bash
# Clone repository
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

### 4. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your favorite editor
nano .env
```

Add your API keys:
```
OPENAI_API_KEY=sk-...your-key-here
GITHUB_TOKEN=ghp_...your-token-here
```

### 5. Verify Installation

```bash
gitbot --help
```

You should see the GitBot help menu.

## First Use

### Test Basic Functionality

```bash
# Analyze sentiment
gitbot analyze "This is amazing work!"

# Generate code
gitbot generate "A function to sort a list of numbers" --language python
```

### Start Webhook Server

```bash
gitbot server --host 0.0.0.0 --port 5000
```

Visit `http://localhost:5000/health` in your browser to verify the server is running.

## Next Steps

1. **Configure GitHub Webhook**: See [Webhook Setup](webhook_setup.md)
2. **Explore Examples**: Check the `examples/` directory
3. **Customize Settings**: Review `.env` configuration options
4. **Read Full Documentation**: See [API Documentation](api_documentation.md)

## Troubleshooting

### Issue: "Command not found: gitbot"

Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

### Issue: "Missing API key"

Ensure `.env` file contains valid API keys:
```bash
cat .env | grep OPENAI_API_KEY
```

### Issue: Package installation errors

Try upgrading pip:
```bash
pip install --upgrade pip
pip install -e .
```

## Getting Help

- GitHub Issues: https://github.com/pyblazers/gitbot-copilot/issues
- Documentation: See `/docs` directory
- Examples: See `/examples` directory
