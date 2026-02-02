"""Test configuration."""

import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Set test environment variables
os.environ['OPENAI_API_KEY'] = 'test-key'
os.environ['GITHUB_TOKEN'] = 'test-token'
os.environ['ENABLE_NLP'] = 'False'
os.environ['ENABLE_CODE_GENERATION'] = 'False'
os.environ['ENABLE_SENTIMENT_ANALYSIS'] = 'False'
os.environ['ENABLE_PREDICTIVE_TASKS'] = 'False'
os.environ['ENABLE_ANALYTICS'] = 'False'
