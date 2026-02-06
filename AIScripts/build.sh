#!/bin/bash
# GitBot AI External Build Script
# This script is called by Xcode's External Build System target

set -e  # Exit on error

# Print build information
echo "========================================="
echo "GitBot AI External Build System"
echo "========================================="
echo "Build Action: ${ACTION}"
echo "Configuration: ${CONFIGURATION}"
echo "Source Root: ${SRCROOT}"
echo "========================================="

# Navigate to AI scripts directory
cd "${SRCROOT}/AIScripts"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3."
    exit 1
fi

echo "Python version:"
python3 --version

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing Python dependencies..."
if ! pip install --upgrade pip 2>&1 | grep -E "(error|Error|ERROR)" ; then
    echo "✓ pip upgraded successfully"
fi

echo "Installing packages from requirements.txt..."
if ! pip install -r requirements.txt 2>&1 | grep -E "(error|Error|ERROR|Failed)" ; then
    echo "✓ Dependencies installed successfully"
fi

echo "========================================="
echo "Running AI workflow: Fine-tuning"
echo "========================================="

# Run fine-tuning script with configuration
python3 fine_tune_model.py --config configs/config.json

# Check if model conversion is needed
if [ -f "output/finetuned_model/config.json" ]; then
    echo "========================================="
    echo "Converting to Core ML format"
    echo "========================================="
    python3 convert_to_coreml.py --config configs/config.json
fi

# Copy output to Resources if it exists
if [ -f "output/model.mlmodel" ]; then
    echo "========================================="
    echo "Copying Core ML model to Resources"
    echo "========================================="
    mkdir -p "${SRCROOT}/GitBot/Resources"
    cp output/model.mlmodel "${SRCROOT}/GitBot/Resources/"
    echo "✓ Model copied to ${SRCROOT}/GitBot/Resources/model.mlmodel"
fi

echo "========================================="
echo "✓ GitBot AI Build Completed Successfully"
echo "========================================="

exit 0
