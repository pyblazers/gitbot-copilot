"""Natural Language Processing module using OpenAI GPT."""

import logging
from typing import Optional, Dict, List

from gitbot.config.settings import Settings
from gitbot.ai.llm_manager import LLMManager

logger = logging.getLogger(__name__)


class NLPProcessor:
    """NLP Processor for parsing commands and generating descriptions."""

    def __init__(self, settings: Settings, llm_manager: LLMManager):
        """Initialize NLP Processor.
        
        Args:
            settings: Application settings
            llm_manager: LLM manager instance
        """
        self.settings = settings
        self.llm_manager = llm_manager

    async def parse_command(self, command: str, context: Optional[Dict] = None) -> Dict:
        """Parse and understand user command.
        
        Args:
            command: Natural language command
            context: Additional context information
            
        Returns:
            dict: Parsed command with intent and parameters
        """
        system_message = """You are a GitHub bot assistant. Parse user commands and extract:
        1. Intent (e.g., 'create_issue', 'assign_pr', 'summarize_discussion')
        2. Parameters (e.g., title, description, assignee)
        3. Confidence level
        
        Return a JSON object with these fields."""
        
        prompt = f"Parse this command: {command}"
        if context:
            prompt += f"\n\nContext: {context}"
        
        try:
            response = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3,
                system_message=system_message
            )
            
            # Parse response as JSON
            import json
            result = json.loads(response)
            return result
        except Exception as e:
            logger.error(f"Failed to parse command: {e}")
            return {
                "intent": "unknown",
                "parameters": {},
                "confidence": 0.0,
                "error": str(e)
            }

    async def generate_issue_description(
        self, 
        title: str, 
        context: Optional[str] = None
    ) -> str:
        """Generate auto-description for GitHub issue.
        
        Args:
            title: Issue title
            context: Additional context
            
        Returns:
            str: Generated issue description
        """
        system_message = """You are a technical writer helping to create clear, 
        comprehensive GitHub issue descriptions. Generate detailed descriptions 
        that include problem statement, expected behavior, and steps to reproduce."""
        
        prompt = f"Generate a detailed description for this issue: {title}"
        if context:
            prompt += f"\n\nAdditional context: {context}"
        
        try:
            description = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=800,
                temperature=0.7,
                system_message=system_message
            )
            return description
        except Exception as e:
            logger.error(f"Failed to generate issue description: {e}")
            return f"Error generating description: {str(e)}"

    async def summarize_pr_discussion(self, discussion: List[Dict]) -> str:
        """Summarize pull request discussion.
        
        Args:
            discussion: List of discussion comments
            
        Returns:
            str: Summary of the discussion
        """
        system_message = """You are a technical summarizer. Create concise summaries 
        of pull request discussions, highlighting key decisions, concerns, and action items."""
        
        # Format discussion for the prompt
        discussion_text = "\n\n".join([
            f"{comment.get('author', 'Unknown')}: {comment.get('body', '')}"
            for comment in discussion
        ])
        
        prompt = f"Summarize this PR discussion:\n\n{discussion_text}"
        
        try:
            summary = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=600,
                temperature=0.5,
                system_message=system_message
            )
            return summary
        except Exception as e:
            logger.error(f"Failed to summarize discussion: {e}")
            return f"Error generating summary: {str(e)}"

    async def extract_action_items(self, text: str) -> List[str]:
        """Extract action items from text.
        
        Args:
            text: Text to extract action items from
            
        Returns:
            list: List of action items
        """
        system_message = """Extract clear, actionable items from the given text. 
        Return them as a numbered list."""
        
        prompt = f"Extract action items from this text:\n\n{text}"
        
        try:
            response = await self.llm_manager.generate_completion(
                prompt=prompt,
                max_tokens=400,
                temperature=0.3,
                system_message=system_message
            )
            
            # Parse numbered list
            action_items = [
                line.strip() 
                for line in response.split('\n') 
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))
            ]
            return action_items
        except Exception as e:
            logger.error(f"Failed to extract action items: {e}")
            return []
