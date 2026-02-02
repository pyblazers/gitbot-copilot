"""
Issue Management Module
"""


class IssueManager:
    """
    Manages GitHub issues operations
    """

    def __init__(self, github_client, repository=None):
        """
        Initialize IssueManager

        Args:
            github_client: GitHub client instance
            repository: Repository object
        """
        self.github_client = github_client
        self.repo = repository

    def set_repository(self, repository):
        """
        Set or change the repository

        Args:
            repository: Repository object
        """
        self.repo = repository

    def list_open_issues(self, state="open", labels=None):
        """
        List issues in the repository

        Args:
            state (str): Issue state (open, closed, all)
            labels (list): List of label names to filter by

        Returns:
            list: List of issues
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        issues = []
        for issue in self.repo.get_issues(state=state, labels=labels or []):
            if not issue.pull_request:  # Exclude pull requests
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "user": issue.user.login,
                    "labels": [label.name for label in issue.labels],
                    "assignees": [assignee.login for assignee in issue.assignees],
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "comments": issue.comments,
                    "url": issue.html_url,
                })
        return issues

    def create_issue(self, title, body="", labels=None, assignees=None):
        """
        Create a new issue

        Args:
            title (str): Issue title
            body (str): Issue description
            labels (list): List of label names
            assignees (list): List of usernames to assign

        Returns:
            dict: Created issue information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        issue = self.repo.create_issue(
            title=title,
            body=body,
            labels=labels or [],
            assignees=assignees or []
        )

        return {
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "user": issue.user.login,
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "created_at": issue.created_at.isoformat(),
            "url": issue.html_url,
        }

    def assign_issue(self, issue_number, assignees):
        """
        Assign users to an issue

        Args:
            issue_number (int): Issue number
            assignees (list): List of usernames to assign

        Returns:
            dict: Updated issue information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        issue = self.repo.get_issue(issue_number)
        issue.edit(assignees=assignees)

        return {
            "number": issue.number,
            "title": issue.title,
            "assignees": [assignee.login for assignee in issue.assignees],
        }

    def add_labels(self, issue_number, labels):
        """
        Add labels to an issue

        Args:
            issue_number (int): Issue number
            labels (list): List of label names to add

        Returns:
            dict: Updated issue information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        issue = self.repo.get_issue(issue_number)
        issue.add_to_labels(*labels)

        return {
            "number": issue.number,
            "title": issue.title,
            "labels": [label.name for label in issue.labels],
        }

    def close_issue(self, issue_number, comment=None):
        """
        Close an issue

        Args:
            issue_number (int): Issue number
            comment (str): Optional closing comment

        Returns:
            dict: Updated issue information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        issue = self.repo.get_issue(issue_number)
        
        if comment:
            issue.create_comment(comment)
        
        issue.edit(state="closed")

        return {
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
        }
