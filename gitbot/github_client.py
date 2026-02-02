"""GitHub API client for GitBot."""

from typing import List, Dict, Optional, Any
from github import Github, GithubException
from github.Repository import Repository
from github.Issue import Issue
from github.PullRequest import PullRequest

from .config import Config


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, config: Config):
        """
        Initialize GitHub client.
        
        Args:
            config: GitBot configuration
        """
        self.config = config
        self.github = Github(config.github_token)
        self.repo: Optional[Repository] = None
        
    def connect(self) -> Repository:
        """
        Connect to the configured repository.
        
        Returns:
            Repository object
        """
        if not self.repo:
            self.repo = self.github.get_repo(self.config.github_repo)
        return self.repo
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current API rate limit status.
        
        Returns:
            Dictionary with rate limit information
        """
        rate_limit = self.github.get_rate_limit()
        return {
            'core': {
                'limit': rate_limit.core.limit,
                'remaining': rate_limit.core.remaining,
                'reset': rate_limit.core.reset
            }
        }
