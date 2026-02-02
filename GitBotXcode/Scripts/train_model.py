#!/usr/bin/env python3
"""
Sample model training script for GitBot
This script demonstrates how to train a simple NLP model for issue classification
"""

import json
import sys
from pathlib import Path

def load_training_data(data_path):
    """Load training data from JSONL file"""
    data = []
    with open(data_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def preprocess_text(text):
    """Basic text preprocessing"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters (basic version)
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    return text

def train_model(training_data, output_path):
    """
    Train a simple model
    In production, this would use scikit-learn, TensorFlow, or PyTorch
    """
    print(f"Training with {len(training_data)} samples...")
    
    # Placeholder for actual training logic
    # Example with scikit-learn:
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # from sklearn.naive_bayes import MultinomialNB
    # vectorizer = TfidfVectorizer()
    # X = vectorizer.fit_transform([d['input'] for d in training_data])
    # y = [d['output'] for d in training_data]
    # model = MultinomialNB()
    # model.fit(X, y)
    
    print(f"Model trained successfully")
    print(f"Saving model to {output_path}")
    
    # Save model
    model_info = {
        "version": "1.0",
        "samples": len(training_data),
        "accuracy": 0.92  # Placeholder
    }
    
    with open(output_path, 'w') as f:
        json.dump(model_info, f)
    
    return model_info

def main():
    if len(sys.argv) < 3:
        print("Usage: python train_model.py <training_data.jsonl> <output_model_path>")
        sys.exit(1)
    
    data_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Load and preprocess data
    training_data = load_training_data(data_path)
    
    # Train model
    model_info = train_model(training_data, output_path)
    
    print(f"Training complete!")
    print(f"Model info: {json.dumps(model_info, indent=2)}")

if __name__ == "__main__":
    main()
