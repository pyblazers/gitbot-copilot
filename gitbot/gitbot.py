"""
Main GitBot class that coordinates all modules
"""

import os
from github import Github
from dotenv import load_dotenv
from .modules.issue_manager import IssueManager
from .modules.pr_manager import PRManager
from .modules.analytics import RepositoryAnalytics
from .modules.webhook_listener import WebhookListener


class GitBot:
    """
    Main GitBot class for automating GitHub repository interactions
    """

    def __init__(self, github_token=None, owner=None, repo_name=None):
        """
        Initialize GitBot with GitHub credentials

        Args:
            github_token (str): GitHub Personal Access Token
            owner (str): Repository owner/username
            repo_name (str): Repository name
        """
        # Load environment variables
        load_dotenv()

        # Set credentials
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.owner = owner or os.getenv("GITHUB_OWNER")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")

        if not self.github_token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass it as parameter.")

        # Initialize GitHub client
        self.github_client = Github(self.github_token)
        
        # Get repository object if owner and repo_name are provided
        self.repo = None
        if self.owner and self.repo_name:
            self.repo = self.github_client.get_repo(f"{self.owner}/{self.repo_name}")

        # Initialize modules
        self.issue_manager = IssueManager(self.github_client, self.repo)
        self.pr_manager = PRManager(self.github_client, self.repo)
        self.analytics = RepositoryAnalytics(self.github_client, self.repo)
        self.webhook_listener = WebhookListener()

    def set_repository(self, owner, repo_name):
        """
        Set or change the repository to work with

        Args:
            owner (str): Repository owner/username
            repo_name (str): Repository name
        """
        self.owner = owner
        self.repo_name = repo_name
        self.repo = self.github_client.get_repo(f"{owner}/{repo_name}")
        
        # Update modules with new repository
        self.issue_manager.set_repository(self.repo)
        self.pr_manager.set_repository(self.repo)
        self.analytics.set_repository(self.repo)

    def get_user_info(self):
        """
        Get authenticated user information

        Returns:
            dict: User information
        """
        user = self.github_client.get_user()
        return {
            "login": user.login,
            "name": user.name,
            "email": user.email,
            "public_repos": user.public_repos,
            "followers": user.followers,
            "following": user.following,
        }
