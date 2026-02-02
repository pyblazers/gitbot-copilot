"""
Unit tests for GitBot main class
"""

import unittest
from unittest.mock import Mock, patch
import os


class TestGitBot(unittest.TestCase):
    """Test GitBot main class"""

    @patch.dict(os.environ, {
        "GITHUB_TOKEN": "test_token",
        "GITHUB_OWNER": "test_owner",
        "GITHUB_REPO": "test_repo"
    })
    @patch("gitbot.gitbot.Github")
    def test_gitbot_initialization(self, mock_github):
        """Test GitBot initialization with environment variables"""
        from gitbot import GitBot
        
        mock_github_instance = Mock()
        mock_github.return_value = mock_github_instance
        mock_repo = Mock()
        mock_github_instance.get_repo.return_value = mock_repo
        
        bot = GitBot()
        
        self.assertEqual(bot.github_token, "test_token")
        self.assertEqual(bot.owner, "test_owner")
        self.assertEqual(bot.repo_name, "test_repo")
        mock_github.assert_called_once_with("test_token")

    @patch("gitbot.gitbot.Github")
    def test_gitbot_initialization_with_params(self, mock_github):
        """Test GitBot initialization with parameters"""
        from gitbot import GitBot
        
        mock_github_instance = Mock()
        mock_github.return_value = mock_github_instance
        mock_repo = Mock()
        mock_github_instance.get_repo.return_value = mock_repo
        
        bot = GitBot(
            github_token="param_token",
            owner="param_owner",
            repo_name="param_repo"
        )
        
        self.assertEqual(bot.github_token, "param_token")
        self.assertEqual(bot.owner, "param_owner")
        self.assertEqual(bot.repo_name, "param_repo")

    @patch("gitbot.gitbot.Github")
    def test_gitbot_no_token_raises_error(self, mock_github):
        """Test that GitBot raises error when no token is provided"""
        from gitbot import GitBot
        
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                bot = GitBot()

    @patch("gitbot.gitbot.Github")
    def test_set_repository(self, mock_github):
        """Test setting repository"""
        from gitbot import GitBot
        
        mock_github_instance = Mock()
        mock_github.return_value = mock_github_instance
        mock_repo = Mock()
        mock_github_instance.get_repo.return_value = mock_repo
        
        bot = GitBot(github_token="test_token")
        bot.set_repository("new_owner", "new_repo")
        
        self.assertEqual(bot.owner, "new_owner")
        self.assertEqual(bot.repo_name, "new_repo")
        mock_github_instance.get_repo.assert_called_with("new_owner/new_repo")


if __name__ == "__main__":
    unittest.main()
