"""Command-line interface for GitBot."""

import argparse
import asyncio
import logging
import sys

from gitbot.config.settings import Settings
from gitbot.core import GitBot
from gitbot.webhook.listener import WebhookListener
from gitbot.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="GitBot Copilot - AI-enhanced GitHub automation"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Start webhook server")
    server_parser.add_argument("--host", default=None, help="Server host")
    server_parser.add_argument("--port", type=int, default=None, help="Server port")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process a command")
    process_parser.add_argument("command", help="Command to process")
    process_parser.add_argument("--context", help="Additional context (JSON)")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate code")
    generate_parser.add_argument("description", help="Code description")
    generate_parser.add_argument("--language", default="python", help="Programming language")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze sentiment")
    analyze_parser.add_argument("text", help="Text to analyze")
    
    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Predict completion time")
    predict_parser.add_argument("--title", required=True, help="Issue title")
    predict_parser.add_argument("--labels", nargs="+", help="Issue labels")
    
    # Common arguments
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    parser.add_argument("--log-file", help="Log file path")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        sys.exit(1)
    
    # Execute command
    if args.command == "server":
        run_server(settings, args)
    elif args.command == "process":
        asyncio.run(process_command(settings, args))
    elif args.command == "generate":
        asyncio.run(generate_code(settings, args))
    elif args.command == "analyze":
        asyncio.run(analyze_sentiment(settings, args))
    elif args.command == "predict":
        asyncio.run(predict_completion(settings, args))
    else:
        parser.print_help()


def run_server(settings: Settings, args):
    """Run webhook server.
    
    Args:
        settings: Application settings
        args: Command-line arguments
    """
    try:
        gitbot = GitBot(settings)
        listener = WebhookListener(settings, gitbot)
        listener.run(host=args.host, port=args.port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


async def process_command(settings: Settings, args):
    """Process a command.
    
    Args:
        settings: Application settings
        args: Command-line arguments
    """
    try:
        gitbot = GitBot(settings)
        
        context = None
        if args.context:
            import json
            context = json.loads(args.context)
        
        result = await gitbot.process_command(args.command, context)
        print("\nResult:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Failed to process command: {e}")
        sys.exit(1)


async def generate_code(settings: Settings, args):
    """Generate code.
    
    Args:
        settings: Application settings
        args: Command-line arguments
    """
    try:
        gitbot = GitBot(settings)
        code = await gitbot.generate_code(args.description, args.language)
        print("\nGenerated Code:")
        print(code)
    except Exception as e:
        logger.error(f"Failed to generate code: {e}")
        sys.exit(1)


async def analyze_sentiment(settings: Settings, args):
    """Analyze sentiment.
    
    Args:
        settings: Application settings
        args: Command-line arguments
    """
    try:
        gitbot = GitBot(settings)
        result = await gitbot.analyze_sentiment(args.text)
        print("\nSentiment Analysis:")
        import json
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Failed to analyze sentiment: {e}")
        sys.exit(1)


async def predict_completion(settings: Settings, args):
    """Predict completion time.
    
    Args:
        settings: Application settings
        args: Command-line arguments
    """
    try:
        gitbot = GitBot(settings)
        issue_data = {
            "title": args.title,
            "labels": args.labels or [],
            "description": "",
            "assignees_count": 0
        }
        result = await gitbot.predict_completion_time(issue_data)
        print("\nCompletion Time Prediction:")
        import json
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Failed to predict completion time: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
