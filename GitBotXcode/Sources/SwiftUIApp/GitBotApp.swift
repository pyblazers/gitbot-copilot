#if canImport(SwiftUI) && canImport(Combine)
import SwiftUI
import Combine
import GitBotCore
import CoreMLModels
import OpenAIIntegration
import PythonBridge

// GitBot SwiftUI App - macOS Only
// This app provides a native macOS interface for GitBot
// For cross-platform command-line usage, use GitBotCore directly

@available(macOS 13.0, *)
@main
struct GitBotApp: App {
    @StateObject private var gitBot = ObservableGitBot()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(gitBot)
        }
        .commands {
            CommandGroup(replacing: .appInfo) {
                Button("About GitBot") {
                    // Show about dialog
                }
            }
        }
    }
}

/// ObservableObject wrapper for GitBot
@available(macOS 13.0, *)
class ObservableGitBot: ObservableObject {
    @Published var gitBot: GitBot
    @Published var isTraining: Bool = false
    @Published var lastError: String?
    
    init() {
        self.gitBot = GitBot()
    }
    
    var configuration: GitBotConfiguration {
        get { gitBot.configuration }
        set { gitBot.configuration = newValue }
    }
    
    func processCommand(_ command: String) async -> String {
        return await gitBot.processCommand(command)
    }
    
    func startFineTuning(with data: [TrainingDataPoint]) async throws {
        isTraining = true
        defer { isTraining = false }
        try await gitBot.startFineTuning(with: data)
    }
}

@available(macOS 13.0, *)

@available(macOS 13.0, *)
struct ContentView: View {
    @EnvironmentObject var gitBot: ObservableGitBot
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "chart.bar.fill")
                }
                .tag(0)
            
            ChatInterfaceView()
                .tabItem {
                    Label("Chat", systemImage: "message.fill")
                }
                .tag(1)
            
            FineTuningView()
                .tabItem {
                    Label("Fine-tuning", systemImage: "slider.horizontal.3")
                }
                .tag(2)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
        .frame(minWidth: 800, minHeight: 600)
    }
}

@available(macOS 13.0, *)
struct DashboardView: View {
    @EnvironmentObject var gitBot: ObservableGitBot
    @State private var analyticsData: [AnalyticsItem] = []
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Header
                    HStack {
                        VStack(alignment: .leading) {
                            Text("GitBot Dashboard")
                                .font(.largeTitle)
                                .bold()
                            Text("AI-Powered GitHub Assistant")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                    }
                    .padding()
                    
                    // Stats Cards
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
                        StatCard(title: "Active Models", value: "3", icon: "brain")
                        StatCard(title: "Training Jobs", value: gitBot.isTraining ? "1" : "0", icon: "arrow.triangle.2.circlepath")
                        StatCard(title: "API Calls Today", value: "142", icon: "network")
                        StatCard(title: "Accuracy", value: "94.2%", icon: "chart.line.uptrend.xyaxis")
                    }
                    .padding(.horizontal)
                    
                    // Analytics Summary
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Recent Analytics")
                            .font(.headline)
                        
                        if analyticsData.isEmpty {
                            Text("No analytics data available")
                                .foregroundColor(.secondary)
                                .padding()
                        } else {
                            ForEach(analyticsData) { item in
                                AnalyticsRow(item: item)
                            }
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                    .padding(.horizontal)
                }
                .padding()
            }
            .navigationTitle("Dashboard")
        }
        .onAppear {
            loadAnalytics()
        }
    }
    
    private func loadAnalytics() {
        // Load analytics data
        analyticsData = [
            AnalyticsItem(title: "Issue Classification", value: "85% accuracy"),
            AnalyticsItem(title: "Response Time", value: "1.2s avg"),
            AnalyticsItem(title: "User Satisfaction", value: "4.5/5")
        ]
    }
}

@available(macOS 13.0, *)
struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(.accentColor)
                Spacer()
            }
            Text(value)
                .font(.title)
                .bold()
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

struct AnalyticsItem: Identifiable {
    let id = UUID()
    let title: String
    let value: String
}

@available(macOS 13.0, *)
struct AnalyticsRow: View {
    let item: AnalyticsItem
    
    var body: some View {
        HStack {
            Text(item.title)
                .font(.subheadline)
            Spacer()
            Text(item.value)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

@available(macOS 13.0, *)
struct ChatInterfaceView: View {
    @EnvironmentObject var gitBot: ObservableGitBot
    @State private var inputText = ""
    @State private var messages: [ChatMessage] = []
    @State private var isProcessing = false
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Natural Language Interface")
                    .font(.headline)
                Spacer()
                if isProcessing {
                    ProgressView()
                        .scaleEffect(0.8)
                }
            }
            .padding()
            .background(Color(.systemGray6))
            
            // Messages
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(messages) { message in
                            ChatBubble(message: message)
                                .id(message.id)
                        }
                    }
                    .padding()
                }
                .onChange(of: messages.count) { _ in
                    if let lastMessage = messages.last {
                        withAnimation {
                            proxy.scrollTo(lastMessage.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            // Input
            HStack(spacing: 12) {
                TextField("Type your command or question...", text: $inputText)
                    .textFieldStyle(.roundedBorder)
                    .onSubmit {
                        sendMessage()
                    }
                
                Button(action: sendMessage) {
                    Image(systemName: "paperplane.fill")
                }
                .disabled(inputText.isEmpty || isProcessing)
                .buttonStyle(.borderedProminent)
            }
            .padding()
        }
    }
    
    private func sendMessage() {
        guard !inputText.isEmpty else { return }
        
        let userMessage = ChatMessage(content: inputText, isUser: true)
        messages.append(userMessage)
        
        let query = inputText
        inputText = ""
        isProcessing = true
        
        Task {
            let response = await gitBot.processCommand(query)
            let botMessage = ChatMessage(content: response, isUser: false)
            
            await MainActor.run {
                messages.append(botMessage)
                isProcessing = false
            }
        }
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let content: String
    let isUser: Bool
    let timestamp = Date()
}

@available(macOS 13.0, *)
struct ChatBubble: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.isUser { Spacer() }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                Text(message.content)
                    .padding(12)
                    .background(message.isUser ? Color.accentColor : Color(.systemGray5))
                    .foregroundColor(message.isUser ? .white : .primary)
                    .cornerRadius(16)
                
                Text(message.timestamp, style: .time)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            .frame(maxWidth: 500, alignment: message.isUser ? .trailing : .leading)
            
            if !message.isUser { Spacer() }
        }
    }
}

@available(macOS 13.0, *)
struct FineTuningView: View {
    @EnvironmentObject var gitBot: ObservableGitBot
    @State private var trainingData: [TrainingDataPoint] = []
    @State private var selectedModel = "Core ML"
    @State private var isShowingDataInput = false
    @State private var fineTuningJobs: [FineTuningJobInfo] = []
    
    let modelOptions = ["Core ML", "OpenAI GPT-3.5", "OpenAI GPT-4"]
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                HStack {
                    VStack(alignment: .leading) {
                        Text("Fine-tuning Manager")
                            .font(.largeTitle)
                            .bold()
                        Text("Train and adapt AI models")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    Spacer()
                }
                .padding()
                
                // Model Selection
                VStack(alignment: .leading, spacing: 8) {
                    Text("Select Model")
                        .font(.headline)
                    
                    Picker("Model", selection: $selectedModel) {
                        ForEach(modelOptions, id: \.self) { model in
                            Text(model).tag(model)
                        }
                    }
                    .pickerStyle(.segmented)
                }
                .padding()
                
                // Training Data
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Text("Training Data (\(trainingData.count) samples)")
                            .font(.headline)
                        Spacer()
                        Button("Add Data") {
                            isShowingDataInput = true
                        }
                        .buttonStyle(.borderedProminent)
                    }
                    
                    if trainingData.isEmpty {
                        Text("No training data added yet")
                            .foregroundColor(.secondary)
                            .padding()
                    } else {
                        List {
                            ForEach(trainingData, id: \.input) { dataPoint in
                                VStack(alignment: .leading, spacing: 4) {
                                    Text("Input: \(dataPoint.input)")
                                        .font(.subheadline)
                                    Text("Output: \(dataPoint.expectedOutput)")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                            }
                        }
                        .frame(height: 200)
                    }
                }
                .padding()
                
                // Actions
                HStack(spacing: 16) {
                    Button("Start Fine-tuning") {
                        startFineTuning()
                    }
                    .disabled(trainingData.isEmpty || gitBot.isTraining)
                    .buttonStyle(.borderedProminent)
                    
                    if gitBot.isTraining {
                        ProgressView()
                        Text("Training in progress...")
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
                
                // Fine-tuning Jobs
                VStack(alignment: .leading, spacing: 8) {
                    Text("Recent Fine-tuning Jobs")
                        .font(.headline)
                    
                    if fineTuningJobs.isEmpty {
                        Text("No jobs yet")
                            .foregroundColor(.secondary)
                            .padding()
                    } else {
                        List(fineTuningJobs) { job in
                            FineTuningJobRow(job: job)
                        }
                        .frame(height: 150)
                    }
                }
                .padding()
                
                Spacer()
            }
            .sheet(isPresented: $isShowingDataInput) {
                DataInputSheet(trainingData: $trainingData)
            }
        }
    }
    
    private func startFineTuning() {
        Task {
            do {
                try await gitBot.startFineTuning(with: trainingData)
                
                await MainActor.run {
                    fineTuningJobs.append(FineTuningJobInfo(
                        model: selectedModel,
                        status: "Completed",
                        samples: trainingData.count
                    ))
                }
            } catch {
                print("Fine-tuning failed: \(error)")
            }
        }
    }
}

struct FineTuningJobInfo: Identifiable {
    let id = UUID()
    let model: String
    let status: String
    let samples: Int
    let timestamp = Date()
}

@available(macOS 13.0, *)
struct FineTuningJobRow: View {
    let job: FineTuningJobInfo
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(job.model)
                    .font(.headline)
                Text("\(job.samples) samples")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
            Text(job.status)
                .font(.caption)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(job.status == "Completed" ? Color.green.opacity(0.2) : Color.orange.opacity(0.2))
                .cornerRadius(8)
        }
    }
}

@available(macOS 13.0, *)
struct DataInputSheet: View {
    @Environment(\.dismiss) var dismiss
    @Binding var trainingData: [TrainingDataPoint]
    @State private var inputText = ""
    @State private var outputText = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section("Input") {
                    TextEditor(text: $inputText)
                        .frame(height: 100)
                }
                
                Section("Expected Output") {
                    TextEditor(text: $outputText)
                        .frame(height: 100)
                }
                
                Section {
                    Button("Add Training Sample") {
                        let dataPoint = TrainingDataPoint(
                            input: inputText,
                            expectedOutput: outputText
                        )
                        trainingData.append(dataPoint)
                        inputText = ""
                        outputText = ""
                        dismiss()
                    }
                    .disabled(inputText.isEmpty || outputText.isEmpty)
                }
            }
            .navigationTitle("Add Training Data")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
}

@available(macOS 13.0, *)
struct SettingsView: View {
    @EnvironmentObject var gitBot: ObservableGitBot
    @State private var apiKey = ""
    @State private var enableOnDeviceTraining = true
    @State private var modelCachePath = "~/Library/Caches/GitBot/Models"
    @State private var pythonPath = ""
    @State private var showingSaveAlert = false
    
    var body: some View {
        NavigationView {
            Form {
                Section("OpenAI Configuration") {
                    SecureField("API Key", text: $apiKey)
                        .textFieldStyle(.roundedBorder)
                    Text("Enter your OpenAI API key for external fine-tuning")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Section("Core ML Settings") {
                    Toggle("Enable On-Device Training", isOn: $enableOnDeviceTraining)
                    TextField("Model Cache Path", text: $modelCachePath)
                        .textFieldStyle(.roundedBorder)
                }
                
                Section("Python Integration") {
                    TextField("Python Environment Path", text: $pythonPath)
                        .textFieldStyle(.roundedBorder)
                    Text("Optional: Path to Python environment for advanced workflows")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Section {
                    Button("Save Settings") {
                        saveSettings()
                    }
                    .buttonStyle(.borderedProminent)
                }
            }
            .navigationTitle("Settings")
            .alert("Settings Saved", isPresented: $showingSaveAlert) {
                Button("OK", role: .cancel) { }
            }
        }
        .onAppear {
            loadSettings()
        }
    }
    
    private func loadSettings() {
        apiKey = gitBot.configuration.openAIAPIKey ?? ""
        enableOnDeviceTraining = gitBot.configuration.enableOnDeviceTraining
        modelCachePath = gitBot.configuration.modelCachePath
        pythonPath = gitBot.configuration.pythonEnvironmentPath ?? ""
    }
    
    private func saveSettings() {
        gitBot.configuration.openAIAPIKey = apiKey.isEmpty ? nil : apiKey
        gitBot.configuration.enableOnDeviceTraining = enableOnDeviceTraining
        gitBot.configuration.modelCachePath = modelCachePath
        gitBot.configuration.pythonEnvironmentPath = pythonPath.isEmpty ? nil : pythonPath
        
        showingSaveAlert = true
    }
}

#Preview {
    ContentView()
        .environmentObject(ObservableGitBot())
}

#else
// SwiftUI not available on this platform
// Use GitBotCore directly for command-line applications
#endif
