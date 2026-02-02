"""Tests for GitBot core functionality."""

import pytest
from gitbot.config.settings import Settings
from gitbot.core import GitBot


@pytest.fixture
def settings():
    """Create test settings."""
    return Settings()


@pytest.fixture
def gitbot(settings):
    """Create GitBot instance."""
    return GitBot(settings)


class TestGitBot:
    """Test GitBot core functionality."""

    def test_initialization(self, gitbot):
        """Test GitBot initialization."""
        assert gitbot is not None
        assert gitbot.settings is not None
        assert hasattr(gitbot, 'llm_manager')

    def test_settings_validation(self, settings):
        """Test settings validation."""
        # This should not raise an error even without API keys in test
        assert settings is not None
        assert hasattr(settings, 'openai_api_key')
        assert hasattr(settings, 'github_token')

    @pytest.mark.asyncio
    async def test_process_command_without_nlp(self):
        """Test command processing when NLP is disabled."""
        settings = Settings()
        settings.enable_nlp = False
        gitbot = GitBot(settings)
        
        result = await gitbot.process_command("test command")
        assert "error" in result
        assert result["error"] == "NLP processor not enabled"

    @pytest.mark.asyncio
    async def test_generate_code_without_code_gen(self):
        """Test code generation when disabled."""
        settings = Settings()
        settings.enable_code_generation = False
        gitbot = GitBot(settings)
        
        code = await gitbot.generate_code("test description")
        assert code == "# Code generation not enabled"

    @pytest.mark.asyncio
    async def test_analyze_sentiment_without_sentiment(self):
        """Test sentiment analysis when disabled."""
        settings = Settings()
        settings.enable_sentiment_analysis = False
        gitbot = GitBot(settings)
        
        result = await gitbot.analyze_sentiment("test text")
        assert "error" in result
        assert result["error"] == "Sentiment analysis not enabled"

    @pytest.mark.asyncio
    async def test_predict_completion_without_predictive(self):
        """Test prediction when disabled."""
        settings = Settings()
        settings.enable_predictive_tasks = False
        gitbot = GitBot(settings)
        
        result = await gitbot.predict_completion_time({})
        assert "error" in result
        assert result["error"] == "Predictive tasks not enabled"

    @pytest.mark.asyncio
    async def test_summarize_discussion_without_analytics(self):
        """Test summarization when analytics disabled."""
        settings = Settings()
        settings.enable_analytics = False
        gitbot = GitBot(settings)
        
        result = await gitbot.summarize_discussion([])
        assert result == "Analytics not enabled"
