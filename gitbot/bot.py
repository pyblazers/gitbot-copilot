"""Main GitBot class integrating all modules."""

from typing import Optional

from .config import Config
from .github_client import GitHubClient
from .issue_manager import IssueManager
from .pr_manager import PullRequestManager
from .analytics import RepositoryAnalytics
from .webhook_listener import WebhookListener


class GitBot:
    """Main GitBot class for GitHub repository automation."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize GitBot.
        
        Args:
            config: Optional configuration object. If not provided, loads from environment.
        """
        self.config = config or Config()
        self.config.validate()
        
        # Initialize components
        self.client = GitHubClient(self.config)
        self.issues = IssueManager(self.client)
        self.pull_requests = PullRequestManager(self.client)
        self.analytics = RepositoryAnalytics(self.client)
        self.webhook_listener = WebhookListener(self.config)
    
    def start_webhook_listener(self):
        """Start the webhook listener server."""
        print(f"Starting webhook listener on {self.config.webhook_host}:{self.config.webhook_port}")
        print(f"Webhook URL: http://{self.config.webhook_host}:{self.config.webhook_port}/webhook")
        self.webhook_listener.start()
