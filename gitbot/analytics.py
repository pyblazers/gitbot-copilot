"""Repository analytics module for GitBot."""

from typing import Dict, List, Any
from datetime import datetime, timedelta

from .github_client import GitHubClient


class RepositoryAnalytics:
    """Provides repository analytics and statistics."""
    
    def __init__(self, client: GitHubClient):
        """
        Initialize analytics module.
        
        Args:
            client: GitHub client instance
        """
        self.client = client
        self.repo = client.connect()
    
    def get_basic_stats(self) -> Dict[str, Any]:
        """
        Get basic repository statistics.
        
        Returns:
            Dictionary with basic stats
        """
        return {
            'name': self.repo.name,
            'full_name': self.repo.full_name,
            'description': self.repo.description,
            'stars': self.repo.stargazers_count,
            'watchers': self.repo.watchers_count,
            'forks': self.repo.forks_count,
            'open_issues': self.repo.open_issues_count,
            'language': self.repo.language,
            'created_at': self.repo.created_at.isoformat(),
            'updated_at': self.repo.updated_at.isoformat(),
            'size': self.repo.size,
            'default_branch': self.repo.default_branch,
            'url': self.repo.html_url
        }
    
    def get_commit_stats(self, days: int = 30) -> Dict[str, Any]:
        """
        Get commit statistics for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with commit stats
        """
        since = datetime.now() - timedelta(days=days)
        commits = self.repo.get_commits(since=since)
        
        commit_list = list(commits)
        total_commits = len(commit_list)
        
        # Count commits by author
        authors: Dict[str, int] = {}
        for commit in commit_list:
            if commit.author:
                author = commit.author.login
                authors[author] = authors.get(author, 0) + 1
        
        return {
            'total_commits': total_commits,
            'period_days': days,
            'since': since.isoformat(),
            'commits_by_author': authors,
            'average_commits_per_day': round(total_commits / days, 2) if days > 0 else 0
        }
    
    def get_contributor_stats(self) -> List[Dict[str, Any]]:
        """
        Get contributor statistics.
        
        Returns:
            List of contributor dictionaries
        """
        contributors = self.repo.get_contributors()
        
        result = []
        for contributor in contributors:
            result.append({
                'login': contributor.login,
                'contributions': contributor.contributions,
                'url': contributor.html_url
            })
        
        return result
    
    def get_recent_activity(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent repository activity.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            Dictionary with recent activity
        """
        # Get recent commits
        commits = self.repo.get_commits()
        recent_commits = []
        for i, commit in enumerate(commits):
            if i >= limit:
                break
            recent_commits.append({
                'sha': commit.sha[:7],
                'message': commit.commit.message.split('\n')[0],
                'author': commit.author.login if commit.author else 'Unknown',
                'date': commit.commit.author.date.isoformat()
            })
        
        # Get recent issues
        issues = self.repo.get_issues(state='all', sort='updated')
        recent_issues = []
        for i, issue in enumerate(issues):
            if i >= limit:
                break
            if issue.pull_request:
                continue
            recent_issues.append({
                'number': issue.number,
                'title': issue.title,
                'state': issue.state,
                'updated_at': issue.updated_at.isoformat()
            })
        
        return {
            'recent_commits': recent_commits,
            'recent_issues': recent_issues
        }
    
    def get_language_stats(self) -> Dict[str, int]:
        """
        Get programming language statistics.
        
        Returns:
            Dictionary with language breakdown
        """
        languages = self.repo.get_languages()
        return dict(languages)
    
    def get_branch_stats(self) -> Dict[str, Any]:
        """
        Get branch statistics.
        
        Returns:
            Dictionary with branch stats
        """
        branches = self.repo.get_branches()
        branch_list = list(branches)
        
        return {
            'total_branches': len(branch_list),
            'default_branch': self.repo.default_branch,
            'branches': [branch.name for branch in branch_list[:20]]  # Limit to 20
        }
