"""Webhook listener module for GitBot."""

import hmac
import hashlib
from typing import Dict, Any, Optional, Callable
from flask import Flask, request, jsonify

from .config import Config


class WebhookListener:
    """Handles GitHub webhook events."""
    
    def __init__(self, config: Config):
        """
        Initialize webhook listener.
        
        Args:
            config: GitBot configuration
        """
        self.config = config
        self.app = Flask(__name__)
        self.handlers: Dict[str, Callable] = {}
        
        # Register webhook endpoint
        self.app.route('/webhook', methods=['POST'])(self._handle_webhook)
    
    def _verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify GitHub webhook signature.
        
        Args:
            payload: Request payload
            signature: X-Hub-Signature-256 header value
            
        Returns:
            True if signature is valid
        """
        if not self.config.webhook_secret:
            # If no secret is configured, skip verification (not recommended for production)
            return True
        
        if not signature:
            return False
        
        # GitHub sends signature as "sha256=<hash>"
        if not signature.startswith('sha256='):
            return False
        
        expected_signature = signature.split('=')[1]
        
        # Compute HMAC
        mac = hmac.new(
            self.config.webhook_secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256
        )
        
        return hmac.compare_digest(mac.hexdigest(), expected_signature)
    
    def _handle_webhook(self):
        """Handle incoming webhook request."""
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not self._verify_signature(request.data, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Get event type
        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        
        # Parse payload
        payload = request.json
        
        # Call registered handler if exists
        if event_type in self.handlers:
            try:
                result = self.handlers[event_type](payload)
                return jsonify({'status': 'success', 'result': result}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # Default response
        return jsonify({
            'status': 'received',
            'event': event_type,
            'message': f'No handler registered for {event_type}'
        }), 200
    
    def register_handler(self, event_type: str, handler: Callable):
        """
        Register a handler for a specific event type.
        
        Args:
            event_type: GitHub event type (e.g., 'issues', 'pull_request')
            handler: Callable that takes payload dict and returns result
        """
        self.handlers[event_type] = handler
    
    def start(self):
        """Start the webhook listener server."""
        self.app.run(
            host=self.config.webhook_host,
            port=self.config.webhook_port,
            debug=False
        )
