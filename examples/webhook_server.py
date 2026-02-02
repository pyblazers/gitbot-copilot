"""Example: Webhook event handling."""

from gitbot import GitBot
from gitbot.config.settings import Settings
from gitbot.webhook.listener import WebhookListener


def main():
    """Start webhook server example."""
    
    # Initialize settings
    settings = Settings()
    
    # Initialize GitBot
    gitbot = GitBot(settings)
    
    # Create webhook listener
    listener = WebhookListener(settings, gitbot)
    
    print("Starting webhook server...")
    print(f"Listening on {settings.flask_host}:{settings.flask_port}")
    print("Webhook endpoint: /webhook")
    print("Health check: /health")
    
    # Run the server
    listener.run()


if __name__ == "__main__":
    main()
