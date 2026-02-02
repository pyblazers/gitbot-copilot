"""Tests for configuration settings."""

import os
import pytest
from gitbot.config.settings import Settings


class TestSettings:
    """Test Settings class."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        
        # Check defaults
        assert settings.openai_model == "gpt-4"
        assert settings.flask_port == 5000
        assert settings.flask_host == "0.0.0.0"
        assert settings.log_level == "INFO"
        assert settings.use_local_llm is False

    def test_feature_toggles_default(self):
        """Test default feature toggle values."""
        settings = Settings()
        
        assert settings.enable_nlp is True
        assert settings.enable_code_generation is True
        assert settings.enable_sentiment_analysis is True
        assert settings.enable_predictive_tasks is True
        assert settings.enable_analytics is True

    def test_validation_without_api_key(self):
        """Test validation when API key is missing."""
        settings = Settings()
        settings.openai_api_key = ""
        settings.use_local_llm = False
        
        with pytest.raises(ValueError) as exc_info:
            settings.validate()
        
        assert "OPENAI_API_KEY" in str(exc_info.value)

    def test_validation_with_local_llm(self):
        """Test validation when using local LLM."""
        settings = Settings()
        settings.openai_api_key = ""
        settings.use_local_llm = True
        
        # Should not raise error
        assert settings.validate() is True
