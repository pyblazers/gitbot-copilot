#!/usr/bin/env python3
"""Validate GitBot installation and structure."""

import os
import sys
from pathlib import Path


def validate_structure():
    """Validate project structure."""
    print("Validating project structure...")
    
    base_dir = Path(__file__).parent
    required_files = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "setup.py",
        "requirements.txt",
        "requirements-dev.txt",
        ".env.example",
        ".gitignore",
    ]
    
    required_dirs = [
        "src/gitbot",
        "src/gitbot/ai",
        "src/gitbot/config",
        "src/gitbot/webhook",
        "src/gitbot/utils",
        "tests",
        "docs",
        "examples",
    ]
    
    required_modules = [
        "src/gitbot/__init__.py",
        "src/gitbot/core.py",
        "src/gitbot/cli.py",
        "src/gitbot/ai/llm_manager.py",
        "src/gitbot/ai/nlp_processor.py",
        "src/gitbot/ai/code_generator.py",
        "src/gitbot/ai/workflow_manager.py",
        "src/gitbot/ai/sentiment_analyzer.py",
        "src/gitbot/ai/predictive_tasks.py",
        "src/gitbot/ai/analytics.py",
        "src/gitbot/config/settings.py",
        "src/gitbot/webhook/listener.py",
        "src/gitbot/utils/logging.py",
    ]
    
    errors = []
    
    # Check files
    for file_path in required_files:
        if not (base_dir / file_path).exists():
            errors.append(f"Missing file: {file_path}")
    
    # Check directories
    for dir_path in required_dirs:
        if not (base_dir / dir_path).is_dir():
            errors.append(f"Missing directory: {dir_path}")
    
    # Check modules
    for module_path in required_modules:
        if not (base_dir / module_path).exists():
            errors.append(f"Missing module: {module_path}")
    
    if errors:
        print("\n❌ Validation failed with errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ All required files and directories are present")
    return True


def validate_imports():
    """Validate basic imports without external dependencies."""
    print("\nValidating basic imports...")
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    try:
        # Check if we can at least import the modules (structure validation)
        import importlib.util
        
        modules_to_check = [
            "gitbot.config.settings",
            "gitbot.core",
            "gitbot.cli",
            "gitbot.ai.llm_manager",
        ]
        
        for module_name in modules_to_check:
            module_path = str(Path(__file__).parent / "src" / module_name.replace(".", "/")) + ".py"
            if Path(module_path).exists():
                print(f"  ✅ Module file exists: {module_name}")
            else:
                print(f"  ❌ Module file missing: {module_name}")
                return False
        
        print("  ℹ️  Note: Full import test requires dependencies (pip install -e .)")
        
    except Exception as e:
        print(f"  ❌ Import validation failed: {e}")
        return False
    
    return True


def validate_documentation():
    """Validate documentation files."""
    print("\nValidating documentation...")
    
    base_dir = Path(__file__).parent
    docs = [
        "docs/quickstart.md",
        "docs/api_documentation.md",
        "docs/macos_deployment.md",
    ]
    
    for doc in docs:
        doc_path = base_dir / doc
        if not doc_path.exists():
            print(f"  ❌ Missing documentation: {doc}")
            return False
        
        # Check if file has content
        if doc_path.stat().st_size == 0:
            print(f"  ❌ Empty documentation: {doc}")
            return False
    
    print("  ✅ All documentation files are present and non-empty")
    return True


def validate_examples():
    """Validate example files."""
    print("\nValidating examples...")
    
    base_dir = Path(__file__).parent
    examples = [
        "examples/basic_usage.py",
        "examples/webhook_server.py",
        "examples/workflow_example.py",
    ]
    
    for example in examples:
        example_path = base_dir / example
        if not example_path.exists():
            print(f"  ❌ Missing example: {example}")
            return False
        
        if example_path.stat().st_size == 0:
            print(f"  ❌ Empty example: {example}")
            return False
    
    print("  ✅ All example files are present and non-empty")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("GitBot Copilot - Installation Validator")
    print("=" * 60)
    
    results = []
    
    results.append(("Structure", validate_structure()))
    results.append(("Imports", validate_imports()))
    results.append(("Documentation", validate_documentation()))
    results.append(("Examples", validate_examples()))
    
    print("\n" + "=" * 60)
    print("Validation Results:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20s}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All validations passed! GitBot is ready to use.")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env and add your API keys")
        print("  2. Install dependencies: pip install -e .")
        print("  3. Run: gitbot --help")
        return 0
    else:
        print("\n⚠️  Some validations failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
