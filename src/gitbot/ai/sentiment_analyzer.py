"""Sentiment analysis using Hugging Face models."""

import logging
from typing import Dict, List, Optional

from gitbot.config.settings import Settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment Analyzer for PR and issue discussions using Hugging Face."""

    def __init__(self, settings: Settings):
        """Initialize Sentiment Analyzer.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.pipeline = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize Hugging Face sentiment analysis model."""
        try:
            from transformers import pipeline
            
            # Use a pre-trained sentiment analysis model
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            logger.info("Sentiment analysis model initialized")
        except ImportError:
            logger.warning("Transformers not installed. Install with: pip install transformers")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment model: {e}")

    async def analyze(self, text: str) -> Dict:
        """Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict: Sentiment analysis results with label and score
        """
        if not self.pipeline:
            return {"error": "Sentiment analyzer not initialized"}
        
        try:
            # Truncate text if too long (model has max length)
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            result = self.pipeline(text)[0]
            
            return {
                "sentiment": result["label"],
                "confidence": result["score"],
                "text_length": len(text)
            }
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {"error": str(e)}

    async def analyze_discussion(self, comments: List[Dict]) -> Dict:
        """Analyze sentiment of a discussion thread.
        
        Args:
            comments: List of comment dictionaries with 'body' field
            
        Returns:
            dict: Aggregated sentiment analysis
        """
        if not self.pipeline:
            return {"error": "Sentiment analyzer not initialized"}
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for comment in comments:
            text = comment.get("body", "")
            if not text:
                continue
            
            result = await self.analyze(text)
            if "error" not in result:
                sentiments.append(result)
                
                sentiment = result["sentiment"].upper()
                if sentiment == "POSITIVE":
                    positive_count += 1
                elif sentiment == "NEGATIVE":
                    negative_count += 1
                else:
                    neutral_count += 1
        
        total = len(sentiments)
        if total == 0:
            return {
                "overall_sentiment": "neutral",
                "positive_ratio": 0.0,
                "negative_ratio": 0.0,
                "neutral_ratio": 0.0,
                "total_comments": 0
            }
        
        return {
            "overall_sentiment": self._determine_overall(positive_count, negative_count, neutral_count),
            "positive_ratio": positive_count / total,
            "negative_ratio": negative_count / total,
            "neutral_ratio": neutral_count / total,
            "total_comments": total,
            "sentiments": sentiments
        }

    def _determine_overall(self, positive: int, negative: int, neutral: int) -> str:
        """Determine overall sentiment.
        
        Args:
            positive: Count of positive sentiments
            negative: Count of negative sentiments
            neutral: Count of neutral sentiments
            
        Returns:
            str: Overall sentiment label
        """
        if positive > negative and positive > neutral:
            return "positive"
        elif negative > positive and negative > neutral:
            return "negative"
        else:
            return "neutral"

    async def detect_tone(self, text: str) -> Dict:
        """Detect the tone of text (formal, casual, aggressive, etc.).
        
        Args:
            text: Text to analyze
            
        Returns:
            dict: Tone analysis results
        """
        if not self.pipeline:
            return {"error": "Sentiment analyzer not initialized"}
        
        try:
            # Basic sentiment as foundation
            sentiment_result = await self.analyze(text)
            
            # Additional tone indicators
            tone_indicators = {
                "exclamation_marks": text.count("!"),
                "question_marks": text.count("?"),
                "all_caps_words": sum(1 for word in text.split() if word.isupper() and len(word) > 1),
                "has_thanks": any(word in text.lower() for word in ["thanks", "thank you", "appreciate"]),
                "has_please": "please" in text.lower()
            }
            
            # Determine tone
            tone = "neutral"
            if sentiment_result.get("sentiment") == "NEGATIVE":
                if tone_indicators["all_caps_words"] > 2 or tone_indicators["exclamation_marks"] > 2:
                    tone = "aggressive"
                else:
                    tone = "critical"
            elif sentiment_result.get("sentiment") == "POSITIVE":
                if tone_indicators["has_thanks"]:
                    tone = "appreciative"
                elif tone_indicators["has_please"]:
                    tone = "polite"
                else:
                    tone = "supportive"
            
            return {
                "tone": tone,
                "sentiment": sentiment_result,
                "indicators": tone_indicators
            }
        except Exception as e:
            logger.error(f"Failed to detect tone: {e}")
            return {"error": str(e)}
