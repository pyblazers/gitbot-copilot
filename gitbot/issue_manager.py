"""Issue management module for GitBot."""

from typing import List, Dict, Optional, Any
from github.Issue import Issue

from .github_client import GitHubClient


class IssueManager:
    """Handles GitHub issue operations."""
    
    def __init__(self, client: GitHubClient):
        """
        Initialize issue manager.
        
        Args:
            client: GitHub client instance
        """
        self.client = client
        self.repo = client.connect()
    
    def list_issues(self, state: str = 'open', labels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List issues in the repository.
        
        Args:
            state: Issue state ('open', 'closed', 'all')
            labels: Optional list of labels to filter by
            
        Returns:
            List of issue dictionaries
        """
        issues = self.repo.get_issues(state=state, labels=labels or [])
        
        result = []
        for issue in issues:
            # Skip pull requests (they also appear in issues)
            if issue.pull_request:
                continue
                
            result.append({
                'number': issue.number,
                'title': issue.title,
                'state': issue.state,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat(),
                'labels': [label.name for label in issue.labels],
                'assignees': [assignee.login for assignee in issue.assignees],
                'body': issue.body,
                'url': issue.html_url,
                'author': issue.user.login if issue.user else None
            })
        
        return result
    
    def create_issue(
        self,
        title: str,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new issue.
        
        Args:
            title: Issue title
            body: Issue body/description
            labels: List of label names to add
            assignees: List of usernames to assign
            
        Returns:
            Created issue dictionary
        """
        issue = self.repo.create_issue(
            title=title,
            body=body or '',
            labels=labels or [],
            assignees=assignees or []
        )
        
        return {
            'number': issue.number,
            'title': issue.title,
            'state': issue.state,
            'url': issue.html_url,
            'labels': [label.name for label in issue.labels],
            'assignees': [assignee.login for assignee in issue.assignees]
        }
    
    def assign_issue(self, issue_number: int, assignees: List[str]) -> Dict[str, Any]:
        """
        Assign users to an issue.
        
        Args:
            issue_number: Issue number
            assignees: List of usernames to assign
            
        Returns:
            Updated issue dictionary
        """
        issue = self.repo.get_issue(issue_number)
        issue.edit(assignees=assignees)
        
        return {
            'number': issue.number,
            'title': issue.title,
            'assignees': [assignee.login for assignee in issue.assignees]
        }
    
    def add_labels(self, issue_number: int, labels: List[str]) -> Dict[str, Any]:
        """
        Add labels to an issue.
        
        Args:
            issue_number: Issue number
            labels: List of label names to add
            
        Returns:
            Updated issue dictionary
        """
        issue = self.repo.get_issue(issue_number)
        issue.add_to_labels(*labels)
        
        return {
            'number': issue.number,
            'title': issue.title,
            'labels': [label.name for label in issue.labels]
        }
    
    def close_issue(self, issue_number: int) -> Dict[str, Any]:
        """
        Close an issue.
        
        Args:
            issue_number: Issue number
            
        Returns:
            Updated issue dictionary
        """
        issue = self.repo.get_issue(issue_number)
        issue.edit(state='closed')
        
        return {
            'number': issue.number,
            'title': issue.title,
            'state': issue.state
        }
