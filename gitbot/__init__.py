"""
GitBot - A Python bot for automating GitHub repository interactions
"""

__version__ = "1.0.0"
__author__ = "GitBot Contributors"

from .gitbot import GitBot
from .modules.issue_manager import IssueManager
from .modules.pr_manager import PRManager
from .modules.analytics import RepositoryAnalytics
from .modules.webhook_listener import WebhookListener

__all__ = [
    "GitBot",
    "IssueManager",
    "PRManager",
    "RepositoryAnalytics",
    "WebhookListener",
]
