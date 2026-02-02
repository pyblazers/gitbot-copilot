# macOS Deployment Guide

Complete guide for deploying GitBot Copilot on Mac Mini or other macOS systems.

## System Requirements

- **macOS**: 10.15 (Catalina) or higher
- **RAM**: Minimum 8GB (16GB recommended for local LLMs)
- **Storage**: 10GB free space (more if using local LLMs)
- **Network**: Internet connection for API calls

## Installation

### Step 1: System Preparation

#### Update macOS
```bash
softwareupdate --list
softwareupdate --install --all
```

#### Install Xcode Command Line Tools
```bash
xcode-select --install
```

### Step 2: Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Add Homebrew to PATH (if needed):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 3: Install Dependencies

#### Python 3.11
```bash
brew install python@3.11
```

#### Git (if not already installed)
```bash
brew install git
```

#### Optional: Node.js (for additional tools)
```bash
brew install node
```

### Step 4: Clone and Install GitBot

```bash
# Create installation directory
mkdir -p ~/gitbot
cd ~/gitbot

# Clone repository
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install GitBot
pip install --upgrade pip
pip install -e .
```

### Step 5: Configuration

#### Create Configuration File
```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

#### Essential Configuration
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=/Users/yourusername/gitbot/gitbot.log
```

## Running as a Service

### Option 1: Using launchd (Recommended for macOS)

#### Create Launch Agent

Create file: `~/Library/LaunchAgents/com.gitbot.webhook.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gitbot.webhook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/yourusername/gitbot/gitbot-copilot/venv/bin/gitbot</string>
        <string>server</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>5000</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/yourusername/gitbot/gitbot-copilot</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/yourusername/gitbot/logs/gitbot-out.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yourusername/gitbot/logs/gitbot-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
```

#### Load and Start Service
```bash
# Create logs directory
mkdir -p ~/gitbot/logs

# Load service
launchctl load ~/Library/LaunchAgents/com.gitbot.webhook.plist

# Start service
launchctl start com.gitbot.webhook

# Check status
launchctl list | grep gitbot
```

#### Service Management Commands
```bash
# Stop service
launchctl stop com.gitbot.webhook

# Unload service
launchctl unload ~/Library/LaunchAgents/com.gitbot.webhook.plist

# View logs
tail -f ~/gitbot/logs/gitbot-out.log
```

### Option 2: Using Screen (Simple Alternative)

```bash
# Start in detached screen session
screen -dmS gitbot bash -c 'cd ~/gitbot/gitbot-copilot && source venv/bin/activate && gitbot server'

# Reattach to session
screen -r gitbot

# Detach: Press Ctrl+A, then D
```

## Network Configuration

### Local Network Access

GitBot will be accessible at:
- Local: `http://localhost:5000`
- Network: `http://[YOUR_MAC_IP]:5000`

Find your IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Using ngrok for External Access (Development/Testing)

```bash
# Install ngrok
brew install ngrok

# Start ngrok tunnel
ngrok http 5000

# Use the provided URL as your webhook endpoint
```

### Firewall Configuration

Allow incoming connections:
```bash
# System Preferences → Security & Privacy → Firewall → Firewall Options
# Add Python/GitBot and allow incoming connections
```

Or via command line:
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/bin/python3
```

## Performance Optimization

### Memory Management

For systems with limited RAM, disable unused features:
```bash
# In .env
ENABLE_PREDICTIVE_TASKS=False
ENABLE_ANALYTICS=False
```

### Using Local LLMs

For better performance and privacy:

```bash
# Install llama-cpp-python with optimizations
pip install llama-cpp-python

# Download model (example)
mkdir -p ~/gitbot/models
cd ~/gitbot/models
wget https://huggingface.co/...model-link.../model.gguf

# Configure in .env
USE_LOCAL_LLM=True
LOCAL_LLM_MODEL_PATH=/Users/yourusername/gitbot/models/model.gguf
LOCAL_LLM_TYPE=llama
```

## Monitoring and Maintenance

### Log Rotation

Create `/etc/newsyslog.d/gitbot.conf`:
```
/Users/yourusername/gitbot/logs/*.log    644  5    10000  *    GZ
```

### Health Checks

Create monitoring script: `~/gitbot/health_check.sh`
```bash
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
if [ "$response" != "200" ]; then
    echo "GitBot is down, restarting..."
    launchctl restart com.gitbot.webhook
fi
```

Add to crontab:
```bash
crontab -e
# Add: */5 * * * * /Users/yourusername/gitbot/health_check.sh
```

### Updates

```bash
cd ~/gitbot/gitbot-copilot
git pull
source venv/bin/activate
pip install -e . --upgrade
launchctl restart com.gitbot.webhook
```

## Security Best Practices

1. **API Keys**: Store in secure keychain
2. **File Permissions**: Restrict .env file
   ```bash
   chmod 600 .env
   ```
3. **Firewall**: Only open necessary ports
4. **Updates**: Keep system and dependencies updated
5. **Monitoring**: Enable logging and monitoring

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Denied
```bash
# Fix file permissions
chmod +x ~/Library/LaunchAgents/com.gitbot.webhook.plist
```

### Service Won't Start
```bash
# Check logs
cat ~/gitbot/logs/gitbot-error.log

# Verify Python path
which python3

# Test manually
cd ~/gitbot/gitbot-copilot
source venv/bin/activate
gitbot server
```

### High CPU Usage
```bash
# Monitor process
top -pid $(pgrep -f gitbot)

# Consider using local LLMs or reducing features
```

## Backup and Recovery

### Backup Configuration
```bash
# Backup .env and models
tar -czf gitbot-backup-$(date +%Y%m%d).tar.gz \
    ~/gitbot/gitbot-copilot/.env \
    ~/gitbot/models/
```

### Restore
```bash
tar -xzf gitbot-backup-*.tar.gz -C ~/
launchctl restart com.gitbot.webhook
```

## Support

For Mac-specific issues:
- Apple Developer Documentation
- Homebrew Issues: `brew doctor`
- Python Issues: Check Python version compatibility

For GitBot issues:
- GitHub Issues: https://github.com/pyblazers/gitbot-copilot/issues
