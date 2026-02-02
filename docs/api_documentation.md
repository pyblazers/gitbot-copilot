# API Documentation

## Core Classes

### GitBot

Main orchestrator class that manages all AI components.

```python
from gitbot import GitBot
from gitbot.config.settings import Settings

# Initialize
settings = Settings()
gitbot = GitBot(settings)
```

#### Methods

##### `process_command(command: str, context: dict = None) -> dict`

Process natural language commands.

**Parameters:**
- `command` (str): Natural language command to process
- `context` (dict, optional): Additional context information

**Returns:**
- dict: Processing results with intent and parameters

**Example:**
```python
result = await gitbot.process_command("Create an issue for bug fix")
```

##### `generate_code(description: str, language: str = "python") -> str`

Generate code based on description.

**Parameters:**
- `description` (str): What the code should do
- `language` (str): Programming language (default: "python")

**Returns:**
- str: Generated code

**Example:**
```python
code = await gitbot.generate_code(
    "A function to validate email",
    language="python"
)
```

##### `analyze_sentiment(text: str) -> dict`

Analyze sentiment of text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- dict: Sentiment analysis results

**Example:**
```python
sentiment = await gitbot.analyze_sentiment("Great work!")
```

##### `predict_completion_time(issue_data: dict) -> dict`

Predict completion time for an issue.

**Parameters:**
- `issue_data` (dict): Issue information

**Returns:**
- dict: Prediction results

**Example:**
```python
prediction = await gitbot.predict_completion_time({
    "title": "Add feature",
    "labels": ["enhancement"],
    "assignees_count": 1
})
```

##### `summarize_discussion(discussion: list) -> str`

Summarize a discussion thread.

**Parameters:**
- `discussion` (list): List of comment dictionaries

**Returns:**
- str: Summary of the discussion

**Example:**
```python
summary = await gitbot.summarize_discussion([
    {"author": "user1", "body": "Comment 1"},
    {"author": "user2", "body": "Comment 2"}
])
```

## AI Modules

### NLPProcessor

Natural language processing using OpenAI GPT.

```python
from gitbot.ai.nlp_processor import NLPProcessor

nlp = NLPProcessor(settings, llm_manager)
```

#### Methods

- `parse_command(command: str, context: dict = None) -> dict`
- `generate_issue_description(title: str, context: str = None) -> str`
- `summarize_pr_discussion(discussion: list) -> str`
- `extract_action_items(text: str) -> list`

### CodeGenerator

Code generation using OpenAI Codex.

```python
from gitbot.ai.code_generator import CodeGenerator

generator = CodeGenerator(settings, llm_manager)
```

#### Methods

- `generate(description: str, language: str = "python", context: str = None) -> str`
- `complete_code(partial_code: str, language: str = "python") -> str`
- `format_code(code: str, language: str = "python") -> str`
- `explain_code(code: str, language: str = "python") -> str`
- `generate_tests(code: str, language: str = "python") -> str`

### SentimentAnalyzer

Sentiment analysis using Hugging Face.

```python
from gitbot.ai.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer(settings)
```

#### Methods

- `analyze(text: str) -> dict`
- `analyze_discussion(comments: list) -> dict`
- `detect_tone(text: str) -> dict`

### WorkflowManager

Workflow management using LangChain.

```python
from gitbot.ai.workflow_manager import WorkflowManager

workflow = WorkflowManager(settings)
```

#### Methods

- `create_workflow(workflow_name: str, steps: list) -> dict`
- `execute_workflow(workflow_name: str, context: dict = None) -> dict`
- `link_queries(queries: list) -> dict`

### PredictiveTasksModel

Predictive analytics using TensorFlow/PyTorch.

```python
from gitbot.ai.predictive_tasks import PredictiveTasksModel

predictor = PredictiveTasksModel(settings)
```

#### Methods

- `predict_completion(issue_data: dict) -> dict`
- `predict_delay(task_data: dict) -> dict`
- `identify_bottlenecks(repository_data: dict) -> dict`

### AnalyticsEngine

Analytics and summarization using Hugging Face.

```python
from gitbot.ai.analytics import AnalyticsEngine

analytics = AnalyticsEngine(settings)
```

#### Methods

- `summarize(text: str, max_length: int = 150, min_length: int = 50) -> str`
- `summarize_discussion(comments: list) -> str`
- `generate_report(data: dict) -> dict`
- `extract_key_points(text: str) -> list`
- `analyze_trends(time_series_data: list) -> dict`

## Webhook Handling

### WebhookListener

GitHub webhook listener with AI processing.

```python
from gitbot.webhook.listener import WebhookListener

listener = WebhookListener(settings, gitbot)
listener.run()
```

#### Supported Events

- `issues`: Issue created, updated, closed
- `pull_request`: PR opened, updated, merged
- `issue_comment`: Comment created, edited
- `push`: Code pushed to repository

## Configuration

### Settings

Configuration class for all settings.

```python
from gitbot.config.settings import Settings

settings = Settings()
```

#### Attributes

- `openai_api_key`: OpenAI API key
- `openai_model`: Model to use (default: "gpt-4")
- `github_token`: GitHub personal access token
- `github_webhook_secret`: Webhook verification secret
- `huggingface_api_key`: Hugging Face API key
- `use_local_llm`: Use local LLM instead of OpenAI
- `enable_nlp`: Enable NLP features
- `enable_code_generation`: Enable code generation
- `enable_sentiment_analysis`: Enable sentiment analysis
- `enable_predictive_tasks`: Enable predictive tasks
- `enable_analytics`: Enable analytics

## Error Handling

All async methods return error information in their response dictionaries when exceptions occur:

```python
result = await gitbot.process_command("invalid command")
if "error" in result:
    print(f"Error: {result['error']}")
```

## Rate Limiting

Be aware of API rate limits:
- OpenAI: Varies by plan
- GitHub: 5000 requests/hour for authenticated requests
- Hugging Face: Varies by plan

## Best Practices

1. Always use async/await for API calls
2. Handle errors appropriately
3. Use context managers for resources
4. Monitor API usage
5. Implement caching for frequently requested data
6. Use local LLMs for sensitive data
