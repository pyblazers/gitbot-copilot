# GitBot

A macOS application built with SwiftUI that integrates Python-based AI workflows for model training, fine-tuning, and Core ML conversion directly within Xcode.

## Overview

GitBot combines the power of Swift/SwiftUI for native macOS UI with Python's machine learning ecosystem. The project features an **External Build System target** (`GitBotAI`) that enables seamless integration of Python-based AI workflows without compromising the main Swift app architecture.

## Features

### Main Application (GitBot)
- **SwiftUI Dashboard**: Modern macOS interface with tabs for Dashboard, AI Workflows, and Settings
- **AI Workflow Management**: Trigger and monitor Python-based AI tasks from within the app
- **Core ML Integration**: Automatically use fine-tuned models in the Swift application
- **Real-time Status**: Track workflow execution and model availability

### External Build System (GitBotAI)
- **Python-based AI Workflows**: 
  - Model fine-tuning (`fine_tune_model.py`)
  - Custom model training (`train_model.py`)
  - Core ML conversion (`convert_to_coreml.py`)
- **Automated Build Integration**: Execute Python scripts as part of the Xcode build process
- **Dependency Management**: Automatic Python virtual environment and package installation
- **Output Integration**: Automatically copy generated ML models to app Resources

## Architecture

```
GitBot.xcodeproj/
├── GitBot (Main App Target)
│   └── Native Swift/SwiftUI macOS application
└── GitBotAI (External Build System Target)
    └── Python-based AI workflows

AIScripts/
├── fine_tune_model.py      # Fine-tune pre-trained models
├── train_model.py           # Train custom models
├── convert_to_coreml.py    # Convert to Core ML format
├── build.sh                 # Build script executed by Xcode
├── requirements.txt         # Python dependencies
└── configs/
    └── config.json          # Model & training configuration
```

## Setup Instructions

### Prerequisites

1. **Xcode**: Version 15.0 or later
2. **macOS**: Version 13.0 (Ventura) or later
3. **Python 3**: Version 3.8 or later

### Python Environment Setup

1. **Verify Python Installation**:
   ```bash
   python3 --version
   ```

2. **Install Python Dependencies** (optional - build script handles this automatically):
   ```bash
   cd AIScripts
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Building the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pyblazers/gitbot-copilot.git
   cd gitbot-copilot
   ```

2. **Open in Xcode**:
   ```bash
   open GitBot.xcodeproj
   ```

3. **Select Target**:
   - For the main app: Select `GitBot` scheme
   - For AI workflows: Select `GitBotAI` scheme

4. **Build and Run**:
   - Press `Cmd + B` to build
   - Press `Cmd + R` to run the main app

## Using the External Build System

### Running AI Workflows from Xcode

1. **Select the GitBotAI Target**:
   - In Xcode, change the active scheme to `GitBotAI`
   - Or use Product → Scheme → GitBotAI

2. **Build the Target**:
   - Press `Cmd + B` or Product → Build
   - The build script will:
     - Create/activate Python virtual environment
     - Install dependencies from `requirements.txt`
     - Execute the fine-tuning workflow
     - Convert models to Core ML format
     - Copy outputs to `GitBot/Resources/`

3. **View Build Output**:
   - Open the Report Navigator (Cmd + 9)
   - Select the latest build to see detailed Python script output

### Configuring AI Workflows

Edit `AIScripts/configs/config.json` to customize your workflow:

```json
{
  "model": {
    "name": "gpt2-small",
    "type": "text-generation",
    "base_model": "gpt2"
  },
  "training": {
    "epochs": 3,
    "batch_size": 8,
    "learning_rate": 5e-5,
    "max_length": 512
  },
  "output": {
    "model_path": "AIScripts/output/finetuned_model",
    "coreml_path": "AIScripts/output/model.mlmodel"
  }
}
```

### Running Workflows Manually

You can also run Python scripts directly from the command line:

```bash
cd AIScripts

# Fine-tune a model
python3 fine_tune_model.py --config configs/config.json

# Train from scratch
python3 train_model.py --config configs/config.json

# Convert to Core ML
python3 convert_to_coreml.py --config configs/config.json

# Validate dependencies only
python3 fine_tune_model.py --validate-only
```

## Python Scripts Reference

### fine_tune_model.py

Fine-tunes pre-trained models on custom datasets.

**Usage**:
```bash
python3 fine_tune_model.py --config configs/config.json
```

**Features**:
- Loads pre-trained models from Hugging Face
- Applies transfer learning with custom data
- Saves fine-tuned models for conversion
- Comprehensive logging with progress tracking

### train_model.py

Trains custom models from scratch.

**Usage**:
```bash
python3 train_model.py --config configs/config.json
```

**Features**:
- Initialize models with custom architectures
- Train on proprietary datasets
- Full control over hyperparameters
- Save checkpoints and training metadata

### convert_to_coreml.py

Converts PyTorch models to Core ML format.

**Usage**:
```bash
python3 convert_to_coreml.py --config configs/config.json
```

**Features**:
- Converts trained models to `.mlmodel` format
- Optimizes for iOS/macOS deployment
- Validates model compatibility
- Generates model metadata

## Dependencies

### Python Packages

Defined in `AIScripts/requirements.txt`:

- `coremltools>=7.0` - Core ML conversion
- `torch>=2.0.0` - PyTorch deep learning framework
- `transformers>=4.30.0` - Hugging Face transformers
- `openai>=1.0.0` - OpenAI API integration
- `numpy>=1.24.0` - Numerical computing
- `scikit-learn>=1.3.0` - Machine learning utilities

### Swift Packages

The main app uses only native SwiftUI frameworks. No external dependencies required.

## Troubleshooting

### Python Not Found

**Error**: `python3: command not found`

**Solution**:
```bash
# Install Python via Homebrew
brew install python3

# Or download from python.org
# https://www.python.org/downloads/
```

### Virtual Environment Issues

**Error**: Cannot create virtual environment

**Solution**:
```bash
# Install venv module
python3 -m pip install --user virtualenv

# Or use system Python
python3 -m ensurepip --upgrade
```

### Build Script Fails

**Error**: Build script exits with error

**Solution**:
1. Check build log in Xcode (Report Navigator)
2. Run script manually to see detailed errors:
   ```bash
   cd AIScripts
   bash build.sh
   ```
3. Verify Python dependencies:
   ```bash
   python3 fine_tune_model.py --validate-only
   ```

### Core ML Conversion Errors

**Error**: Model conversion fails

**Solution**:
- Ensure `coremltools` is installed: `pip install coremltools>=7.0`
- Check model compatibility with Core ML
- Verify PyTorch model is in evaluation mode
- Review conversion logs in `AIScripts/coreml_conversion.log`

### Permission Denied on Scripts

**Error**: `Permission denied` when running `.py` or `.sh` files

**Solution**:
```bash
chmod +x AIScripts/*.py AIScripts/build.sh
```

## Project Structure

```
gitbot-copilot/
├── README.md                    # This file
├── .gitignore                  # Git ignore rules
├── GitBot.xcodeproj/           # Xcode project
│   └── project.pbxproj         # Project configuration
├── GitBot/                     # Main app target
│   ├── Sources/
│   │   ├── GitBotApp.swift     # App entry point
│   │   ├── ContentView.swift   # Main view
│   │   ├── DashboardView.swift # Dashboard tab
│   │   ├── AIWorkflowView.swift # AI workflows tab
│   │   └── SettingsView.swift  # Settings tab
│   ├── Resources/
│   │   └── Assets.xcassets/    # App assets
│   └── GitBot.entitlements     # App permissions
└── AIScripts/                  # External build target
    ├── build.sh                # Build script
    ├── requirements.txt        # Python dependencies
    ├── fine_tune_model.py      # Fine-tuning script
    ├── train_model.py          # Training script
    ├── convert_to_coreml.py    # Conversion script
    ├── configs/
    │   └── config.json         # Configuration
    └── output/                 # Generated models (gitignored)
```

## Development Workflow

### Typical Workflow

1. **Modify AI Configuration**: Edit `AIScripts/configs/config.json`
2. **Run AI Workflow**: Build the `GitBotAI` target in Xcode
3. **Verify Output**: Check `AIScripts/output/` for generated models
4. **Use in App**: Models are automatically copied to `GitBot/Resources/`
5. **Build Main App**: Switch to `GitBot` scheme and build
6. **Test Integration**: Run the app and verify model availability

### Adding New Python Scripts

1. Create script in `AIScripts/` directory
2. Make it executable: `chmod +x AIScripts/your_script.py`
3. Update `build.sh` to call your script
4. Add any new dependencies to `requirements.txt`
5. Document in this README

### Modifying the Swift App

1. Navigate to `GitBot/Sources/`
2. Edit Swift files as needed
3. Build and run the `GitBot` target
4. Swift changes do not affect the Python workflows

## Best Practices

### Separation of Concerns

- **Swift/SwiftUI**: UI, app logic, Core ML inference
- **Python**: Model training, fine-tuning, conversion
- **External Build System**: Bridge between Python and Swift

### Version Control

- Python virtual environments are gitignored
- ML model outputs are gitignored
- Only source code and configuration are tracked

### Security

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Review `GitBot.entitlements` for app permissions

## Contributing

When contributing to this project:

1. Maintain separation between Swift and Python code
2. Update documentation for new features
3. Test both targets (GitBot and GitBotAI)
4. Follow existing code style and patterns
5. Add appropriate error handling and logging

## License

This project is part of the GitBot initiative. Refer to the repository license for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review existing documentation
- Check troubleshooting section above

## Acknowledgments

- Built with SwiftUI for macOS
- Powered by PyTorch and Hugging Face Transformers
- Integrated with Core ML for on-device inference