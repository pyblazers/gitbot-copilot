"""Configuration management for GitBot."""

import os
from typing import Optional


class Config:
    """Configuration class for GitBot."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.github_token: Optional[str] = os.getenv('GITHUB_TOKEN')
        self.github_repo: Optional[str] = os.getenv('GITHUB_REPO')
        self.webhook_secret: Optional[str] = os.getenv('WEBHOOK_SECRET')
        self.webhook_port: int = int(os.getenv('WEBHOOK_PORT', '5000'))
        self.webhook_host: str = os.getenv('WEBHOOK_HOST', '0.0.0.0')
        
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        if not self.github_repo:
            raise ValueError("GITHUB_REPO environment variable is required (format: owner/repo)")
        return True
    
    @property
    def repo_owner(self) -> str:
        """Extract repository owner from GITHUB_REPO."""
        if self.github_repo and '/' in self.github_repo:
            return self.github_repo.split('/')[0]
        return ''
    
    @property
    def repo_name(self) -> str:
        """Extract repository name from GITHUB_REPO."""
        if self.github_repo and '/' in self.github_repo:
            return self.github_repo.split('/')[1]
        return ''
