"""GitHub webhook listener with AI-driven insights."""

import logging
import hmac
import hashlib
from typing import Dict, Optional

from flask import Flask, request, jsonify

from gitbot.config.settings import Settings
from gitbot.core import GitBot

logger = logging.getLogger(__name__)


class WebhookListener:
    """Webhook listener for GitHub events with AI-driven processing."""

    def __init__(self, settings: Settings, gitbot: GitBot):
        """Initialize Webhook Listener.
        
        Args:
            settings: Application settings
            gitbot: GitBot instance for AI processing
        """
        self.settings = settings
        self.gitbot = gitbot
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes for webhook handling."""
        
        @self.app.route("/webhook", methods=["POST"])
        async def handle_webhook():
            """Handle incoming GitHub webhook."""
            # Verify signature
            if not self._verify_signature(request):
                logger.warning("Invalid webhook signature")
                return jsonify({"error": "Invalid signature"}), 403
            
            # Get event type
            event_type = request.headers.get("X-GitHub-Event")
            payload = request.json
            
            logger.info(f"Received webhook event: {event_type}")
            
            # Process event with AI
            result = await self._process_event(event_type, payload)
            
            return jsonify(result), 200
        
        @self.app.route("/health", methods=["GET"])
        def health_check():
            """Health check endpoint."""
            return jsonify({"status": "healthy"}), 200

    def _verify_signature(self, req) -> bool:
        """Verify webhook signature.
        
        Args:
            req: Flask request object
            
        Returns:
            bool: True if signature is valid
        """
        if not self.settings.github_webhook_secret:
            logger.warning("No webhook secret configured, skipping verification")
            return True
        
        signature = req.headers.get("X-Hub-Signature-256")
        if not signature:
            return False
        
        # Calculate expected signature
        mac = hmac.new(
            self.settings.github_webhook_secret.encode(),
            msg=req.data,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + mac.hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)

    async def _process_event(self, event_type: str, payload: Dict) -> Dict:
        """Process GitHub webhook event with AI.
        
        Args:
            event_type: Type of GitHub event
            payload: Event payload
            
        Returns:
            dict: Processing result
        """
        try:
            if event_type == "issues":
                return await self._handle_issue_event(payload)
            elif event_type == "pull_request":
                return await self._handle_pr_event(payload)
            elif event_type == "issue_comment":
                return await self._handle_comment_event(payload)
            elif event_type == "push":
                return await self._handle_push_event(payload)
            else:
                logger.info(f"Unhandled event type: {event_type}")
                return {"status": "ignored", "event_type": event_type}
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return {"status": "error", "message": str(e)}

    async def _handle_issue_event(self, payload: Dict) -> Dict:
        """Handle issue events with AI-driven insights.
        
        Args:
            payload: Issue event payload
            
        Returns:
            dict: Processing result
        """
        action = payload.get("action")
        issue = payload.get("issue", {})
        
        logger.info(f"Processing issue event: {action}")
        
        if action == "opened":
            # Auto-generate description if needed
            if len(issue.get("body", "")) < 50:
                title = issue.get("title", "")
                description = await self.gitbot.nlp_processor.generate_issue_description(title)
                logger.info(f"Generated description for issue: {title}")
            
            # Analyze sentiment
            sentiment = await self.gitbot.analyze_sentiment(issue.get("body", ""))
            
            # Predict completion time
            issue_data = {
                "title": issue.get("title", ""),
                "description": issue.get("body", ""),
                "labels": [label.get("name") for label in issue.get("labels", [])],
                "assignees_count": len(issue.get("assignees", []))
            }
            prediction = await self.gitbot.predict_completion_time(issue_data)
            
            return {
                "status": "processed",
                "action": "issue_opened",
                "sentiment": sentiment,
                "prediction": prediction
            }
        
        return {"status": "processed", "action": action}

    async def _handle_pr_event(self, payload: Dict) -> Dict:
        """Handle pull request events with AI routing.
        
        Args:
            payload: PR event payload
            
        Returns:
            dict: Processing result
        """
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        
        logger.info(f"Processing PR event: {action}")
        
        if action == "opened":
            # Analyze PR description sentiment
            sentiment = await self.gitbot.analyze_sentiment(pr.get("body", ""))
            
            # Determine routing based on files changed and context
            # This would integrate with workflow manager for dynamic assignment
            files_changed = pr.get("changed_files", 0)
            
            route_context = {
                "files_changed": files_changed,
                "title": pr.get("title", ""),
                "labels": [label.get("name") for label in pr.get("labels", [])]
            }
            
            logger.info(f"PR routing context: {route_context}")
            
            return {
                "status": "processed",
                "action": "pr_opened",
                "sentiment": sentiment,
                "routing": route_context
            }
        
        return {"status": "processed", "action": action}

    async def _handle_comment_event(self, payload: Dict) -> Dict:
        """Handle comment events with sentiment analysis.
        
        Args:
            payload: Comment event payload
            
        Returns:
            dict: Processing result
        """
        action = payload.get("action")
        comment = payload.get("comment", {})
        
        logger.info(f"Processing comment event: {action}")
        
        if action == "created":
            # Analyze comment sentiment and tone
            text = comment.get("body", "")
            sentiment = await self.gitbot.analyze_sentiment(text)
            
            # Check if response is needed (e.g., negative sentiment)
            needs_attention = sentiment.get("sentiment") == "NEGATIVE"
            
            return {
                "status": "processed",
                "action": "comment_created",
                "sentiment": sentiment,
                "needs_attention": needs_attention
            }
        
        return {"status": "processed", "action": action}

    async def _handle_push_event(self, payload: Dict) -> Dict:
        """Handle push events.
        
        Args:
            payload: Push event payload
            
        Returns:
            dict: Processing result
        """
        commits = payload.get("commits", [])
        logger.info(f"Processing push event with {len(commits)} commits")
        
        # Could analyze commit messages, detect patterns, etc.
        return {
            "status": "processed",
            "action": "push",
            "commits_count": len(commits)
        }

    def run(self, host: Optional[str] = None, port: Optional[int] = None):
        """Run the webhook server.
        
        Args:
            host: Server host
            port: Server port
        """
        host = host or self.settings.flask_host
        port = port or self.settings.flask_port
        
        logger.info(f"Starting webhook server on {host}:{port}")
        self.app.run(host=host, port=port, debug=self.settings.flask_debug)
