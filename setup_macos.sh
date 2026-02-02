#!/bin/bash
# GitBot Setup Script for macOS
# This script installs all dependencies required for GitBot

set -e

echo "🤖 GitBot Setup for macOS"
echo "=========================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is already installed"
fi

# Update Homebrew
echo ""
echo "📦 Updating Homebrew..."
brew update

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Installing Python 3..."
    brew install python3
else
    echo "✅ Python 3 is already installed ($(python3 --version))"
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Installing pip..."
    python3 -m ensurepip --upgrade
else
    echo "✅ pip3 is already installed"
fi

# Create virtual environment
echo ""
echo "🔧 Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo ""
echo "📚 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your GitHub credentials"
    echo "   - Get a personal access token from: https://github.com/settings/tokens"
    echo "   - Required scopes: repo, admin:repo_hook, admin:org_hook"
else
    echo ""
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GitHub credentials"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run GitBot: python cli.py --help"
echo ""
