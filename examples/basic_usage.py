"""Example: Basic usage of GitBot."""

import os
from gitbot.bot import GitBot
from gitbot.config import Config

# Initialize GitBot
config = Config()
bot = GitBot(config)

# List open issues
print("=== Open Issues ===")
issues = bot.issues.list_issues(state='open')
for issue in issues[:5]:  # Show first 5
    print(f"#{issue['number']}: {issue['title']}")
    print(f"  Labels: {', '.join(issue['labels'])}")
    print(f"  URL: {issue['url']}")
    print()

# Get repository statistics
print("\n=== Repository Statistics ===")
stats = bot.analytics.get_basic_stats()
print(f"Repository: {stats['full_name']}")
print(f"Description: {stats['description']}")
print(f"Stars: {stats['stars']}")
print(f"Forks: {stats['forks']}")
print(f"Open Issues: {stats['open_issues']}")
print(f"Language: {stats['language']}")

# Get commit statistics
print("\n=== Commit Statistics (Last 30 Days) ===")
commit_stats = bot.analytics.get_commit_stats(days=30)
print(f"Total Commits: {commit_stats['total_commits']}")
print(f"Average per Day: {commit_stats['average_commits_per_day']}")
print("\nCommits by Author:")
for author, count in commit_stats['commits_by_author'].items():
    print(f"  {author}: {count}")

# List pull requests
print("\n=== Open Pull Requests ===")
prs = bot.pull_requests.list_pull_requests(state='open')
for pr in prs[:5]:  # Show first 5
    print(f"#{pr['number']}: {pr['title']}")
    print(f"  Author: {pr['author']}")
    print(f"  Head: {pr['head']} -> Base: {pr['base']}")
    print(f"  Mergeable: {pr['mergeable']}")
    print(f"  URL: {pr['url']}")
    print()
