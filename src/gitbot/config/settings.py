"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application configuration settings."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_codex_model: str = os.getenv("OPENAI_CODEX_MODEL", "gpt-4")

    # GitHub Configuration
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")

    # Hugging Face Configuration
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")

    # Server Configuration
    flask_host: str = os.getenv("FLASK_HOST", "0.0.0.0")
    flask_port: int = int(os.getenv("FLASK_PORT", "5000"))
    flask_debug: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Local LLM Configuration
    use_local_llm: bool = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"
    local_llm_model_path: str = os.getenv("LOCAL_LLM_MODEL_PATH", "")
    local_llm_type: str = os.getenv("LOCAL_LLM_TYPE", "llama")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "gitbot.log")

    # Features Toggle
    enable_nlp: bool = os.getenv("ENABLE_NLP", "True").lower() == "true"
    enable_code_generation: bool = os.getenv("ENABLE_CODE_GENERATION", "True").lower() == "true"
    enable_sentiment_analysis: bool = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "True").lower() == "true"
    enable_predictive_tasks: bool = os.getenv("ENABLE_PREDICTIVE_TASKS", "True").lower() == "true"
    enable_analytics: bool = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"

    def validate(self) -> bool:
        """Validate required settings.
        
        Returns:
            bool: True if all required settings are present
        """
        required_settings = []
        
        if self.enable_nlp or self.enable_code_generation:
            if not self.use_local_llm and not self.openai_api_key:
                required_settings.append("OPENAI_API_KEY")
        
        if required_settings:
            raise ValueError(f"Missing required settings: {', '.join(required_settings)}")
        
        return True
