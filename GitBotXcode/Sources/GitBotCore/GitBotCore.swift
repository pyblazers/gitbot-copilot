import Foundation

/// Core protocol for AI model adapters in GitBot
public protocol AIModelAdapter {
    associatedtype InputType
    associatedtype OutputType
    
    func predict(_ input: InputType) async throws -> OutputType
    func update(with trainingData: [TrainingDataPoint]) async throws
}

/// Represents a training data point for model updates
public struct TrainingDataPoint: Codable {
    public let input: String
    public let expectedOutput: String
    public let metadata: [String: String]
    
    public init(input: String, expectedOutput: String, metadata: [String: String] = [:]) {
        self.input = input
        self.expectedOutput = expectedOutput
        self.metadata = metadata
    }
}

/// GitBot configuration
public struct GitBotConfiguration: Codable {
    public var openAIAPIKey: String?
    public var enableOnDeviceTraining: Bool
    public var modelCachePath: String
    public var pythonEnvironmentPath: String?
    
    public init(
        openAIAPIKey: String? = nil,
        enableOnDeviceTraining: Bool = true,
        modelCachePath: String = "~/Library/Caches/GitBot/Models",
        pythonEnvironmentPath: String? = nil
    ) {
        self.openAIAPIKey = openAIAPIKey
        self.enableOnDeviceTraining = enableOnDeviceTraining
        self.modelCachePath = modelCachePath
        self.pythonEnvironmentPath = pythonEnvironmentPath
    }
}

/// Main GitBot coordinator
public class GitBot {
    public var configuration: GitBotConfiguration
    public var isTraining: Bool = false
    public var lastError: String?
    
    public init(configuration: GitBotConfiguration = GitBotConfiguration()) {
        self.configuration = configuration
    }
    
    public func processCommand(_ command: String) async -> String {
        // To be implemented by specific model adapters
        return "Command processed: \(command)"
    }
    
    public func startFineTuning(with data: [TrainingDataPoint]) async throws {
        isTraining = true
        defer { isTraining = false }
        
        // Fine-tuning logic to be implemented
        try await Task.sleep(nanoseconds: 1_000_000_000) // Simulate training
    }
}

/// Protocol for workflow management
public protocol WorkflowManager {
    func registerWorkflow(_ workflow: Workflow)
    func executeWorkflow(named: String) async throws
}

/// Represents a modular workflow
public struct Workflow: Identifiable {
    public let id: UUID
    public let name: String
    public let description: String
    public let execute: () async throws -> Void
    
    public init(name: String, description: String, execute: @escaping () async throws -> Void) {
        self.id = UUID()
        self.name = name
        self.description = description
        self.execute = execute
    }
}
