# GitBot Copilot 🤖

AI-enhanced GitHub automation bot with advanced capabilities for natural language processing, code generation, workflow management, sentiment analysis, predictive analytics, and more.

## 🌟 Features

### 1. **Natural Language Processing (NLP)**
- Parse and understand user commands using OpenAI GPT-4
- Auto-generate detailed issue descriptions
- Summarize pull request discussions
- Extract action items from conversations

### 2. **Code Generation**
- Generate code snippets using OpenAI Codex
- Complete partial code intelligently
- Format and improve code structure
- Generate unit tests automatically
- Explain complex code

### 3. **Workflow Management**
- Handle complex workflows using LangChain
- Automate task assignments based on context
- Link multiple queries seamlessly
- Dynamic routing of PRs and issues

### 4. **Sentiment Analysis**
- Analyze tone of PR and issue discussions using Hugging Face
- Detect negative sentiments requiring attention
- Monitor overall discussion health
- Identify aggressive or critical tones

### 5. **Predictive Tasks**
- Predict task completion times using ML models
- Identify potential delays and risk factors
- Detect bottlenecks in repository management
- Provide actionable recommendations

### 6. **Analytics and Summarization**
- Quick analytics and reporting using Hugging Face models
- Summarize lengthy discussions
- Extract key points from documentation
- Analyze trends over time

### 7. **Open-Source LLM Support**
- Support for LLaMA models for local processing
- GPT-J integration for privacy-focused tasks
- Configurable model selection

### 8. **Webhook Listener**
- Real-time GitHub event processing
- AI-driven insights and routing
- Automatic issue triage
- Dynamic PR assignment based on context

## 📋 Requirements

- Python 3.8 or higher
- macOS (optimized for Mac Mini deployment)
- Git
- OpenAI API key (for GPT-4 and Codex)
- Optional: Local LLM models for offline processing

## 🚀 Installation (macOS)

### Step 1: Install Homebrew

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
brew install python@3.11
```

Verify installation:

```bash
python3 --version
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -e .
```

For development:

```bash
pip install -r requirements-dev.txt
```

### Step 6: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

# Optional
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### Step 7: Verify Installation

```bash
gitbot --help
```

## 🎯 Usage

### Start Webhook Server

```bash
gitbot server --host 0.0.0.0 --port 5000
```

### Process Commands

```bash
gitbot process "Create an issue for fixing the login bug"
```

### Generate Code

```bash
gitbot generate "A Python function to calculate Fibonacci numbers" --language python
```

### Analyze Sentiment

```bash
gitbot analyze "This PR looks great! Well done on the implementation."
```

### Predict Completion Time

```bash
gitbot predict --title "Implement user authentication" --labels enhancement security
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes (unless using local LLM) |
| `OPENAI_MODEL` | OpenAI model to use | gpt-4 | No |
| `GITHUB_TOKEN` | GitHub personal access token | - | Yes |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook verification | - | Recommended |
| `HUGGINGFACE_API_KEY` | Hugging Face API key | - | No |
| `USE_LOCAL_LLM` | Use local LLM instead of OpenAI | False | No |
| `LOCAL_LLM_MODEL_PATH` | Path to local LLM model | - | If USE_LOCAL_LLM=True |
| `LOCAL_LLM_TYPE` | Type of local LLM (llama/gptj) | llama | No |
| `ENABLE_NLP` | Enable NLP features | True | No |
| `ENABLE_CODE_GENERATION` | Enable code generation | True | No |
| `ENABLE_SENTIMENT_ANALYSIS` | Enable sentiment analysis | True | No |
| `ENABLE_PREDICTIVE_TASKS` | Enable predictive tasks | True | No |
| `ENABLE_ANALYTICS` | Enable analytics | True | No |

### Using Local LLMs

#### LLaMA Setup

1. Install llama-cpp-python:
   ```bash
   pip install llama-cpp-python
   ```

2. Download a LLaMA model (e.g., from Hugging Face)

3. Configure in `.env`:
   ```bash
   USE_LOCAL_LLM=True
   LOCAL_LLM_MODEL_PATH=/path/to/llama-model.gguf
   LOCAL_LLM_TYPE=llama
   ```

#### GPT-J Setup

1. Install gpt4all:
   ```bash
   pip install gpt4all
   ```

2. Download GPT-J model

3. Configure in `.env`:
   ```bash
   USE_LOCAL_LLM=True
   LOCAL_LLM_MODEL_PATH=/path/to/gptj-model.bin
   LOCAL_LLM_TYPE=gptj
   ```

## 🔌 GitHub Webhook Setup

### 1. Configure GitHub Webhook

1. Go to your repository settings
2. Navigate to "Webhooks" → "Add webhook"
3. Set Payload URL: `http://your-server:5000/webhook`
4. Set Content type: `application/json`
5. Set Secret: (use the value from `GITHUB_WEBHOOK_SECRET`)
6. Select events to trigger the webhook

### 2. Expose Local Server (for testing)

Using ngrok:

```bash
brew install ngrok
ngrok http 5000
```

Use the ngrok URL as your webhook payload URL.

## 📊 Architecture

```
gitbot-copilot/
├── src/
│   └── gitbot/
│       ├── __init__.py
│       ├── core.py              # Main GitBot orchestrator
│       ├── cli.py               # Command-line interface
│       ├── config/              # Configuration
│       │   └── settings.py
│       ├── ai/                  # AI modules
│       │   ├── llm_manager.py   # LLM management
│       │   ├── nlp_processor.py # NLP features
│       │   ├── code_generator.py # Code generation
│       │   ├── workflow_manager.py # Workflow automation
│       │   ├── sentiment_analyzer.py # Sentiment analysis
│       │   ├── predictive_tasks.py # Predictive models
│       │   └── analytics.py     # Analytics engine
│       ├── webhook/             # Webhook handling
│       │   └── listener.py
│       └── utils/               # Utilities
│           └── logging.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🧪 Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=gitbot --cov-report=html
```

## 🔐 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Webhook Secret**: Always use webhook secrets in production
3. **Local LLMs**: For sensitive data, consider using local LLMs
4. **Network**: Run behind a firewall or reverse proxy
5. **Authentication**: Implement additional authentication for production

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/pyblazers/gitbot-copilot/issues)
- **Documentation**: See `/docs` directory
- **Examples**: See `/examples` directory

## 🗺️ Roadmap

- [ ] Add support for more LLM providers
- [ ] Implement caching for faster responses
- [ ] Add multi-repository support
- [ ] Create web dashboard for monitoring
- [ ] Add more advanced analytics features
- [ ] Support for custom workflow templates
- [ ] Integration with more CI/CD platforms

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Codex
- Hugging Face for transformers and models
- LangChain for workflow orchestration
- The open-source community for various libraries

---

Built with ❤️ for the developer community