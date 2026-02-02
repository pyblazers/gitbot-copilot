"""Pull request management module for GitBot."""

from typing import List, Dict, Optional, Any
from github.PullRequest import PullRequest

from .github_client import GitHubClient


class PullRequestManager:
    """Handles GitHub pull request operations."""
    
    def __init__(self, client: GitHubClient):
        """
        Initialize PR manager.
        
        Args:
            client: GitHub client instance
        """
        self.client = client
        self.repo = client.connect()
    
    def list_pull_requests(self, state: str = 'open') -> List[Dict[str, Any]]:
        """
        List pull requests in the repository.
        
        Args:
            state: PR state ('open', 'closed', 'all')
            
        Returns:
            List of PR dictionaries
        """
        prs = self.repo.get_pulls(state=state)
        
        result = []
        for pr in prs:
            result.append({
                'number': pr.number,
                'title': pr.title,
                'state': pr.state,
                'created_at': pr.created_at.isoformat(),
                'updated_at': pr.updated_at.isoformat(),
                'merged': pr.merged,
                'mergeable': pr.mergeable,
                'head': pr.head.ref,
                'base': pr.base.ref,
                'author': pr.user.login if pr.user else None,
                'url': pr.html_url,
                'body': pr.body
            })
        
        return result
    
    def get_pull_request(self, pr_number: int) -> Dict[str, Any]:
        """
        Get details of a specific pull request.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            PR dictionary
        """
        pr = self.repo.get_pull(pr_number)
        
        return {
            'number': pr.number,
            'title': pr.title,
            'state': pr.state,
            'created_at': pr.created_at.isoformat(),
            'updated_at': pr.updated_at.isoformat(),
            'merged': pr.merged,
            'mergeable': pr.mergeable,
            'mergeable_state': pr.mergeable_state,
            'head': pr.head.ref,
            'base': pr.base.ref,
            'author': pr.user.login if pr.user else None,
            'url': pr.html_url,
            'body': pr.body,
            'commits': pr.commits,
            'additions': pr.additions,
            'deletions': pr.deletions,
            'changed_files': pr.changed_files
        }
    
    def merge_pull_request(
        self,
        pr_number: int,
        commit_title: Optional[str] = None,
        commit_message: Optional[str] = None,
        merge_method: str = 'merge'
    ) -> Dict[str, Any]:
        """
        Merge a pull request after validation.
        
        Args:
            pr_number: Pull request number
            commit_title: Optional commit title
            commit_message: Optional commit message
            merge_method: Merge method ('merge', 'squash', 'rebase')
            
        Returns:
            Merge result dictionary
        """
        pr = self.repo.get_pull(pr_number)
        
        # Validate PR is mergeable
        if pr.state != 'open':
            raise ValueError(f"Pull request #{pr_number} is not open (state: {pr.state})")
        
        if pr.merged:
            raise ValueError(f"Pull request #{pr_number} is already merged")
        
        if pr.mergeable is False:
            raise ValueError(f"Pull request #{pr_number} has merge conflicts")
        
        # Merge the PR
        result = pr.merge(
            commit_title=commit_title,
            commit_message=commit_message,
            merge_method=merge_method
        )
        
        return {
            'merged': result.merged,
            'message': result.message,
            'sha': result.sha if result.merged else None,
            'pr_number': pr_number
        }
    
    def get_pending_reviews(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get pending reviews for a pull request.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            List of review dictionaries
        """
        pr = self.repo.get_pull(pr_number)
        reviews = pr.get_reviews()
        
        result = []
        for review in reviews:
            result.append({
                'id': review.id,
                'user': review.user.login if review.user else None,
                'state': review.state,
                'body': review.body,
                'submitted_at': review.submitted_at.isoformat() if review.submitted_at else None
            })
        
        return result
    
    def approve_pull_request(self, pr_number: int, body: Optional[str] = None) -> Dict[str, Any]:
        """
        Approve a pull request.
        
        Args:
            pr_number: Pull request number
            body: Optional review comment
            
        Returns:
            Review dictionary
        """
        pr = self.repo.get_pull(pr_number)
        review = pr.create_review(body=body or "Approved", event='APPROVE')
        
        return {
            'id': review.id,
            'state': review.state,
            'body': review.body
        }
