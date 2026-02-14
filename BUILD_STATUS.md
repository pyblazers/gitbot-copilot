# Build Status and CI/CD Documentation

## Overview

This document describes the build system, continuous integration, and testing infrastructure for GitBot Copilot.

## Build Status

[![Build and Test](https://github.com/pyblazers/gitbot-copilot/actions/workflows/build.yml/badge.svg)](https://github.com/pyblazers/gitbot-copilot/actions/workflows/build.yml)

## Continuous Integration

The project uses GitHub Actions for automated builds and testing on every commit and pull request.

### Supported Platforms

| Platform | Runner | Swift Version | Status |
|----------|--------|---------------|--------|
| Linux | ubuntu-latest | 5.9 | ✅ Core modules |
| macOS | macos-latest | Latest | ✅ Full stack |

### Workflows

#### Build and Test (`build.yml`)

This workflow runs on:
- Push to `main`, `master`, `develop`, or any `copilot/**` branch
- Pull requests to `main`, `master`, or `develop`
- Manual dispatch

**Jobs:**

1. **build-linux**: Builds on Ubuntu Linux
   - Sets up Swift 5.9
   - Builds GitBotXcode package
   - Runs all tests
   - Tests core modules (GitBotCore, OpenAIIntegration, PythonBridge)

2. **build-macos**: Builds on macOS
   - Uses latest macOS runner with native Swift
   - Builds GitBotXcode package including SwiftUI
   - Runs all tests
   - Tests full stack including Core ML features

3. **check-python-scripts**: Validates Python scripts
   - Sets up Python 3.9
   - Installs dependencies from requirements.txt
   - Syntax checks all Python scripts
   - Tests script help output

## Local Build Instructions

### Prerequisites

- Swift 5.9 or later
- Xcode 15.0 or later (for macOS UI features)
- Python 3.8+ (optional, for Python scripts)

### Building

```bash
# Navigate to the Swift package
cd GitBotXcode

# Build in debug mode
swift build

# Build in release mode
swift build -c release

# Clean build artifacts
swift package clean
```

### Testing

```bash
# Run all tests
swift test

# Run tests with verbose output
swift test -v

# Run specific test
swift test --filter GitBotCoreTests
```

### Build Artifacts

Build artifacts are stored in:
- `.build/debug/` - Debug builds
- `.build/release/` - Release builds
- `.build/x86_64-unknown-linux-gnu/` - Linux builds
- `.build/arm64-apple-macosx/` - macOS ARM builds
- `.build/x86_64-apple-macosx/` - macOS Intel builds

**Note:** The `.build/` directory is excluded from version control via `.gitignore`.

## Build Configuration

### Swift Package Manager

The project uses Swift Package Manager (SPM) with the following structure:

```
GitBotXcode/
├── Package.swift          # Package manifest
├── Sources/
│   ├── GitBotCore/       # Core functionality (cross-platform)
│   ├── CoreMLModels/     # Core ML integration (macOS only)
│   ├── OpenAIIntegration/# OpenAI API client
│   ├── PythonBridge/     # Python interoperability
│   └── SwiftUIApp/       # macOS UI (conditional compilation)
└── Tests/
    ├── GitBotCoreTests.swift
    ├── CoreMLIntegrationTests.swift
    └── OpenAIIntegrationTests.swift
```

### Platform-Specific Features

Some features are conditionally compiled based on platform:

```swift
#if canImport(CoreML) && canImport(NaturalLanguage)
// macOS-only Core ML code
#else
// Cross-platform fallback
#endif

#if canImport(SwiftUI) && canImport(Combine)
// SwiftUI app (macOS only)
#endif
```

## Test Coverage

| Module | Tests | Status |
|--------|-------|--------|
| GitBotCore | 6 tests | ✅ Passing |
| CoreMLModels | 2 tests | ✅ Passing |
| OpenAIIntegration | 4 tests | ✅ Passing |
| **Total** | **12 tests** | **✅ All Passing** |

### Test Execution Time

- Average test suite time: ~1.1 seconds
- Platform: Linux (x86_64-unknown-linux-gnu)
- Swift Testing Library: 6.2.3

## Dependencies

### Swift Dependencies

- **PythonKit** (master branch)
  - Repository: https://github.com/pvieito/PythonKit.git
  - Purpose: Python interoperability

### Python Dependencies

See `requirements.txt` for Python packages:
- coremltools >= 7.0
- scikit-learn >= 1.3.0
- numpy >= 1.24.0
- pandas >= 2.0.0
- nltk >= 3.8.0
- scipy >= 1.11.0
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## Build Troubleshooting

### Common Issues

**Issue: Swift version not found**
```bash
# Install Swift or update to 5.9+
swift --version
```

**Issue: PythonKit dependency fails**
```bash
# Clean and rebuild
swift package clean
swift package resolve
swift build
```

**Issue: Core ML not available**
- Core ML features only work on macOS 13.0+
- Linux builds use fallback implementations

**Issue: Build artifacts too large**
```bash
# Clean build directory
rm -rf .build/
swift build
```

### Platform-Specific Notes

#### Linux
- Core ML features are stubbed out
- SwiftUI app is excluded from build
- All core functionality works

#### macOS
- Full feature support
- Core ML available on macOS 13.0+
- SwiftUI available on macOS 13.0+

## Continuous Deployment

Currently, the project focuses on continuous integration. Future plans include:

- [ ] Automated release builds
- [ ] Binary distribution
- [ ] Swift Package registry publication
- [ ] Docker images for Linux
- [ ] macOS app bundle creation

## Monitoring Build Health

To monitor build health:

1. Check the [Actions tab](https://github.com/pyblazers/gitbot-copilot/actions) on GitHub
2. Review build badges in README.md
3. Subscribe to workflow notifications
4. Review test results in workflow logs

## Contributing

When contributing code:

1. Ensure all tests pass locally
2. Run `swift build` before committing
3. Run `swift test` to validate changes
4. Check that CI passes on your PR
5. Review any platform-specific considerations

## Resources

- [Swift Package Manager Documentation](https://swift.org/package-manager/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Swift on Linux](https://swift.org/download/)
- [Xcode Downloads](https://developer.apple.com/xcode/)

---

**Last Updated:** 2026-02-14
**CI System:** GitHub Actions
**Build Tool:** Swift Package Manager
