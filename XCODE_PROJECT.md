# GitBot Xcode Project Documentation

## Project Overview

This is a complete, functional Xcode project for **GitBot** - an AI-powered GitHub companion app for macOS. The project is built using SwiftUI and includes Core ML integration for AI fine-tuning capabilities.

## Project Structure

```
GitBot/
├── GitBotApp.swift              # Main app entry point (@main)
├── ContentView.swift             # Main view with navigation sidebar
├── GitBot.entitlements          # App entitlements for sandboxing
├── Models/
│   └── GitHubModel.swift        # Data models (Repository, Issue, PR, etc.)
├── Views/
│   ├── DashboardView.swift      # Main dashboard with stats & activity
│   ├── RepositoryView.swift     # Repository browser interface
│   └── FineTuningView.swift     # AI fine-tuning interface
├── Services/
│   ├── GitHubService.swift      # GitHub API integration
│   └── CoreMLService.swift      # Core ML model management
├── Resources/
│   ├── Info.plist               # App configuration
│   └── Assets.xcassets/         # App icons and colors
│       ├── AppIcon.appiconset/
│       └── AccentColor.colorset/
└── AIScripts/
    ├── fine_tune_model.py       # Python fine-tuning script
    ├── requirements.txt         # Python dependencies
    └── config.json              # Training configuration

GitBot.xcodeproj/
├── project.pbxproj              # Xcode project configuration
└── project.xcworkspace/         # Workspace configuration
```

## Features Implemented

### 1. **SwiftUI Navigation**
- Modern NavigationSplitView with sidebar
- Sections for Dashboard, Repositories, Issues, Pull Requests, and Fine-Tuning
- Clean and intuitive UI design

### 2. **Dashboard View**
- Welcome message and app overview
- Statistics cards (Repositories, Issues, PRs, Fine-Tunings)
- Recent activity feed with timestamps
- Quick action buttons

### 3. **Repository Browser**
- Search functionality
- Repository cards with metadata (stars, forks, language)
- Language color coding
- Refresh capability

### 4. **Fine-Tuning Interface**
- Model selection (GPT-Code-Review, CodeBERT, etc.)
- Training data path input
- Configuration display (epochs, batch size, learning rate)
- Progress tracking with logs
- Model performance metrics

### 5. **GitHub Service**
- Repository fetching and searching
- Issue management (create, update, list)
- Pull request operations
- Code search functionality
- Proper error handling with NetworkError enum

### 6. **Core ML Service**
- Model loading and management
- Fine-tuning workflow integration
- Performance tracking (accuracy, loss, F1 score)
- Python script execution for training

### 7. **Python Integration**
- Complete fine-tuning script with argument parsing
- Configuration file support (JSON)
- Training data validation
- Progress logging
- Core ML conversion support

## Technical Specifications

### Build Settings
- **Platform**: macOS 13.0+
- **Language**: Swift 5.0+
- **UI Framework**: SwiftUI
- **Bundle ID**: com.pyblazers.gitbot
- **Code Signing**: Automatic

### Entitlements
- App Sandbox enabled
- Network client access
- User-selected file read/write access

### Dependencies
The project uses only native Apple frameworks:
- SwiftUI
- Foundation
- CoreML
- Combine (implicit via @Published)

### Python Dependencies (for AI Scripts)
- coremltools >= 7.0
- torch >= 2.0.0
- transformers >= 4.30.0
- numpy >= 1.24.0
- pandas >= 2.0.0
- scikit-learn >= 1.3.0

## How to Build and Run

### Prerequisites
- macOS 13.0 or later
- Xcode 15.0 or later
- (Optional) Python 3.8+ for AI fine-tuning features

### Opening the Project
1. Navigate to the project directory
2. Open `GitBot.xcodeproj` in Xcode
3. Select the GitBot target
4. Choose a destination (My Mac)
5. Click Run (⌘R) or Product > Run

### Building from Command Line
```bash
xcodebuild -project GitBot.xcodeproj \
           -scheme GitBot \
           -configuration Debug \
           build
```

### Running the App
Once built, the app will launch and display:
- A sidebar with navigation options
- The Dashboard view by default
- Sample data for demonstration

## Code Statistics

- **Total Swift Files**: 9
- **Total Lines of Swift Code**: ~1,500
- **Total Python Files**: 1 (fine_tune_model.py)
- **Configuration Files**: 3 (Info.plist, config.json, requirements.txt)

## Architecture

### Design Pattern
The app follows the **MVVM** (Model-View-ViewModel) pattern:
- **Models**: Data structures (Repository, Issue, User, etc.)
- **Views**: SwiftUI views (Dashboard, Repository, FineTuning)
- **ViewModels**: Service classes using `@StateObject` and `@Published`

### State Management
- Uses SwiftUI's native state management (`@State`, `@StateObject`)
- Singleton services (GitHubService.shared, CoreMLService.shared)
- ObservableObject pattern for reactive updates

### Networking
- URLSession-based async/await networking
- Proper error handling with custom NetworkError enum
- GitHub API v3 integration
- Authentication token support (stored in UserDefaults)

## Customization

### Changing the Bundle Identifier
1. Open the project in Xcode
2. Select the GitBot target
3. Go to "Signing & Capabilities"
4. Change the Bundle Identifier

### Adding GitHub Token
The app supports GitHub authentication. To add your token:
1. Get a personal access token from GitHub
2. In the app, navigate to settings (when implemented)
3. Or modify `GitHubService.swift` to set a default token

### Extending Views
To add new views:
1. Create a new Swift file in the `Views/` directory
2. Add the view to `ContentView.swift` navigation
3. Update `NavigationSection` enum if needed

## Known Limitations

1. **Placeholder Data**: Some views use placeholder/mock data
2. **Authentication**: GitHub token management needs Keychain integration
3. **Error Display**: Error alerts need to be implemented in the UI
4. **Python Integration**: Python script execution is simulated
5. **Model Files**: Actual .mlmodel files need to be added for Core ML

## Future Enhancements

- [ ] Keychain integration for secure token storage
- [ ] Real GitHub API integration with live data
- [ ] Actual Python script execution using Process
- [ ] Pre-trained Core ML models included
- [ ] Settings/Preferences window
- [ ] Issue and PR detail views
- [ ] Code syntax highlighting
- [ ] Notifications for GitHub events
- [ ] Multi-account support

## Testing

The project currently doesn't include unit tests, but you can add them:
1. File > New > Target > macOS Unit Testing Bundle
2. Create test files for Services and Models
3. Run tests with ⌘U

## Troubleshooting

### Build Fails
- Ensure you're using macOS 13.0+ and Xcode 15.0+
- Clean build folder: Product > Clean Build Folder (⌘⇧K)
- Reset package dependencies if any are added later

### App Crashes on Launch
- Check Console.app for crash logs
- Verify Info.plist is properly configured
- Ensure all Swift files are included in the target

### UI Not Displaying Correctly
- Check that SwiftUI previews work in Xcode
- Verify Asset Catalog is properly linked
- Try running on a real Mac instead of simulator

## Support

For issues or questions:
1. Check the GitHub repository issues
2. Review the inline code comments
3. Consult SwiftUI and Core ML documentation

## License

Copyright © 2024 PyBlazers. All rights reserved.

## Acknowledgments

Built with:
- SwiftUI for the user interface
- Core ML for machine learning integration
- GitHub REST API for repository integration
