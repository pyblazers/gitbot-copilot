"""
Unit tests for IssueManager
"""

import unittest
from unittest.mock import Mock, patch
from gitbot.modules.issue_manager import IssueManager


class TestIssueManager(unittest.TestCase):
    """Test IssueManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_github_client = Mock()
        self.mock_repo = Mock()
        self.issue_manager = IssueManager(self.mock_github_client, self.mock_repo)

    def test_list_open_issues(self):
        """Test listing open issues"""
        mock_issue = Mock()
        mock_issue.number = 1
        mock_issue.title = "Test Issue"
        mock_issue.state = "open"
        mock_issue.user.login = "testuser"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.comments = 0
        mock_issue.html_url = "https://github.com/test/test/issues/1"
        mock_issue.pull_request = None
        mock_issue.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        mock_issue.updated_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        self.mock_repo.get_issues.return_value = [mock_issue]
        
        issues = self.issue_manager.list_open_issues()
        
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["number"], 1)
        self.assertEqual(issues[0]["title"], "Test Issue")

    def test_create_issue(self):
        """Test creating an issue"""
        mock_issue = Mock()
        mock_issue.number = 2
        mock_issue.title = "New Issue"
        mock_issue.state = "open"
        mock_issue.user.login = "testuser"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.html_url = "https://github.com/test/test/issues/2"
        mock_issue.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        self.mock_repo.create_issue.return_value = mock_issue
        
        result = self.issue_manager.create_issue(
            title="New Issue",
            body="Test body",
            labels=["bug"]
        )
        
        self.assertEqual(result["number"], 2)
        self.assertEqual(result["title"], "New Issue")
        self.mock_repo.create_issue.assert_called_once()

    def test_repository_not_set_error(self):
        """Test error when repository is not set"""
        manager = IssueManager(self.mock_github_client)
        
        with self.assertRaises(ValueError):
            manager.list_open_issues()


if __name__ == "__main__":
    unittest.main()
