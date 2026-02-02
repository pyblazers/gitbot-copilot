#!/usr/bin/env python3
"""Test script to verify GitBot installation and structure."""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from gitbot.bot import GitBot
        from gitbot.config import Config
        from gitbot.github_client import GitHubClient
        from gitbot.issue_manager import IssueManager
        from gitbot.pr_manager import PullRequestManager
        from gitbot.analytics import RepositoryAnalytics
        from gitbot.webhook_listener import WebhookListener
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration management."""
    print("\nTesting configuration...")
    from gitbot.config import Config
    
    # Save existing env vars
    old_token = os.environ.get('GITHUB_TOKEN')
    old_repo = os.environ.get('GITHUB_REPO')
    
    try:
        # Test missing required config
        os.environ.pop('GITHUB_TOKEN', None)
        os.environ.pop('GITHUB_REPO', None)
        
        config = Config()
        try:
            config.validate()
            print("✗ Should have raised error for missing config")
            return False
        except ValueError:
            print("✓ Config validation works")
        
        # Test valid config
        os.environ['GITHUB_TOKEN'] = 'test_token'
        os.environ['GITHUB_REPO'] = 'owner/repo'
        
        config = Config()
        config.validate()
        
        assert config.repo_owner == 'owner', "Repo owner parsing failed"
        assert config.repo_name == 'repo', "Repo name parsing failed"
        print("✓ Config parsing works")
        
        return True
    finally:
        # Restore env vars
        if old_token:
            os.environ['GITHUB_TOKEN'] = old_token
        else:
            os.environ.pop('GITHUB_TOKEN', None)
        
        if old_repo:
            os.environ['GITHUB_REPO'] = old_repo
        else:
            os.environ.pop('GITHUB_REPO', None)


def test_cli():
    """Test CLI interface."""
    print("\nTesting CLI...")
    import subprocess
    
    result = subprocess.run(
        ['python3', 'cli.py', '--help'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and 'GitBot' in result.stdout:
        print("✓ CLI interface works")
        return True
    else:
        print("✗ CLI interface failed")
        return False


def test_structure():
    """Test project structure."""
    print("\nTesting project structure...")
    
    required_files = [
        'gitbot/__init__.py',
        'gitbot/bot.py',
        'gitbot/config.py',
        'gitbot/github_client.py',
        'gitbot/issue_manager.py',
        'gitbot/pr_manager.py',
        'gitbot/analytics.py',
        'gitbot/webhook_listener.py',
        'cli.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        '.gitignore',
        'setup_macos.sh',
        'examples/basic_usage.py',
        'examples/issue_management.py',
        'examples/pr_automation.py',
        'examples/webhook_example.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        return False
    else:
        print("✓ All required files present")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("GitBot Installation Test")
    print("=" * 60)
    
    tests = [
        test_structure,
        test_imports,
        test_config,
        test_cli
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nGitBot is ready to use!")
        print("Next steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your GitHub token to .env")
        print("3. Run: python3 cli.py --help")
        return 0
    else:
        print(f"✗ {results.count(False)} test(s) failed")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
