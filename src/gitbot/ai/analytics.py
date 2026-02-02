"""Analytics and summarization using Hugging Face models."""

import logging
from typing import Dict, List, Optional

from gitbot.config.settings import Settings

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Analytics Engine for summarization and reporting using Hugging Face."""

    def __init__(self, settings: Settings):
        """Initialize Analytics Engine.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.summarizer = None
        self._initialize_models()

    def _initialize_models(self):
        """Initialize Hugging Face summarization models."""
        try:
            from transformers import pipeline
            
            # Use a pre-trained summarization model
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn"
            )
            logger.info("Summarization model initialized")
        except ImportError:
            logger.warning("Transformers not installed. Install with: pip install transformers")
        except Exception as e:
            logger.error(f"Failed to initialize summarization model: {e}")

    async def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Summarize text.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            str: Summary
        """
        if not self.summarizer:
            return "Summarization not available"
        
        try:
            # Ensure text is not too short
            if len(text.split()) < 50:
                return text
            
            # Truncate if too long (model has max input length)
            max_input_length = 1024
            if len(text) > max_input_length:
                text = text[:max_input_length]
            
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return summary[0]["summary_text"]
        except Exception as e:
            logger.error(f"Failed to summarize text: {e}")
            return f"Error generating summary: {str(e)}"

    async def summarize_discussion(self, comments: List[Dict]) -> str:
        """Summarize a discussion thread.
        
        Args:
            comments: List of comments with 'body' and 'author' fields
            
        Returns:
            str: Discussion summary
        """
        if not self.summarizer:
            return "Summarization not available"
        
        try:
            # Combine all comments into one text
            discussion_text = "\n\n".join([
                f"{comment.get('author', 'Unknown')}: {comment.get('body', '')}"
                for comment in comments
            ])
            
            # Summarize the combined text
            summary = await self.summarize(discussion_text, max_length=200, min_length=50)
            
            return summary
        except Exception as e:
            logger.error(f"Failed to summarize discussion: {e}")
            return f"Error generating discussion summary: {str(e)}"

    async def generate_report(self, data: Dict) -> Dict:
        """Generate analytics report.
        
        Args:
            data: Repository or project data
            
        Returns:
            dict: Analytics report
        """
        try:
            report = {
                "summary": {},
                "metrics": {},
                "insights": []
            }
            
            # Calculate basic metrics
            report["metrics"] = {
                "total_issues": data.get("total_issues", 0),
                "open_issues": data.get("open_issues", 0),
                "closed_issues": data.get("closed_issues", 0),
                "total_prs": data.get("total_prs", 0),
                "open_prs": data.get("open_prs", 0),
                "merged_prs": data.get("merged_prs", 0),
                "avg_close_time_days": data.get("avg_close_time_days", 0)
            }
            
            # Generate insights
            if report["metrics"]["open_issues"] > 50:
                report["insights"].append({
                    "type": "issues",
                    "severity": "high",
                    "message": f"High number of open issues ({report['metrics']['open_issues']})"
                })
            
            if report["metrics"]["open_prs"] > 20:
                report["insights"].append({
                    "type": "pull_requests",
                    "severity": "medium",
                    "message": f"Many open PRs ({report['metrics']['open_prs']}) may indicate review bottleneck"
                })
            
            close_rate = 0
            if report["metrics"]["total_issues"] > 0:
                close_rate = report["metrics"]["closed_issues"] / report["metrics"]["total_issues"]
            
            report["metrics"]["issue_close_rate"] = round(close_rate * 100, 1)
            
            if close_rate < 0.5:
                report["insights"].append({
                    "type": "issues",
                    "severity": "medium",
                    "message": f"Low issue close rate ({report['metrics']['issue_close_rate']}%)"
                })
            
            # Generate summary text
            report["summary"] = {
                "health_status": self._determine_health(report["insights"]),
                "key_metrics": f"Open Issues: {report['metrics']['open_issues']}, Open PRs: {report['metrics']['open_prs']}",
                "action_items": self._generate_action_items(report["insights"])
            }
            
            return report
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {"error": str(e)}

    async def extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text.
        
        Args:
            text: Text to extract key points from
            
        Returns:
            list: List of key points
        """
        try:
            # Use summarization to extract key information
            summary = await self.summarize(text, max_length=200, min_length=30)
            
            # Split into sentences as key points
            import re
            sentences = re.split(r'[.!?]+', summary)
            key_points = [s.strip() for s in sentences if s.strip()]
            
            return key_points
        except Exception as e:
            logger.error(f"Failed to extract key points: {e}")
            return []

    async def analyze_trends(self, time_series_data: List[Dict]) -> Dict:
        """Analyze trends in time series data.
        
        Args:
            time_series_data: List of data points over time
            
        Returns:
            dict: Trend analysis
        """
        try:
            if not time_series_data or len(time_series_data) < 2:
                return {"error": "Insufficient data for trend analysis"}
            
            # Simple trend analysis
            values = [d.get("value", 0) for d in time_series_data]
            
            # Calculate basic statistics
            import statistics
            avg = statistics.mean(values)
            
            # Determine trend direction
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            if second_avg > first_avg * 1.1:
                trend = "increasing"
            elif second_avg < first_avg * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
            
            return {
                "trend": trend,
                "average": round(avg, 2),
                "first_period_avg": round(first_avg, 2),
                "second_period_avg": round(second_avg, 2),
                "change_percent": round(((second_avg - first_avg) / first_avg * 100), 1) if first_avg > 0 else 0
            }
        except Exception as e:
            logger.error(f"Failed to analyze trends: {e}")
            return {"error": str(e)}

    def _determine_health(self, insights: List[Dict]) -> str:
        """Determine overall health status.
        
        Args:
            insights: List of insights
            
        Returns:
            str: Health status
        """
        if not insights:
            return "excellent"
        
        high_severity = sum(1 for i in insights if i.get("severity") == "high")
        
        if high_severity >= 2:
            return "poor"
        elif high_severity == 1:
            return "fair"
        elif len(insights) > 2:
            return "fair"
        else:
            return "good"

    def _generate_action_items(self, insights: List[Dict]) -> List[str]:
        """Generate action items from insights.
        
        Args:
            insights: List of insights
            
        Returns:
            list: Action items
        """
        action_items = []
        
        for insight in insights:
            if insight.get("type") == "issues" and insight.get("severity") == "high":
                action_items.append("Review and triage open issues")
            elif insight.get("type") == "pull_requests":
                action_items.append("Expedite PR reviews to reduce backlog")
            elif "close rate" in insight.get("message", "").lower():
                action_items.append("Investigate and resolve long-standing issues")
        
        if not action_items:
            action_items.append("Continue monitoring repository metrics")
        
        return action_items
