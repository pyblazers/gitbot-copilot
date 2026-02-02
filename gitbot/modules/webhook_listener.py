"""
Webhook Listener Module
"""

import hmac
import hashlib
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv


class WebhookListener:
    """
    Handles GitHub webhook events
    """

    def __init__(self, secret=None, port=None):
        """
        Initialize WebhookListener

        Args:
            secret (str): Webhook secret for validation
            port (int): Port to run the Flask server on
        """
        load_dotenv()
        
        self.secret = secret or os.getenv("WEBHOOK_SECRET")
        self.port = port or int(os.getenv("WEBHOOK_PORT", 5000))
        self.app = Flask(__name__)
        self.event_handlers = {}
        
        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """
        Setup Flask routes for webhook handling
        """
        @self.app.route("/", methods=["GET"])
        def index():
            return jsonify({
                "status": "GitBot Webhook Listener is running",
                "version": "1.0.0"
            })

        @self.app.route("/webhook", methods=["POST"])
        def webhook():
            # Verify signature if secret is configured
            if self.secret:
                if not self._verify_signature(request):
                    return jsonify({"error": "Invalid signature"}), 403

            # Get event type
            event_type = request.headers.get("X-GitHub-Event")
            payload = request.json

            # Handle event
            result = self._handle_event(event_type, payload)
            
            return jsonify(result), 200

        @self.app.route("/health", methods=["GET"])
        def health():
            return jsonify({"status": "healthy"}), 200

    def _verify_signature(self, req):
        """
        Verify GitHub webhook signature

        Args:
            req: Flask request object

        Returns:
            bool: True if signature is valid
        """
        signature = req.headers.get("X-Hub-Signature-256")
        if not signature:
            return False

        # Calculate expected signature
        mac = hmac.new(
            self.secret.encode(),
            msg=req.data,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + mac.hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def _handle_event(self, event_type, payload):
        """
        Handle webhook event

        Args:
            event_type (str): Type of GitHub event
            payload (dict): Event payload

        Returns:
            dict: Event handling result
        """
        handler = self.event_handlers.get(event_type)
        
        if handler:
            try:
                return handler(payload)
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "event": event_type
                }
        
        return {
            "status": "unhandled",
            "message": f"No handler registered for event: {event_type}",
            "event": event_type
        }

    def register_handler(self, event_type, handler_func):
        """
        Register a handler function for a specific event type

        Args:
            event_type (str): GitHub event type (push, pull_request, issues, etc.)
            handler_func (callable): Function to handle the event
        """
        self.event_handlers[event_type] = handler_func

    def start(self, debug=False):
        """
        Start the webhook listener server

        Args:
            debug (bool): Run Flask in debug mode
        """
        print(f"Starting GitBot Webhook Listener on port {self.port}")
        print(f"Webhook endpoint: http://localhost:{self.port}/webhook")
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


# Example event handlers
def handle_push_event(payload):
    """
    Example handler for push events

    Args:
        payload (dict): Event payload

    Returns:
        dict: Handler result
    """
    repo_name = payload.get("repository", {}).get("full_name")
    ref = payload.get("ref")
    pusher = payload.get("pusher", {}).get("name")
    
    return {
        "status": "success",
        "message": f"Push event received for {repo_name} on {ref} by {pusher}"
    }


def handle_pull_request_event(payload):
    """
    Example handler for pull request events

    Args:
        payload (dict): Event payload

    Returns:
        dict: Handler result
    """
    action = payload.get("action")
    pr_number = payload.get("pull_request", {}).get("number")
    pr_title = payload.get("pull_request", {}).get("title")
    
    return {
        "status": "success",
        "message": f"Pull request #{pr_number} '{pr_title}' was {action}"
    }


def handle_issues_event(payload):
    """
    Example handler for issues events

    Args:
        payload (dict): Event payload

    Returns:
        dict: Handler result
    """
    action = payload.get("action")
    issue_number = payload.get("issue", {}).get("number")
    issue_title = payload.get("issue", {}).get("title")
    
    return {
        "status": "success",
        "message": f"Issue #{issue_number} '{issue_title}' was {action}"
    }
