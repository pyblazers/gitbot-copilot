"""Example: Using GitBot programmatically."""

import asyncio
from gitbot import GitBot
from gitbot.config.settings import Settings


async def main():
    """Main example function."""
    
    # Initialize GitBot with settings
    settings = Settings()
    gitbot = GitBot(settings)
    
    print("=== GitBot Examples ===\n")
    
    # Example 1: Process a natural language command
    print("1. Processing natural language command...")
    command = "Create an issue for implementing user authentication"
    result = await gitbot.process_command(command)
    print(f"Result: {result}\n")
    
    # Example 2: Generate code
    print("2. Generating code...")
    description = "A Python function that validates email addresses using regex"
    code = await gitbot.generate_code(description, language="python")
    print(f"Generated code:\n{code}\n")
    
    # Example 3: Analyze sentiment
    print("3. Analyzing sentiment...")
    text = "This is an excellent implementation! Great work on the optimization."
    sentiment = await gitbot.analyze_sentiment(text)
    print(f"Sentiment: {sentiment}\n")
    
    # Example 4: Predict completion time
    print("4. Predicting completion time...")
    issue_data = {
        "title": "Add dark mode support",
        "description": "Implement dark mode throughout the application with toggle support",
        "labels": ["enhancement", "ui"],
        "assignees_count": 1,
        "comments_count": 0,
        "days_open": 0
    }
    prediction = await gitbot.predict_completion_time(issue_data)
    print(f"Prediction: {prediction}\n")
    
    # Example 5: Summarize discussion
    print("5. Summarizing discussion...")
    discussion = [
        {
            "author": "developer1",
            "body": "I think we should use React for this component. It provides better state management."
        },
        {
            "author": "developer2",
            "body": "Agreed, but we need to ensure it's compatible with our existing Vue components."
        },
        {
            "author": "developer1",
            "body": "Good point. I'll create a proof of concept to test the integration."
        }
    ]
    summary = await gitbot.summarize_discussion(discussion)
    print(f"Summary: {summary}\n")
    
    print("=== Examples completed ===")


if __name__ == "__main__":
    asyncio.run(main())
