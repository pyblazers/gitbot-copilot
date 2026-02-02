"""Tests for AI modules."""

import pytest
from gitbot.config.settings import Settings
from gitbot.ai.llm_manager import LLMManager


class TestLLMManager:
    """Test LLM Manager."""

    def test_initialization(self):
        """Test LLM manager initialization."""
        settings = Settings()
        llm_manager = LLMManager(settings)
        
        assert llm_manager is not None
        assert llm_manager.settings == settings

    def test_initialization_without_api_key(self):
        """Test initialization without API key."""
        settings = Settings()
        settings.openai_api_key = ""
        llm_manager = LLMManager(settings)
        
        # Should initialize but without client
        assert llm_manager.openai_client is None

    @pytest.mark.asyncio
    async def test_generate_completion_without_llm(self):
        """Test completion generation without LLM."""
        settings = Settings()
        settings.openai_api_key = ""
        settings.use_local_llm = False
        llm_manager = LLMManager(settings)
        
        result = await llm_manager.generate_completion("test prompt")
        assert "Error" in result or "No language model available" in result
