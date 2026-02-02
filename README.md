# GitBot Copilot

An AI-powered GitHub assistant with Xcode-focused infrastructure for macOS, featuring Core ML integration, on-device fine-tuning, and OpenAI connectivity.

## Features

### 🧠 Core ML Integration
- Convert pre-trained models to Core ML format (.mlmodel)
- Natural language understanding for issue analysis
- Issue prioritization using NLP models
- Analytics summarization with Core ML

### 📱 On-Device Fine-Tuning
- Real-time model adaptation with Core ML Update API
- Learn new commands and workflows dynamically
- Privacy-focused on-device training
- No data leaves your device

### 🌐 OpenAI API Connectivity
- Connect to external AI services (GPT-3.5, GPT-4)
- Submit fine-tuning jobs programmatically
- Upload training datasets
- Fetch updated models and responses

### 🎨 SwiftUI Interface
- Intuitive macOS-native interface
- Dashboard with analytics and metrics
- Natural language chat interface
- Fine-tuning task manager
- Settings for API configuration

### 🐍 PythonKit Integration
- Execute Python workflows from Swift
- Advanced model training with Python
- Seamless integration of Python ML libraries
- Model conversion utilities

### 🔧 Modular Architecture
- Protocol-based design for extensibility
- Easy integration of additional AI models
- Plugin-ready workflow system
- Future-proof architecture

## Requirements

- macOS 13.0 or later
- Xcode 15.0 or later
- Swift 5.9 or later
- Python 3.8+ (for PythonKit features)
- Optional: OpenAI API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot
```

### 2. Set Up Python Environment (Optional)

For advanced features using PythonKit:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install coremltools scikit-learn numpy
```

### 3. Build with Swift Package Manager

```bash
cd GitBotXcode
swift build
```

### 4. Run the Application

```bash
swift run GitBotApp
```

Or open the package in Xcode and run directly.

## Quick Start

### Running the SwiftUI App

1. Open `GitBotXcode/Package.swift` in Xcode
2. Select the `GitBotApp` scheme
3. Build and run (⌘R)
4. Configure your settings in the Settings tab

### Basic Usage

#### 1. Configure OpenAI API (Optional)

In the Settings tab:
- Enter your OpenAI API key
- Enable/disable on-device training
- Set model cache path
- Configure Python environment path

#### 2. Chat with GitBot

Navigate to the Chat tab and interact naturally:
```
You: Analyze this issue: "Critical bug in authentication"
GitBot: This appears to be a high-priority security issue...
```

#### 3. Fine-Tune Models

In the Fine-tuning tab:
1. Add training data (input/output pairs)
2. Select model type (Core ML, OpenAI)
3. Click "Start Fine-tuning"
4. Monitor progress in the dashboard

## Architecture

### Module Structure

```
GitBotXcode/
├── Sources/
│   ├── GitBotCore/          # Core functionality and protocols
│   ├── CoreMLModels/        # Core ML integration and NLP
│   ├── OpenAIIntegration/   # OpenAI API client
│   ├── PythonBridge/        # Python interop layer
│   └── SwiftUIApp/          # macOS SwiftUI interface
├── Tests/                   # Unit tests
├── Scripts/                 # Python utility scripts
│   ├── train_model.py
│   ├── convert_to_coreml.py
│   └── preprocess_data.py
└── Resources/
    └── Models/              # ML model storage
```

### Core Components

#### GitBotCore
Central coordinator managing AI models and workflows:
```swift
let gitBot = GitBot()
let result = await gitBot.processCommand("Your command")
```

#### CoreMLModels
Wrapper for Core ML models with fine-tuning support:
```swift
let handler = try NLPTaskHandler(modelURL: modelURL)
let priority = try await handler.analyzeIssue(issueText: text)
```

#### OpenAIIntegration
Client for OpenAI API operations:
```swift
let client = OpenAIClient(apiKey: "your-key")
let response = try await client.createCompletion(prompt: "Hello")
```

#### PythonBridge
Execute Python scripts from Swift:
```swift
let bridge = try PythonBridge()
try await bridge.trainModel(
    scriptPath: "train_model.py",
    trainingData: "data.jsonl",
    modelOutputPath: "model.pkl"
)
```

## Training Custom Models

### 1. Prepare Training Data

Create a JSONL file with training samples:

```json
{"input": "Fix authentication bug", "output": "high"}
{"input": "Update README", "output": "low"}
{"input": "Security vulnerability found", "output": "critical"}
```

### 2. Preprocess Data

```bash
python Scripts/preprocess_data.py training.jsonl processed.jsonl
```

### 3. Train Model

```bash
python Scripts/train_model.py processed.jsonl model.pkl
```

### 4. Convert to Core ML

```bash
python Scripts/convert_to_coreml.py model.pkl model.mlmodel classifier
```

### 5. Use in GitBot

```swift
let modelURL = URL(fileURLWithPath: "model.mlmodel")
let handler = try NLPTaskHandler(modelURL: modelURL)
```

## Fine-Tuning Workflows

### On-Device Fine-Tuning with Core ML

```swift
let updatableModel = try UpdatableModelWrapper(modelURL: modelURL)
let trainingData = [
    TrainingDataPoint(input: "...", expectedOutput: "...")
]
try await updatableModel.fineTune(with: trainingData)
```

### OpenAI Fine-Tuning

```swift
let client = OpenAIClient(apiKey: apiKey)

// Upload training data
let jsonlData = TrainingDataFormatter.formatForOpenAI(data: trainingData)
let file = try await client.uploadFile(
    data: jsonlData.data(using: .utf8)!
)

// Create fine-tuning job
let job = try await client.createFineTuningJob(
    trainingFileId: file.id,
    model: "gpt-3.5-turbo"
)

// Check status
let status = try await client.getFineTuningJob(id: job.id)
```

## Python Integration

### Execute Python Scripts

```swift
let bridge = try PythonBridge()
let result = try bridge.executeScript(at: "path/to/script.py")
```

### Custom Workflows

```swift
let workflowManager = try PythonWorkflowManager()

let customWorkflow = PythonWorkflow(
    name: "Custom Analysis",
    description: "Perform custom data analysis",
    scriptPath: "analysis.py"
) { bridge in
    try await bridge.runAnalytics(
        data: analyticsData,
        scriptPath: "analysis.py"
    )
}

workflowManager.registerWorkflow(customWorkflow)
try await workflowManager.executeWorkflow(named: "Custom Analysis")
```

## Extending GitBot

### Adding New AI Models

1. Implement the `AIModelAdapter` protocol:

```swift
class CustomModelAdapter: AIModelAdapter {
    func predict(_ input: String) async throws -> String {
        // Your implementation
    }
    
    func update(with trainingData: [TrainingDataPoint]) async throws {
        // Your fine-tuning logic
    }
}
```

2. Register with GitBot:

```swift
gitBot.registerModel(CustomModelAdapter())
```

### Creating Custom Workflows

```swift
let workflow = Workflow(
    name: "Issue Triage",
    description: "Automatically triage GitHub issues"
) {
    // Your workflow logic
}
```

## API Reference

### GitBotCore

#### GitBot
Main coordinator class for AI operations.

**Methods:**
- `processCommand(_ command: String) async -> String`
- `startFineTuning(with data: [TrainingDataPoint]) async throws`

#### TrainingDataPoint
Represents a single training sample.

**Properties:**
- `input: String` - Input text
- `expectedOutput: String` - Expected model output
- `metadata: [String: String]` - Additional metadata

### CoreMLModels

#### NLPTaskHandler
Handler for NLP tasks using Core ML.

**Methods:**
- `analyzeIssue(issueText: String) async throws -> IssuePriority`
- `summarizeAnalytics(data: [String]) async throws -> String`

#### UpdatableModelWrapper
Wrapper for Core ML models with update support.

**Methods:**
- `fineTune(with trainingData: [TrainingDataPoint]) async throws`

### OpenAIIntegration

#### OpenAIClient
Client for OpenAI API operations.

**Methods:**
- `createFineTuningJob(trainingFileId: String, model: String) async throws -> FineTuningJob`
- `uploadFile(data: Data, purpose: String) async throws -> FileUploadResponse`
- `createCompletion(prompt: String, model: String) async throws -> String`

### PythonBridge

#### PythonBridge
Bridge for executing Python code from Swift.

**Methods:**
- `executeScript(at path: String) throws -> String`
- `trainModel(scriptPath: String, trainingData: String, modelOutputPath: String) async throws`
- `convertToCoreMl(modelPath: String, outputPath: String) async throws`

## Testing

Run tests with Swift Package Manager:

```bash
cd GitBotXcode
swift test
```

Or in Xcode:
1. Open Package.swift
2. Select the test target
3. Run tests (⌘U)

## Best Practices

### Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Enable on-device training for privacy-sensitive tasks

### Performance
- Cache models locally to reduce load times
- Use batch processing for multiple predictions
- Monitor memory usage with Core ML models

### Model Training
- Start with small datasets for testing
- Validate models before deployment
- Keep training data clean and well-labeled
- Use cross-validation for model evaluation

## Troubleshooting

### Python Integration Issues

If PythonKit can't find Python:
```bash
export PYTHON_LIBRARY=/usr/local/Frameworks/Python.framework/Versions/3.x/lib/libpython3.x.dylib
```

### Core ML Model Issues

Verify model compatibility:
```bash
xcrun coremlcompiler compile model.mlmodel output/
```

### OpenAI API Errors

- Verify API key is valid
- Check rate limits
- Ensure proper data format for fine-tuning

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Resources

- [Core ML Documentation](https://developer.apple.com/documentation/coreml)
- [Create ML Documentation](https://developer.apple.com/documentation/createml)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [PythonKit Repository](https://github.com/pvieito/PythonKit)
- [Swift Package Manager Guide](https://swift.org/package-manager/)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review example code in the repository

---

Built with ❤️ for the AI and developer community