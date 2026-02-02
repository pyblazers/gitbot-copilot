#!/usr/bin/env python3
"""
Data preprocessing script for GitBot training data
"""

import json
import sys
import re
from pathlib import Path

def preprocess_github_issue(issue_text):
    """Preprocess GitHub issue text"""
    # Remove URLs
    text = re.sub(r'http\S+', '', issue_text)
    
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove inline code
    text = re.sub(r'`[^`]*`', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()

def extract_features(text):
    """Extract features from text"""
    features = {
        'length': len(text),
        'word_count': len(text.split()),
        'has_urgent_keywords': any(word in text.lower() for word in ['urgent', 'critical', 'asap', 'immediately']),
        'has_bug_keywords': any(word in text.lower() for word in ['bug', 'error', 'crash', 'fail']),
        'has_feature_keywords': any(word in text.lower() for word in ['feature', 'enhancement', 'improve']),
        'has_question_keywords': any(word in text.lower() for word in ['how', 'why', 'what', 'question']),
    }
    return features

def preprocess_dataset(input_path, output_path):
    """Preprocess entire dataset"""
    print(f"Loading data from {input_path}...")
    
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    print(f"Loaded {len(data)} samples")
    
    # Preprocess each sample
    processed_data = []
    for item in data:
        processed_item = {
            'original_input': item.get('input', ''),
            'processed_input': preprocess_github_issue(item.get('input', '')),
            'output': item.get('output', ''),
            'features': extract_features(item.get('input', '')),
            'metadata': item.get('metadata', {})
        }
        processed_data.append(processed_item)
    
    # Save processed data
    print(f"Saving processed data to {output_path}...")
    with open(output_path, 'w') as f:
        for item in processed_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"Preprocessing complete! Saved {len(processed_data)} samples")
    
    # Print statistics
    print("\nDataset Statistics:")
    print(f"  Total samples: {len(processed_data)}")
    print(f"  Avg input length: {sum(item['features']['length'] for item in processed_data) / len(processed_data):.1f} chars")
    print(f"  Avg word count: {sum(item['features']['word_count'] for item in processed_data) / len(processed_data):.1f} words")

def main():
    if len(sys.argv) < 3:
        print("Usage: python preprocess_data.py <input.jsonl> <output.jsonl>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not Path(input_path).exists():
        print(f"Error: Input file {input_path} not found")
        sys.exit(1)
    
    preprocess_dataset(input_path, output_path)

if __name__ == "__main__":
    main()
