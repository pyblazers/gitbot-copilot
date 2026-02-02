"""
Pull Request Management Module
"""


class PRManager:
    """
    Manages GitHub pull request operations
    """

    def __init__(self, github_client, repository=None):
        """
        Initialize PRManager

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

    def list_pull_requests(self, state="open", sort="created", direction="desc"):
        """
        List pull requests in the repository

        Args:
            state (str): PR state (open, closed, all)
            sort (str): Sort by (created, updated, popularity, long-running)
            direction (str): Sort direction (asc, desc)

        Returns:
            list: List of pull requests
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        prs = []
        for pr in self.repo.get_pulls(state=state, sort=sort, direction=direction):
            prs.append({
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "user": pr.user.login,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "mergeable": pr.mergeable,
                "merged": pr.merged,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "url": pr.html_url,
                "labels": [label.name for label in pr.labels],
                "assignees": [assignee.login for assignee in pr.assignees],
            })
        return prs

    def get_pull_request(self, pr_number):
        """
        Get detailed information about a pull request

        Args:
            pr_number (int): Pull request number

        Returns:
            dict: Pull request information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        pr = self.repo.get_pull(pr_number)
        
        return {
            "number": pr.number,
            "title": pr.title,
            "body": pr.body,
            "state": pr.state,
            "user": pr.user.login,
            "head": pr.head.ref,
            "base": pr.base.ref,
            "mergeable": pr.mergeable,
            "merged": pr.merged,
            "mergeable_state": pr.mergeable_state,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
            "url": pr.html_url,
            "commits": pr.commits,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "changed_files": pr.changed_files,
            "labels": [label.name for label in pr.labels],
            "assignees": [assignee.login for assignee in pr.assignees],
        }

    def merge_pull_request(self, pr_number, commit_message=None, merge_method="merge"):
        """
        Merge a pull request after validation

        Args:
            pr_number (int): Pull request number
            commit_message (str): Optional commit message
            merge_method (str): Merge method (merge, squash, rebase)

        Returns:
            dict: Merge result information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        pr = self.repo.get_pull(pr_number)
        
        # Validate PR is mergeable
        if not pr.mergeable:
            return {
                "success": False,
                "message": "Pull request is not mergeable",
                "mergeable_state": pr.mergeable_state,
            }

        if pr.merged:
            return {
                "success": False,
                "message": "Pull request is already merged",
            }

        # Merge the pull request
        try:
            result = pr.merge(
                commit_message=commit_message,
                merge_method=merge_method
            )
            
            return {
                "success": result.merged,
                "message": result.message,
                "sha": result.sha,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to merge: {str(e)}",
            }

    def create_pull_request(self, title, head, base, body=""):
        """
        Create a new pull request

        Args:
            title (str): PR title
            head (str): The name of the branch where your changes are
            base (str): The name of the branch you want to merge into
            body (str): PR description

        Returns:
            dict: Created pull request information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        pr = self.repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )

        return {
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "user": pr.user.login,
            "head": pr.head.ref,
            "base": pr.base.ref,
            "created_at": pr.created_at.isoformat(),
            "url": pr.html_url,
        }

    def add_review_comment(self, pr_number, comment):
        """
        Add a review comment to a pull request

        Args:
            pr_number (int): Pull request number
            comment (str): Comment text

        Returns:
            dict: Comment information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        pr = self.repo.get_pull(pr_number)
        issue = self.repo.get_issue(pr_number)
        comment_obj = issue.create_comment(comment)

        return {
            "id": comment_obj.id,
            "user": comment_obj.user.login,
            "body": comment_obj.body,
            "created_at": comment_obj.created_at.isoformat(),
        }
