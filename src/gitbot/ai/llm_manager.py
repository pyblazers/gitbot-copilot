"""LLM Manager for handling multiple language models."""

import logging
from typing import Optional, Union

from gitbot.config.settings import Settings

logger = logging.getLogger(__name__)


class LLMManager:
    """Manager for handling OpenAI and local LLM models."""

    def __init__(self, settings: Settings):
        """Initialize LLM Manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.openai_client = None
        self.local_llm = None
        
        self._initialize_models()

    def _initialize_models(self):
        """Initialize language models based on settings."""
        if not self.settings.use_local_llm and self.settings.openai_api_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.settings.openai_api_key)
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("OpenAI package not installed")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        if self.settings.use_local_llm:
            self._initialize_local_llm()

    def _initialize_local_llm(self):
        """Initialize local LLM (LLaMA or GPT-J)."""
        try:
            if self.settings.local_llm_type == "llama":
                try:
                    from llama_cpp import Llama
                    self.local_llm = Llama(
                        model_path=self.settings.local_llm_model_path,
                        n_ctx=2048,
                        n_threads=4
                    )
                    logger.info("LLaMA model initialized")
                except ImportError:
                    logger.warning("llama-cpp-python not installed. Install with: pip install llama-cpp-python")
            elif self.settings.local_llm_type == "gptj":
                try:
                    from gpt4all import GPT4All
                    self.local_llm = GPT4All(self.settings.local_llm_model_path)
                    logger.info("GPT-J model initialized")
                except ImportError:
                    logger.warning("gpt4all not installed. Install with: pip install gpt4all")
        except Exception as e:
            logger.error(f"Failed to initialize local LLM: {e}")

    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> str:
        """Generate completion using available LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_message: Optional system message
            
        Returns:
            str: Generated completion
        """
        if self.openai_client:
            return await self._openai_completion(prompt, max_tokens, temperature, system_message)
        elif self.local_llm:
            return await self._local_completion(prompt, max_tokens, temperature)
        else:
            logger.error("No LLM available")
            return "Error: No language model available"

    async def _openai_completion(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        system_message: Optional[str]
    ) -> str:
        """Generate completion using OpenAI."""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI completion failed: {e}")
            return f"Error: {str(e)}"

    async def _local_completion(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate completion using local LLM."""
        try:
            if self.settings.local_llm_type == "llama":
                output = self.local_llm(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    echo=False
                )
                return output['choices'][0]['text']
            elif self.settings.local_llm_type == "gptj":
                return self.local_llm.generate(
                    prompt,
                    max_tokens=max_tokens,
                    temp=temperature
                )
        except Exception as e:
            logger.error(f"Local LLM completion failed: {e}")
            return f"Error: {str(e)}"
