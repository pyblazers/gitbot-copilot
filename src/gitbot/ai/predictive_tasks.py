"""Predictive tasks using TensorFlow/PyTorch models."""

import logging
from typing import Dict, List, Optional
import numpy as np

from gitbot.config.settings import Settings

logger = logging.getLogger(__name__)


class PredictiveTasksModel:
    """Predictive model for task delays, completion times, and bottlenecks."""

    def __init__(self, settings: Settings):
        """Initialize Predictive Tasks Model.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize ML model (TensorFlow or PyTorch)."""
        try:
            import torch
            import torch.nn as nn
            
            # Simple neural network for demonstration
            class PredictionNet(nn.Module):
                def __init__(self, input_size=10, hidden_size=20, output_size=1):
                    super(PredictionNet, self).__init__()
                    self.fc1 = nn.Linear(input_size, hidden_size)
                    self.relu = nn.ReLU()
                    self.fc2 = nn.Linear(hidden_size, output_size)
                
                def forward(self, x):
                    x = self.fc1(x)
                    x = self.relu(x)
                    x = self.fc2(x)
                    return x
            
            self.model = PredictionNet()
            logger.info("PyTorch prediction model initialized")
        except ImportError:
            try:
                import tensorflow as tf
                
                # Simple TensorFlow model
                self.model = tf.keras.Sequential([
                    tf.keras.layers.Dense(20, activation='relu', input_shape=(10,)),
                    tf.keras.layers.Dense(1)
                ])
                logger.info("TensorFlow prediction model initialized")
            except ImportError:
                logger.warning("Neither PyTorch nor TensorFlow installed")
        except Exception as e:
            logger.error(f"Failed to initialize prediction model: {e}")

    async def predict_completion(self, issue_data: Dict) -> Dict:
        """Predict completion time for an issue.
        
        Args:
            issue_data: Issue information (title, labels, complexity, etc.)
            
        Returns:
            dict: Prediction results with estimated completion time
        """
        try:
            # Extract features from issue data
            features = self._extract_features(issue_data)
            
            # For demonstration, use heuristics when model is not trained
            base_hours = 8  # Base estimate
            
            # Adjust based on labels
            labels = issue_data.get("labels", [])
            if "bug" in labels:
                base_hours *= 0.8  # Bugs typically faster
            if "enhancement" in labels:
                base_hours *= 1.5  # Enhancements take longer
            if "high-priority" in labels:
                base_hours *= 0.9  # High priority gets more focus
            
            # Adjust based on complexity indicators
            description = issue_data.get("description", "")
            if len(description) > 500:
                base_hours *= 1.2  # Complex issues have longer descriptions
            
            # Add uncertainty range
            min_hours = base_hours * 0.7
            max_hours = base_hours * 1.5
            
            return {
                "estimated_hours": round(base_hours, 1),
                "min_hours": round(min_hours, 1),
                "max_hours": round(max_hours, 1),
                "confidence": 0.75,
                "factors": {
                    "labels": labels,
                    "description_length": len(description)
                }
            }
        except Exception as e:
            logger.error(f"Failed to predict completion time: {e}")
            return {"error": str(e)}

    async def predict_delay(self, task_data: Dict) -> Dict:
        """Predict potential delays for a task.
        
        Args:
            task_data: Task information
            
        Returns:
            dict: Delay prediction with risk factors
        """
        try:
            risk_score = 0.0
            risk_factors = []
            
            # Check for delay indicators
            if task_data.get("assignees_count", 0) == 0:
                risk_score += 0.3
                risk_factors.append("No assignee")
            
            if task_data.get("comments_count", 0) > 10:
                risk_score += 0.2
                risk_factors.append("Many comments (potential blockers)")
            
            if task_data.get("days_open", 0) > 7:
                risk_score += 0.25
                risk_factors.append("Open for > 7 days")
            
            labels = task_data.get("labels", [])
            if "blocked" in labels:
                risk_score += 0.5
                risk_factors.append("Blocked label")
            
            if "needs-review" in labels:
                risk_score += 0.15
                risk_factors.append("Awaiting review")
            
            # Cap at 1.0
            risk_score = min(risk_score, 1.0)
            
            risk_level = "low"
            if risk_score > 0.7:
                risk_level = "high"
            elif risk_score > 0.4:
                risk_level = "medium"
            
            return {
                "delay_risk_score": round(risk_score, 2),
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "recommended_action": self._get_recommendation(risk_level, risk_factors)
            }
        except Exception as e:
            logger.error(f"Failed to predict delay: {e}")
            return {"error": str(e)}

    async def identify_bottlenecks(self, repository_data: Dict) -> Dict:
        """Identify bottlenecks in repository management.
        
        Args:
            repository_data: Repository statistics and metrics
            
        Returns:
            dict: Identified bottlenecks and recommendations
        """
        try:
            bottlenecks = []
            
            # Check PR review bottleneck
            open_prs = repository_data.get("open_prs_count", 0)
            avg_review_time = repository_data.get("avg_review_time_days", 0)
            
            if open_prs > 10 and avg_review_time > 3:
                bottlenecks.append({
                    "type": "pr_review",
                    "severity": "high",
                    "description": f"{open_prs} open PRs with avg review time of {avg_review_time} days",
                    "recommendation": "Add more reviewers or automate some review checks"
                })
            
            # Check issue triage bottleneck
            untriaged_issues = repository_data.get("untriaged_issues_count", 0)
            if untriaged_issues > 20:
                bottlenecks.append({
                    "type": "issue_triage",
                    "severity": "medium",
                    "description": f"{untriaged_issues} untriaged issues",
                    "recommendation": "Implement automated issue labeling and routing"
                })
            
            # Check stale items bottleneck
            stale_items = repository_data.get("stale_items_count", 0)
            if stale_items > 15:
                bottlenecks.append({
                    "type": "stale_items",
                    "severity": "medium",
                    "description": f"{stale_items} stale items (>30 days inactive)",
                    "recommendation": "Close or update stale items to maintain repository health"
                })
            
            return {
                "bottlenecks": bottlenecks,
                "bottleneck_count": len(bottlenecks),
                "overall_health": self._calculate_health(bottlenecks)
            }
        except Exception as e:
            logger.error(f"Failed to identify bottlenecks: {e}")
            return {"error": str(e)}

    def _extract_features(self, data: Dict) -> np.ndarray:
        """Extract numerical features from data.
        
        Args:
            data: Input data dictionary
            
        Returns:
            numpy array of features
        """
        # Simplified feature extraction
        features = [
            len(data.get("labels", [])),
            len(data.get("description", "")),
            data.get("comments_count", 0),
            1 if "bug" in data.get("labels", []) else 0,
            1 if "enhancement" in data.get("labels", []) else 0,
            data.get("assignees_count", 0),
            data.get("milestone_progress", 0),
            data.get("days_open", 0),
            len(data.get("title", "")),
            data.get("linked_issues_count", 0)
        ]
        return np.array(features, dtype=np.float32)

    def _get_recommendation(self, risk_level: str, risk_factors: List[str]) -> str:
        """Get recommendation based on risk level.
        
        Args:
            risk_level: Risk level (low, medium, high)
            risk_factors: List of identified risk factors
            
        Returns:
            str: Recommendation
        """
        if risk_level == "high":
            return "Immediate attention required. Review blockers and reassign if needed."
        elif risk_level == "medium":
            return "Monitor closely. Address identified issues soon."
        else:
            return "Continue normal workflow. No immediate action needed."

    def _calculate_health(self, bottlenecks: List[Dict]) -> str:
        """Calculate overall repository health.
        
        Args:
            bottlenecks: List of identified bottlenecks
            
        Returns:
            str: Health status (excellent, good, fair, poor)
        """
        if not bottlenecks:
            return "excellent"
        
        high_severity = sum(1 for b in bottlenecks if b.get("severity") == "high")
        
        if high_severity >= 2:
            return "poor"
        elif high_severity == 1:
            return "fair"
        elif len(bottlenecks) > 2:
            return "fair"
        else:
            return "good"
