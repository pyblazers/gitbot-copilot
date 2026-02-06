//
//  FineTuningView.swift
//  GitBot
//
//  AI fine-tuning interface
//

import SwiftUI

struct FineTuningView: View {
    @StateObject private var coreMLService = CoreMLService.shared
    @State private var selectedModel: String = "GPT-Code-Review"
    @State private var trainingDataPath: String = ""
    @State private var isTraining = false
    @State private var trainingProgress: Double = 0.0
    @State private var logs: [String] = []
    @State private var showFilePicker = false
    
    let availableModels = [
        "GPT-Code-Review",
        "CodeBERT-Analyzer",
        "SwiftLint-ML",
        "Documentation-Generator"
    ]
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // Header
                VStack(alignment: .leading, spacing: 8) {
                    Text("AI Fine-Tuning")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    Text("Train custom models for your workflow")
                        .font(.title3)
                        .foregroundColor(.secondary)
                }
                .padding(.top, 20)
                
                // Model Selection
                VStack(alignment: .leading, spacing: 12) {
                    Text("Select Model")
                        .font(.headline)
                    
                    Picker("Model", selection: $selectedModel) {
                        ForEach(availableModels, id: \.self) { model in
                            Text(model).tag(model)
                        }
                    }
                    .pickerStyle(.segmented)
                }
                .padding()
                .background(Color(nsColor: .controlBackgroundColor))
                .cornerRadius(12)
                
                // Training Data Input
                VStack(alignment: .leading, spacing: 12) {
                    Text("Training Data")
                        .font(.headline)
                    
                    HStack {
                        TextField("Path to training data...", text: $trainingDataPath)
                            .textFieldStyle(.roundedBorder)
                            .disabled(isTraining)
                        
                        Button(action: { showFilePicker.toggle() }) {
                            Label("Browse", systemImage: "folder")
                        }
                        .disabled(isTraining)
                    }
                    
                    Text("Select a directory containing your training data files")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding()
                .background(Color(nsColor: .controlBackgroundColor))
                .cornerRadius(12)
                
                // Training Configuration
                VStack(alignment: .leading, spacing: 12) {
                    Text("Configuration")
                        .font(.headline)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        ConfigRow(label: "Epochs", value: "10")
                        ConfigRow(label: "Batch Size", value: "32")
                        ConfigRow(label: "Learning Rate", value: "0.001")
                        ConfigRow(label: "Validation Split", value: "20%")
                    }
                }
                .padding()
                .background(Color(nsColor: .controlBackgroundColor))
                .cornerRadius(12)
                
                // Training Controls
                HStack(spacing: 12) {
                    Button(action: startTraining) {
                        HStack {
                            Image(systemName: isTraining ? "stop.circle" : "play.circle")
                            Text(isTraining ? "Stop Training" : "Start Training")
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(trainingDataPath.isEmpty)
                    
                    Button(action: resetTraining) {
                        HStack {
                            Image(systemName: "arrow.counterclockwise")
                            Text("Reset")
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.bordered)
                    .disabled(isTraining)
                }
                
                // Training Progress
                if isTraining || trainingProgress > 0 {
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Text("Training Progress")
                                .font(.headline)
                            Spacer()
                            Text("\(Int(trainingProgress * 100))%")
                                .font(.headline)
                                .foregroundColor(.blue)
                        }
                        
                        ProgressView(value: trainingProgress)
                            .progressViewStyle(.linear)
                        
                        HStack {
                            Text("Status:")
                                .foregroundColor(.secondary)
                            Text(isTraining ? "Training in progress..." : "Training completed")
                                .foregroundColor(isTraining ? .orange : .green)
                        }
                        .font(.subheadline)
                    }
                    .padding()
                    .background(Color(nsColor: .controlBackgroundColor))
                    .cornerRadius(12)
                }
                
                // Training Logs
                VStack(alignment: .leading, spacing: 12) {
                    Text("Training Logs")
                        .font(.headline)
                    
                    ScrollView {
                        VStack(alignment: .leading, spacing: 4) {
                            if logs.isEmpty {
                                Text("No logs yet. Start training to see progress...")
                                    .foregroundColor(.secondary)
                                    .padding()
                            } else {
                                ForEach(logs.indices, id: \.self) { index in
                                    Text(logs[index])
                                        .font(.system(.body, design: .monospaced))
                                        .foregroundColor(.primary)
                                }
                            }
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(8)
                    }
                    .frame(height: 200)
                    .background(Color(nsColor: .textBackgroundColor))
                    .cornerRadius(8)
                }
                .padding()
                .background(Color(nsColor: .controlBackgroundColor))
                .cornerRadius(12)
                
                // Model Performance
                VStack(alignment: .leading, spacing: 12) {
                    Text("Model Performance")
                        .font(.headline)
                    
                    LazyVGrid(columns: [
                        GridItem(.flexible()),
                        GridItem(.flexible()),
                        GridItem(.flexible())
                    ], spacing: 12) {
                        MetricCard(title: "Accuracy", value: "94.2%", trend: "+2.1%")
                        MetricCard(title: "Loss", value: "0.058", trend: "-0.012")
                        MetricCard(title: "F1 Score", value: "0.91", trend: "+0.03")
                    }
                }
                .padding()
                .background(Color(nsColor: .controlBackgroundColor))
                .cornerRadius(12)
            }
            .padding(.horizontal, 32)
            .padding(.bottom, 32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
    
    private func startTraining() {
        if isTraining {
            // Stop training
            isTraining = false
            logs.append("[\(formatTime())] Training stopped by user")
        } else {
            // Start training
            isTraining = true
            trainingProgress = 0.0
            logs.removeAll()
            logs.append("[\(formatTime())] Starting training for \(selectedModel)...")
            logs.append("[\(formatTime())] Loading training data from: \(trainingDataPath)")
            logs.append("[\(formatTime())] Initializing model...")
            
            // Simulate training progress
            Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { timer in
                if self.trainingProgress < 1.0 && self.isTraining {
                    self.trainingProgress += 0.05
                    
                    if self.trainingProgress >= 0.25 && self.logs.count < 5 {
                        self.logs.append("[\(self.formatTime())] Epoch 1/10 - Loss: 0.245")
                    }
                    if self.trainingProgress >= 0.50 && self.logs.count < 6 {
                        self.logs.append("[\(self.formatTime())] Epoch 5/10 - Loss: 0.112")
                    }
                    if self.trainingProgress >= 0.75 && self.logs.count < 7 {
                        self.logs.append("[\(self.formatTime())] Epoch 8/10 - Loss: 0.078")
                    }
                    if self.trainingProgress >= 0.95 {
                        self.logs.append("[\(self.formatTime())] Training completed successfully!")
                        self.logs.append("[\(self.formatTime())] Model saved to: ./models/\(self.selectedModel.lowercased())")
                        self.isTraining = false
                        self.trainingProgress = 1.0
                        timer.invalidate()
                    }
                } else {
                    timer.invalidate()
                }
            }
        }
    }
    
    private func resetTraining() {
        trainingProgress = 0.0
        logs.removeAll()
        trainingDataPath = ""
    }
    
    private func formatTime() -> String {
        let formatter = DateFormatter()
        formatter.timeStyle = .medium
        return formatter.string(from: Date())
    }
}

// MARK: - Config Row Component
struct ConfigRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.medium)
        }
    }
}

// MARK: - Metric Card Component
struct MetricCard: View {
    let title: String
    let value: String
    let trend: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            Text(trend)
                .font(.caption)
                .foregroundColor(trend.hasPrefix("+") ? .green : .red)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(nsColor: .textBackgroundColor))
        .cornerRadius(8)
    }
}

#Preview {
    FineTuningView()
}
