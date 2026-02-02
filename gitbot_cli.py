#!/usr/bin/env python3
"""
GitBot CLI - Command-line interface for GitBot
"""

import sys
import argparse
import json
from gitbot import GitBot
from gitbot.modules.webhook_listener import (
    handle_push_event,
    handle_pull_request_event,
    handle_issues_event
)


def main():
    parser = argparse.ArgumentParser(
        description="GitBot - Automate GitHub repository interactions"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Issue commands
    issue_parser = subparsers.add_parser("issues", help="Manage issues")
    issue_parser.add_argument("--list", action="store_true", help="List open issues")
    issue_parser.add_argument("--create", action="store_true", help="Create a new issue")
    issue_parser.add_argument("--title", help="Issue title")
    issue_parser.add_argument("--body", help="Issue body/description")
    issue_parser.add_argument("--labels", nargs="+", help="Issue labels")
    issue_parser.add_argument("--assignees", nargs="+", help="Assignees")
    issue_parser.add_argument("--state", default="open", choices=["open", "closed", "all"], help="Issue state")
    
    # Pull request commands
    pr_parser = subparsers.add_parser("pr", help="Manage pull requests")
    pr_parser.add_argument("--list", action="store_true", help="List pull requests")
    pr_parser.add_argument("--merge", type=int, help="Merge pull request by number")
    pr_parser.add_argument("--get", type=int, help="Get pull request details by number")
    pr_parser.add_argument("--state", default="open", choices=["open", "closed", "all"], help="PR state")
    pr_parser.add_argument("--method", default="merge", choices=["merge", "squash", "rebase"], help="Merge method")
    
    # Analytics commands
    analytics_parser = subparsers.add_parser("analytics", help="Get repository analytics")
    analytics_parser.add_argument("--stats", action="store_true", help="Get basic stats")
    analytics_parser.add_argument("--commits", action="store_true", help="Get commit stats")
    analytics_parser.add_argument("--contributors", action="store_true", help="Get contributor stats")
    analytics_parser.add_argument("--activity", action="store_true", help="Get recent activity")
    analytics_parser.add_argument("--languages", action="store_true", help="Get language stats")
    analytics_parser.add_argument("--releases", action="store_true", help="Get release stats")
    analytics_parser.add_argument("--days", type=int, default=30, help="Days for commit stats")
    
    # Webhook commands
    webhook_parser = subparsers.add_parser("webhook", help="Start webhook listener")
    webhook_parser.add_argument("--port", type=int, help="Port to run on")
    webhook_parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    # User info command
    user_parser = subparsers.add_parser("user", help="Get user information")
    
    # Repository arguments
    parser.add_argument("--owner", help="Repository owner")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument("--token", help="GitHub token")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize GitBot
        bot = GitBot(
            github_token=args.token,
            owner=args.owner,
            repo_name=args.repo
        )
        
        # Handle commands
        if args.command == "issues":
            handle_issues_command(bot, args)
        elif args.command == "pr":
            handle_pr_command(bot, args)
        elif args.command == "analytics":
            handle_analytics_command(bot, args)
        elif args.command == "webhook":
            handle_webhook_command(bot, args)
        elif args.command == "user":
            handle_user_command(bot, args)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def handle_issues_command(bot, args):
    """Handle issue-related commands"""
    if args.list:
        issues = bot.issue_manager.list_open_issues(state=args.state)
        print(json.dumps(issues, indent=2))
    elif args.create:
        if not args.title:
            print("Error: --title is required to create an issue", file=sys.stderr)
            sys.exit(1)
        issue = bot.issue_manager.create_issue(
            title=args.title,
            body=args.body or "",
            labels=args.labels,
            assignees=args.assignees
        )
        print(json.dumps(issue, indent=2))
    else:
        print("Error: Specify --list or --create", file=sys.stderr)
        sys.exit(1)


def handle_pr_command(bot, args):
    """Handle pull request-related commands"""
    if args.list:
        prs = bot.pr_manager.list_pull_requests(state=args.state)
        print(json.dumps(prs, indent=2))
    elif args.merge:
        result = bot.pr_manager.merge_pull_request(args.merge, merge_method=args.method)
        print(json.dumps(result, indent=2))
    elif args.get:
        pr = bot.pr_manager.get_pull_request(args.get)
        print(json.dumps(pr, indent=2))
    else:
        print("Error: Specify --list, --merge, or --get", file=sys.stderr)
        sys.exit(1)


def handle_analytics_command(bot, args):
    """Handle analytics-related commands"""
    if args.stats:
        stats = bot.analytics.get_basic_stats()
        print(json.dumps(stats, indent=2))
    elif args.commits:
        stats = bot.analytics.get_commit_stats(since_days=args.days)
        print(json.dumps(stats, indent=2))
    elif args.contributors:
        stats = bot.analytics.get_contributor_stats()
        print(json.dumps(stats, indent=2))
    elif args.activity:
        stats = bot.analytics.get_recent_activity()
        print(json.dumps(stats, indent=2))
    elif args.languages:
        stats = bot.analytics.get_language_stats()
        print(json.dumps(stats, indent=2))
    elif args.releases:
        stats = bot.analytics.get_release_stats()
        print(json.dumps(stats, indent=2))
    else:
        print("Error: Specify an analytics option", file=sys.stderr)
        sys.exit(1)


def handle_webhook_command(bot, args):
    """Handle webhook-related commands"""
    # Register example handlers
    bot.webhook_listener.register_handler("push", handle_push_event)
    bot.webhook_listener.register_handler("pull_request", handle_pull_request_event)
    bot.webhook_listener.register_handler("issues", handle_issues_event)
    
    # Start the listener
    bot.webhook_listener.start(debug=args.debug)


def handle_user_command(bot, args):
    """Handle user-related commands"""
    user_info = bot.get_user_info()
    print(json.dumps(user_info, indent=2))


if __name__ == "__main__":
    main()
