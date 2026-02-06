//
//  CoreMLService.swift
//  GitBot
//
//  Core ML integration service for AI model operations
//

import Foundation
import CoreML

class CoreMLService: ObservableObject {
    static let shared = CoreMLService()
    
    @Published var loadedModels: [String: MLModel] = [:]
    @Published var modelPerformance: [String: ModelPerformance] = [:]
    @Published var isTraining: Bool = false
    
    private init() {
        // Initialize service
        setupDefaultPerformance()
    }
    
    // MARK: - Model Loading
    
    func loadModel(named name: String) async throws -> MLModel {
        // Check if model is already loaded
        if let model = loadedModels[name] {
            return model
        }
        
        // Try to load model from bundle or documents directory
        guard let modelURL = findModelURL(named: name) else {
            throw CoreMLError.modelNotFound(name)
        }
        
        do {
            let model = try MLModel(contentsOf: modelURL)
            await MainActor.run {
                self.loadedModels[name] = model
            }
            return model
        } catch {
            throw CoreMLError.loadingFailed(error)
        }
    }
    
    func unloadModel(named name: String) {
        loadedModels.removeValue(forKey: name)
    }
    
    func unloadAllModels() {
        loadedModels.removeAll()
    }
    
    private func findModelURL(named name: String) -> URL? {
        // First, try to find in bundle
        if let bundleURL = Bundle.main.url(forResource: name, withExtension: "mlmodelc") {
            return bundleURL
        }
        
        // Then, try in documents directory
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let modelPath = documentsPath.appendingPathComponent("\(name).mlmodelc")
        
        if FileManager.default.fileExists(atPath: modelPath.path) {
            return modelPath
        }
        
        return nil
    }
    
    // MARK: - Model Prediction
    
    func predict(modelName: String, input: MLFeatureProvider) async throws -> MLFeatureProvider {
        guard let model = loadedModels[modelName] else {
            // Try to load the model if not loaded
            let loadedModel = try await loadModel(named: modelName)
            return try loadedModel.prediction(from: input)
        }
        
        return try model.prediction(from: input)
    }
    
    // MARK: - Fine-Tuning Workflow
    
    func startFineTuning(
        modelName: String,
        trainingDataPath: String,
        configuration: FineTuningConfiguration
    ) async throws {
        guard !isTraining else {
            throw CoreMLError.trainingInProgress
        }
        
        await MainActor.run {
            self.isTraining = true
        }
        
        // This would call the Python fine-tuning script
        let scriptPath = getPythonScriptPath()
        let command = buildFineTuningCommand(
            scriptPath: scriptPath,
            modelName: modelName,
            dataPath: trainingDataPath,
            config: configuration
        )
        
        do {
            try await executePythonScript(command)
            
            // Update performance metrics after training
            await updatePerformanceMetrics(for: modelName)
            
            await MainActor.run {
                self.isTraining = false
            }
        } catch {
            await MainActor.run {
                self.isTraining = false
            }
            throw CoreMLError.trainingFailed(error)
        }
    }
    
    func stopFineTuning() {
        // Stop the training process
        isTraining = false
        // TODO: Implement actual process termination
    }
    
    private func getPythonScriptPath() -> String {
        // Get the path to the Python fine-tuning script
        let scriptsDirectory = FileManager.default.currentDirectoryPath + "/GitBot/AIScripts"
        return scriptsDirectory + "/fine_tune_model.py"
    }
    
    private func buildFineTuningCommand(
        scriptPath: String,
        modelName: String,
        dataPath: String,
        config: FineTuningConfiguration
    ) -> String {
        var command = "python3 \"\(scriptPath)\""
        command += " --model \"\(modelName)\""
        command += " --data \"\(dataPath)\""
        command += " --epochs \(config.epochs)"
        command += " --batch-size \(config.batchSize)"
        command += " --learning-rate \(config.learningRate)"
        
        if let outputPath = config.outputPath {
            command += " --output \"\(outputPath)\""
        }
        
        return command
    }
    
    private func executePythonScript(_ command: String) async throws {
        // Execute Python script using Process
        // This is a placeholder - actual implementation would use Process
        try await Task.sleep(nanoseconds: 2_000_000_000) // Simulate execution
    }
    
    // MARK: - Model Performance Tracking
    
    func updatePerformanceMetrics(for modelName: String) async {
        // Simulate fetching performance metrics
        let performance = ModelPerformance(
            accuracy: Double.random(in: 0.85...0.98),
            loss: Double.random(in: 0.02...0.15),
            f1Score: Double.random(in: 0.80...0.95),
            trainingTime: Double.random(in: 300...1800),
            lastUpdated: Date()
        )
        
        await MainActor.run {
            self.modelPerformance[modelName] = performance
        }
    }
    
    func getPerformance(for modelName: String) -> ModelPerformance? {
        return modelPerformance[modelName]
    }
    
    private func setupDefaultPerformance() {
        // Setup some default performance metrics for demo purposes
        modelPerformance["GPT-Code-Review"] = ModelPerformance(
            accuracy: 0.942,
            loss: 0.058,
            f1Score: 0.91,
            trainingTime: 1245.0,
            lastUpdated: Date().addingTimeInterval(-86400)
        )
        
        modelPerformance["CodeBERT-Analyzer"] = ModelPerformance(
            accuracy: 0.889,
            loss: 0.098,
            f1Score: 0.87,
            trainingTime: 892.0,
            lastUpdated: Date().addingTimeInterval(-172800)
        )
    }
    
    // MARK: - Model Management
    
    func listAvailableModels() -> [String] {
        var models: [String] = []
        
        // Check bundle for compiled models
        if let bundleModels = Bundle.main.urls(forResourcesWithExtension: "mlmodelc", subdirectory: nil) {
            models.append(contentsOf: bundleModels.map { $0.deletingPathExtension().lastPathComponent })
        }
        
        // Check documents directory
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        if let documentModels = try? FileManager.default.contentsOfDirectory(at: documentsPath, includingPropertiesForKeys: nil)
            .filter({ $0.pathExtension == "mlmodelc" }) {
            models.append(contentsOf: documentModels.map { $0.deletingPathExtension().lastPathComponent })
        }
        
        return Array(Set(models)) // Remove duplicates
    }
    
    func deleteModel(named name: String) throws {
        // Remove from loaded models
        unloadModel(named: name)
        
        // Delete from documents directory
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let modelPath = documentsPath.appendingPathComponent("\(name).mlmodelc")
        
        if FileManager.default.fileExists(atPath: modelPath.path) {
            try FileManager.default.removeItem(at: modelPath)
        }
        
        // Remove performance metrics
        modelPerformance.removeValue(forKey: name)
    }
}

// MARK: - Supporting Types

struct FineTuningConfiguration {
    var epochs: Int = 10
    var batchSize: Int = 32
    var learningRate: Double = 0.001
    var validationSplit: Double = 0.2
    var outputPath: String?
    
    static let `default` = FineTuningConfiguration()
}

struct ModelPerformance {
    let accuracy: Double
    let loss: Double
    let f1Score: Double
    let trainingTime: Double // in seconds
    let lastUpdated: Date
    
    var formattedAccuracy: String {
        String(format: "%.1f%%", accuracy * 100)
    }
    
    var formattedLoss: String {
        String(format: "%.3f", loss)
    }
    
    var formattedF1Score: String {
        String(format: "%.2f", f1Score)
    }
    
    var formattedTrainingTime: String {
        let hours = Int(trainingTime) / 3600
        let minutes = (Int(trainingTime) % 3600) / 60
        let seconds = Int(trainingTime) % 60
        
        if hours > 0 {
            return "\(hours)h \(minutes)m \(seconds)s"
        } else if minutes > 0 {
            return "\(minutes)m \(seconds)s"
        } else {
            return "\(seconds)s"
        }
    }
}

// MARK: - Core ML Errors

enum CoreMLError: Error, LocalizedError {
    case modelNotFound(String)
    case loadingFailed(Error)
    case predictionFailed(Error)
    case trainingInProgress
    case trainingFailed(Error)
    case invalidConfiguration
    
    var errorDescription: String? {
        switch self {
        case .modelNotFound(let name):
            return "Model not found: \(name)"
        case .loadingFailed(let error):
            return "Failed to load model: \(error.localizedDescription)"
        case .predictionFailed(let error):
            return "Prediction failed: \(error.localizedDescription)"
        case .trainingInProgress:
            return "A training session is already in progress"
        case .trainingFailed(let error):
            return "Training failed: \(error.localizedDescription)"
        case .invalidConfiguration:
            return "Invalid training configuration"
        }
    }
}
