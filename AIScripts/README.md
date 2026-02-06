# AI Scripts Directory

This directory contains Python scripts for AI/ML workflows that integrate with the Xcode External Build System.

## Files

### Python Scripts

- **`fine_tune_model.py`**: Fine-tune pre-trained models on custom datasets
- **`train_model.py`**: Train custom models from scratch
- **`convert_to_coreml.py`**: Convert PyTorch models to Core ML format
- **`build.sh`**: Build script executed by Xcode's External Build System

### Configuration

- **`configs/config.json`**: Model and training configuration
- **`requirements.txt`**: Python package dependencies

### Directories

- **`output/`**: Generated models and artifacts (gitignored)
- **`configs/`**: Configuration files for different workflows
- **`venv/`**: Python virtual environment (gitignored, auto-created)

## Quick Start

### Run Scripts Manually

```bash
# Validate dependencies
python3 fine_tune_model.py --validate-only

# Run fine-tuning
python3 fine_tune_model.py --config configs/config.json

# Train a model
python3 train_model.py --config configs/config.json

# Convert to Core ML
python3 convert_to_coreml.py --config configs/config.json
```

### Run via Xcode

1. Select the `GitBotAI` scheme in Xcode
2. Press `Cmd + B` to build
3. View output in the Report Navigator

## Configuration

Edit `configs/config.json` to customize your workflow:

```json
{
  "model": {
    "name": "gpt2-small",
    "base_model": "gpt2"
  },
  "training": {
    "epochs": 3,
    "batch_size": 8,
    "learning_rate": 5e-5
  },
  "output": {
    "model_path": "AIScripts/output/finetuned_model",
    "coreml_path": "AIScripts/output/model.mlmodel"
  }
}
```

## Logging

All scripts generate detailed logs:

- `fine_tuning.log` - Fine-tuning progress
- `model_training.log` - Training progress
- `coreml_conversion.log` - Conversion progress

## Output

Generated files are saved to the `output/` directory:

- `output/finetuned_model/` - Fine-tuned model checkpoints
- `output/model.mlmodel` - Core ML model (auto-copied to GitBot/Resources)
- `output/logs/` - Training logs and metrics
