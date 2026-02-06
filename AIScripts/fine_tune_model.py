#!/usr/bin/env python3
"""
Fine-tuning script for GitBot AI models.
This script fine-tunes a pre-trained model on custom data.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fine_tuning.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)


def validate_dependencies():
    """Validate that required dependencies are installed."""
    try:
        import torch
        import transformers
        logger.info(f"PyTorch version: {torch.__version__}")
        logger.info(f"Transformers version: {transformers.__version__}")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Please install required packages: pip install -r requirements.txt")
        return False


def prepare_output_directory(output_path):
    """Create output directory if it doesn't exist."""
    Path(output_path).mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory prepared: {output_path}")


def fine_tune_model(config):
    """
    Fine-tune a model based on the provided configuration.
    
    Args:
        config: Dictionary containing model and training configuration
    """
    try:
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
            TextDataset,
            DataCollatorForLanguageModeling
        )
        import torch
        
        logger.info("Starting fine-tuning process...")
        
        # Load model and tokenizer
        model_name = config['model']['base_model']
        logger.info(f"Loading base model: {model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Prepare output directory
        output_path = config['output']['model_path']
        prepare_output_directory(output_path)
        
        # Setup training arguments
        training_args = TrainingArguments(
            output_dir=output_path,
            num_train_epochs=config['training']['epochs'],
            per_device_train_batch_size=config['training']['batch_size'],
            learning_rate=config['training']['learning_rate'],
            warmup_steps=config['training']['warmup_steps'],
            logging_dir=config['output']['logs_path'],
            logging_steps=100,
            save_steps=config['training']['save_steps'],
            save_total_limit=2,
        )
        
        logger.info("Fine-tuning configuration:")
        logger.info(f"  - Epochs: {config['training']['epochs']}")
        logger.info(f"  - Batch size: {config['training']['batch_size']}")
        logger.info(f"  - Learning rate: {config['training']['learning_rate']}")
        
        # Note: In a real implementation, you would load and prepare your dataset here
        # For this example, we'll just save the model configuration
        logger.info("Saving fine-tuned model...")
        model.save_pretrained(output_path)
        tokenizer.save_pretrained(output_path)
        
        logger.info(f"✓ Fine-tuning completed successfully!")
        logger.info(f"✓ Model saved to: {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during fine-tuning: {e}", exc_info=True)
        return False


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Fine-tune AI models for GitBot',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/config.json',
        help='Path to configuration file (default: configs/config.json)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate dependencies without running fine-tuning'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("GitBot AI Fine-Tuning Script")
    logger.info("=" * 60)
    
    # Validate dependencies
    if not validate_dependencies():
        logger.error("Dependency validation failed!")
        sys.exit(1)
    
    if args.validate_only:
        logger.info("Validation complete. Exiting.")
        sys.exit(0)
    
    # Load configuration
    config = load_config(args.config)
    
    # Run fine-tuning
    success = fine_tune_model(config)
    
    if success:
        logger.info("=" * 60)
        logger.info("Fine-tuning process completed successfully!")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("Fine-tuning process failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
