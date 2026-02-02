"""Core GitBot functionality."""

import logging
from typing import Optional

from gitbot.config.settings import Settings
from gitbot.ai.nlp_processor import NLPProcessor
from gitbot.ai.code_generator import CodeGenerator
from gitbot.ai.workflow_manager import WorkflowManager
from gitbot.ai.sentiment_analyzer import SentimentAnalyzer
from gitbot.ai.predictive_tasks import PredictiveTasksModel
from gitbot.ai.analytics import AnalyticsEngine
from gitbot.ai.llm_manager import LLMManager

logger = logging.getLogger(__name__)


class GitBot:
    """Main GitBot class orchestrating all AI components."""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize GitBot with all AI components.
        
        Args:
            settings: Configuration settings. If None, loads from environment.
        """
        self.settings = settings or Settings()
        self._initialize_components()
        logger.info("GitBot initialized successfully")

    def _initialize_components(self):
        """Initialize all AI components based on settings."""
        self.llm_manager = LLMManager(self.settings)
        
        if self.settings.enable_nlp:
            self.nlp_processor = NLPProcessor(self.settings, self.llm_manager)
            logger.info("NLP Processor initialized")
        
        if self.settings.enable_code_generation:
            self.code_generator = CodeGenerator(self.settings, self.llm_manager)
            logger.info("Code Generator initialized")
        
        self.workflow_manager = WorkflowManager(self.settings)
        logger.info("Workflow Manager initialized")
        
        if self.settings.enable_sentiment_analysis:
            self.sentiment_analyzer = SentimentAnalyzer(self.settings)
            logger.info("Sentiment Analyzer initialized")
        
        if self.settings.enable_predictive_tasks:
            self.predictive_model = PredictiveTasksModel(self.settings)
            logger.info("Predictive Tasks Model initialized")
        
        if self.settings.enable_analytics:
            self.analytics_engine = AnalyticsEngine(self.settings)
            logger.info("Analytics Engine initialized")

    async def process_command(self, command: str, context: dict = None) -> dict:
        """Process a natural language command.
        
        Args:
            command: Natural language command to process
            context: Additional context information
            
        Returns:
            dict: Processing results
        """
        if not hasattr(self, 'nlp_processor'):
            return {"error": "NLP processor not enabled"}
        
        return await self.nlp_processor.parse_command(command, context)

    async def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code based on description.
        
        Args:
            description: Description of what the code should do
            language: Programming language
            
        Returns:
            str: Generated code
        """
        if not hasattr(self, 'code_generator'):
            return "# Code generation not enabled"
        
        return await self.code_generator.generate(description, language)

    async def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict: Sentiment analysis results
        """
        if not hasattr(self, 'sentiment_analyzer'):
            return {"error": "Sentiment analysis not enabled"}
        
        return await self.sentiment_analyzer.analyze(text)

    async def predict_completion_time(self, issue_data: dict) -> dict:
        """Predict completion time for an issue.
        
        Args:
            issue_data: Issue data including description, labels, etc.
            
        Returns:
            dict: Prediction results
        """
        if not hasattr(self, 'predictive_model'):
            return {"error": "Predictive tasks not enabled"}
        
        return await self.predictive_model.predict_completion(issue_data)

    async def summarize_discussion(self, discussion: list) -> str:
        """Summarize a discussion thread.
        
        Args:
            discussion: List of discussion comments
            
        Returns:
            str: Summary of the discussion
        """
        if not hasattr(self, 'analytics_engine'):
            return "Analytics not enabled"
        
        return await self.analytics_engine.summarize(discussion)
