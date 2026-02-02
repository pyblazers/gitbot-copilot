"""Code generation module using OpenAI Codex."""

import logging
from typing import Optional, Dict

from gitbot.config.settings import Settings
from gitbot.ai.llm_manager import LLMManager

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Code Generator using OpenAI Codex for code generation and completion."""

    def __init__(self, settings: Settings, llm_manager: LLMManager):
        """Initialize Code Generator.
        
        Args:
            settings: Application settings
            llm_manager: LLM manager instance
        """
        self.settings = settings
        self.llm_manager = llm_manager

    async def generate(
        self, 
        description: str, 
        language: str = "python",
        context: Optional[str] = None
    ) -> str:
        """Generate code based on description.
        
        Args:
            description: What the code should do
            language: Programming language
            context: Additional context or existing code
            
        Returns:
            str: Generated code
        """
        system_message = f"""You are an expert {language} programmer. Generate clean, 
        well-documented, and efficient code based on the given description. Include 
        comments explaining the logic."""
        
        prompt = f"Generate {language} code for: {description}"
        if context:
            prompt += f"\n\nExisting code context:\n{context}"
        
        try:
            code = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.2,
                system_message=system_message
            )
            return code
        except Exception as e:
            logger.error(f"Failed to generate code: {e}")
            return f"# Error generating code: {str(e)}"

    async def complete_code(self, partial_code: str, language: str = "python") -> str:
        """Complete partial code snippet.
        
        Args:
            partial_code: Incomplete code
            language: Programming language
            
        Returns:
            str: Completed code
        """
        system_message = f"""You are an expert {language} programmer. Complete the 
        given code snippet naturally and correctly."""
        
        prompt = f"Complete this {language} code:\n\n{partial_code}"
        
        try:
            completion = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.2,
                system_message=system_message
            )
            return completion
        except Exception as e:
            logger.error(f"Failed to complete code: {e}")
            return f"# Error completing code: {str(e)}"

    async def format_code(self, code: str, language: str = "python") -> str:
        """Format and improve code structure.
        
        Args:
            code: Code to format
            language: Programming language
            
        Returns:
            str: Formatted code
        """
        system_message = f"""You are an expert {language} programmer. Format and 
        improve the given code following best practices and style guides."""
        
        prompt = f"Format and improve this {language} code:\n\n{code}"
        
        try:
            formatted = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.1,
                system_message=system_message
            )
            return formatted
        except Exception as e:
            logger.error(f"Failed to format code: {e}")
            return code  # Return original on error

    async def explain_code(self, code: str, language: str = "python") -> str:
        """Generate explanation for code.
        
        Args:
            code: Code to explain
            language: Programming language
            
        Returns:
            str: Code explanation
        """
        system_message = """You are a technical educator. Explain code clearly 
        and concisely, highlighting key concepts and logic."""
        
        prompt = f"Explain this {language} code:\n\n{code}"
        
        try:
            explanation = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=800,
                temperature=0.5,
                system_message=system_message
            )
            return explanation
        except Exception as e:
            logger.error(f"Failed to explain code: {e}")
            return f"Error generating explanation: {str(e)}"

    async def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate unit tests for code.
        
        Args:
            code: Code to test
            language: Programming language
            
        Returns:
            str: Generated test code
        """
        framework_map = {
            "python": "pytest",
            "javascript": "jest",
            "java": "junit",
            "go": "testing package"
        }
        framework = framework_map.get(language, "appropriate testing framework")
        
        system_message = f"""You are an expert in test-driven development. Generate 
        comprehensive unit tests using {framework} for the given code."""
        
        prompt = f"Generate unit tests for this {language} code:\n\n{code}"
        
        try:
            tests = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.3,
                system_message=system_message
            )
            return tests
        except Exception as e:
            logger.error(f"Failed to generate tests: {e}")
            return f"# Error generating tests: {str(e)}"
