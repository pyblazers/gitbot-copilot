# Contributing to GitBot Copilot

Thank you for your interest in contributing to GitBot Copilot! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- macOS, Linux, or Windows with WSL

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gitbot-copilot.git
   cd gitbot-copilot
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

5. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

6. Validate the setup:
   ```bash
   python3 validate.py
   ```

## Development Workflow

### Creating a Branch

Create a descriptive branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Making Changes

1. Make your changes in the appropriate files
2. Add tests for new functionality
3. Update documentation as needed
4. Run tests and linters locally

### Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=gitbot --cov-report=html
```

### Code Quality

Format code with Black:
```bash
black src/ tests/
```

Sort imports with isort:
```bash
isort src/ tests/
```

Lint with flake8:
```bash
flake8 src/ tests/
```

Type checking with mypy:
```bash
mypy src/
```

### Committing Changes

Follow conventional commit format:

```
feat: add new sentiment analysis feature
fix: correct webhook signature verification
docs: update API documentation
test: add tests for code generator
refactor: improve LLM manager structure
```

### Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub
3. Fill out the PR template with details
4. Wait for review and address feedback

## Project Structure

```
gitbot-copilot/
├── src/gitbot/          # Main source code
│   ├── ai/              # AI modules
│   ├── config/          # Configuration
│   ├── webhook/         # Webhook handling
│   └── utils/           # Utilities
├── tests/               # Test files
├── docs/                # Documentation
├── examples/            # Usage examples
└── .github/             # GitHub workflows
```

## Adding New Features

### AI Module

1. Create module in `src/gitbot/ai/`
2. Implement the class with clear docstrings
3. Add tests in `tests/`
4. Update `src/gitbot/core.py` to integrate
5. Add example in `examples/`
6. Document in `docs/api_documentation.md`

### CLI Command

1. Add command parser in `src/gitbot/cli.py`
2. Implement command handler
3. Add tests
4. Update README with usage example

## Documentation

- Use clear, concise language
- Include code examples
- Keep API documentation up to date
- Add inline comments for complex logic

## Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Use pytest fixtures for common setup
- Mock external API calls
- Test error conditions

## Issue Reporting

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version)
- Error messages or logs

### Feature Requests

Include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach
- Any related issues or PRs

## Review Process

1. Maintainers review PRs
2. CI tests must pass
3. Code review feedback is addressed
4. PR is approved and merged

## Release Process

1. Update CHANGELOG.md
2. Update version in setup.py
3. Create release tag
4. Build and publish to PyPI

## Community

- Be respectful and constructive
- Help others in issues and discussions
- Share knowledge and experience
- Celebrate contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask questions in:
- GitHub Issues
- GitHub Discussions
- Pull Request comments

Thank you for contributing to GitBot Copilot! 🚀
