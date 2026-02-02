#!/usr/bin/env python3
"""Command-line interface for GitBot."""

import argparse
import json
import sys
from typing import Optional

from gitbot.bot import GitBot
from gitbot.config import Config


def format_output(data, output_format: str = 'json'):
    """Format output data."""
    if output_format == 'json':
        return json.dumps(data, indent=2)
    return str(data)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='GitBot - GitHub Repository Automation Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Issue commands
    issues_parser = subparsers.add_parser('issues', help='Manage issues')
    issues_subparsers = issues_parser.add_subparsers(dest='subcommand')
    
    # List issues
    list_issues_parser = issues_subparsers.add_parser('list', help='List issues')
    list_issues_parser.add_argument('--state', default='open', choices=['open', 'closed', 'all'])
    list_issues_parser.add_argument('--labels', nargs='+', help='Filter by labels')
    
    # Create issue
    create_issue_parser = issues_subparsers.add_parser('create', help='Create issue')
    create_issue_parser.add_argument('--title', required=True, help='Issue title')
    create_issue_parser.add_argument('--body', help='Issue body')
    create_issue_parser.add_argument('--labels', nargs='+', help='Labels to add')
    create_issue_parser.add_argument('--assignees', nargs='+', help='Users to assign')
    
    # Assign issue
    assign_issue_parser = issues_subparsers.add_parser('assign', help='Assign issue')
    assign_issue_parser.add_argument('--number', type=int, required=True, help='Issue number')
    assign_issue_parser.add_argument('--assignees', nargs='+', required=True, help='Users to assign')
    
    # Pull request commands
    pr_parser = subparsers.add_parser('pr', help='Manage pull requests')
    pr_subparsers = pr_parser.add_subparsers(dest='subcommand')
    
    # List PRs
    list_pr_parser = pr_subparsers.add_parser('list', help='List pull requests')
    list_pr_parser.add_argument('--state', default='open', choices=['open', 'closed', 'all'])
    
    # Get PR details
    get_pr_parser = pr_subparsers.add_parser('get', help='Get pull request details')
    get_pr_parser.add_argument('--number', type=int, required=True, help='PR number')
    
    # Merge PR
    merge_pr_parser = pr_subparsers.add_parser('merge', help='Merge pull request')
    merge_pr_parser.add_argument('--number', type=int, required=True, help='PR number')
    merge_pr_parser.add_argument('--method', default='merge', choices=['merge', 'squash', 'rebase'])
    merge_pr_parser.add_argument('--title', help='Commit title')
    merge_pr_parser.add_argument('--message', help='Commit message')
    
    # Analytics commands
    analytics_parser = subparsers.add_parser('analytics', help='Repository analytics')
    analytics_subparsers = analytics_parser.add_subparsers(dest='subcommand')
    
    # Basic stats
    analytics_subparsers.add_parser('stats', help='Get basic repository statistics')
    
    # Commit stats
    commit_stats_parser = analytics_subparsers.add_parser('commits', help='Get commit statistics')
    commit_stats_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Contributors
    analytics_subparsers.add_parser('contributors', help='Get contributor statistics')
    
    # Recent activity
    activity_parser = analytics_subparsers.add_parser('activity', help='Get recent activity')
    activity_parser.add_argument('--limit', type=int, default=10, help='Number of events to return')
    
    # Language stats
    analytics_subparsers.add_parser('languages', help='Get language statistics')
    
    # Webhook listener
    webhook_parser = subparsers.add_parser('webhook', help='Start webhook listener')
    webhook_parser.add_argument('--host', help='Host to bind to')
    webhook_parser.add_argument('--port', type=int, help='Port to bind to')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize GitBot
        config = Config()
        
        # Override config with CLI arguments
        if args.command == 'webhook':
            if args.host:
                config.webhook_host = args.host
            if args.port:
                config.webhook_port = args.port
        
        bot = GitBot(config)
        
        # Execute command
        if args.command == 'issues':
            if args.subcommand == 'list':
                result = bot.issues.list_issues(state=args.state, labels=args.labels)
            elif args.subcommand == 'create':
                result = bot.issues.create_issue(
                    title=args.title,
                    body=args.body,
                    labels=args.labels,
                    assignees=args.assignees
                )
            elif args.subcommand == 'assign':
                result = bot.issues.assign_issue(args.number, args.assignees)
            else:
                parser.print_help()
                return
            
            print(format_output(result))
        
        elif args.command == 'pr':
            if args.subcommand == 'list':
                result = bot.pull_requests.list_pull_requests(state=args.state)
            elif args.subcommand == 'get':
                result = bot.pull_requests.get_pull_request(args.number)
            elif args.subcommand == 'merge':
                result = bot.pull_requests.merge_pull_request(
                    pr_number=args.number,
                    commit_title=args.title,
                    commit_message=args.message,
                    merge_method=args.method
                )
            else:
                parser.print_help()
                return
            
            print(format_output(result))
        
        elif args.command == 'analytics':
            if args.subcommand == 'stats':
                result = bot.analytics.get_basic_stats()
            elif args.subcommand == 'commits':
                result = bot.analytics.get_commit_stats(days=args.days)
            elif args.subcommand == 'contributors':
                result = bot.analytics.get_contributor_stats()
            elif args.subcommand == 'activity':
                result = bot.analytics.get_recent_activity(limit=args.limit)
            elif args.subcommand == 'languages':
                result = bot.analytics.get_language_stats()
            else:
                parser.print_help()
                return
            
            print(format_output(result))
        
        elif args.command == 'webhook':
            bot.start_webhook_listener()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
