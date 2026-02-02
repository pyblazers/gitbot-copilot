# Getting Started with GitBot

This guide will help you set up and start using GitBot for AI-powered GitHub assistance.

## Prerequisites

Before you begin, ensure you have:
- macOS 13.0 or later
- Xcode 15.0 or later installed
- Basic familiarity with Swift and terminal commands

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/pyblazers/gitbot-copilot.git
cd gitbot-copilot/GitBotXcode

# Verify Swift version
swift --version
```

## Step 2: Build the Project

```bash
# Build with Swift Package Manager
swift build

# Or open in Xcode
open Package.swift
```

## Step 3: Configure GitBot

1. Copy the example configuration:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your settings:
   - Add your OpenAI API key (optional)
   - Set model cache path
   - Configure Python environment path (if using Python features)

## Step 4: Run the Application

### Option A: Command Line
```bash
swift run GitBotApp
```

### Option B: Xcode
1. Open `Package.swift` in Xcode
2. Select the `GitBotApp` scheme
3. Press ⌘R to run

## Step 5: First Interaction

1. Open the **Chat** tab
2. Try a simple command:
   ```
   Analyze this issue: "Critical bug in login system"
   ```
3. GitBot will respond with analysis and priority

## Step 6: Configure Fine-Tuning (Optional)

### For Core ML:
1. Go to the **Fine-tuning** tab
2. Select "Core ML" as the model type
3. Add training data using the "Add Data" button
4. Click "Start Fine-tuning"

### For OpenAI:
1. Go to **Settings** tab
2. Enter your OpenAI API key
3. Return to **Fine-tuning** tab
4. Select "OpenAI GPT-3.5" or "OpenAI GPT-4"
5. Add training data and start fine-tuning

## Step 7: Set Up Python Integration (Optional)

For advanced features:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install coremltools scikit-learn numpy pandas

# Test Python integration
python Scripts/train_model.py --help
```

## Common Tasks

### Task 1: Analyze an Issue

```swift
// In code
let result = await gitBot.processCommand("Analyze: Security vulnerability found")

// In UI
// Use the Chat interface and type your question
```

### Task 2: Train a Custom Model

```bash
# Prepare training data
python Scripts/preprocess_data.py Resources/sample_training_data.jsonl processed.jsonl

# Train model
python Scripts/train_model.py processed.jsonl model.pkl

# Convert to Core ML
python Scripts/convert_to_coreml.py model.pkl model.mlmodel classifier
```

### Task 3: Fine-Tune with OpenAI

```swift
let client = OpenAIClient(apiKey: "your-key")

// Format and upload training data
let jsonlData = TrainingDataFormatter.formatForOpenAI(data: trainingData)
let file = try await client.uploadFile(data: jsonlData.data(using: .utf8)!)

// Create fine-tuning job
let job = try await client.createFineTuningJob(
    trainingFileId: file.id,
    model: "gpt-3.5-turbo"
)
```

## Troubleshooting

### Issue: Cannot find Python

**Solution:**
```bash
export PYTHON_LIBRARY=/usr/local/Frameworks/Python.framework/Versions/3.x/lib/libpython3.x.dylib
```

### Issue: Module not found in Swift

**Solution:**
```bash
# Clean and rebuild
swift package clean
swift build
```

### Issue: OpenAI API errors

**Solution:**
- Verify API key is correct
- Check your OpenAI account has credits
- Ensure data is in correct JSONL format

## Next Steps

1. **Explore the Dashboard**: View analytics and model performance
2. **Customize Models**: Train models on your specific data
3. **Create Workflows**: Build custom automation workflows
4. **Integrate with GitHub**: Connect to actual GitHub repositories

## Learning Resources

- Read the full [README.md](../README.md)
- Check out the [API documentation](API.md)
- Review example code in the test files
- Explore Python scripts in the `Scripts/` directory

## Getting Help

- Review existing [GitHub Issues](https://github.com/pyblazers/gitbot-copilot/issues)
- Check the troubleshooting section in README.md
- Open a new issue with detailed information

## Quick Reference

| Command | Description |
|---------|-------------|
| `swift build` | Build the project |
| `swift test` | Run tests |
| `swift run GitBotApp` | Run the application |
| `python Scripts/train_model.py` | Train a model |
| `python Scripts/convert_to_coreml.py` | Convert to Core ML |

Happy coding! 🚀
