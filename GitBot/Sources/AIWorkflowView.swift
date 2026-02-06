import SwiftUI

struct AIWorkflowView: View {
    @State private var isRunningWorkflow = false
    @State private var selectedWorkflow = "Fine-tuning"
    @State private var workflowLog = "Ready to start AI workflow..."
    
    let workflows = ["Fine-tuning", "Training", "Core ML Conversion"]
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Workflow Selection
                GroupBox(label: Label("Select Workflow", systemImage: "list.bullet.rectangle")) {
                    Picker("Workflow Type", selection: $selectedWorkflow) {
                        ForEach(workflows, id: \.self) { workflow in
                            Text(workflow).tag(workflow)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding()
                }
                .padding(.horizontal)
                
                // Workflow Description
                GroupBox(label: Label("Description", systemImage: "info.circle")) {
                    Text(workflowDescription)
                        .font(.subheadline)
                        .padding()
                }
                .padding(.horizontal)
                
                // Run Button
                Button(action: runWorkflow) {
                    HStack {
                        if isRunningWorkflow {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle())
                                .scaleEffect(0.8)
                        } else {
                            Image(systemName: "play.fill")
                        }
                        Text(isRunningWorkflow ? "Running..." : "Run Workflow")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                }
                .buttonStyle(.borderedProminent)
                .disabled(isRunningWorkflow)
                .padding(.horizontal)
                
                // Workflow Log
                GroupBox(label: Label("Workflow Log", systemImage: "terminal")) {
                    ScrollView {
                        Text(workflowLog)
                            .font(.system(.body, design: .monospaced))
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding()
                    }
                    .frame(height: 200)
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .padding(.top)
            .navigationTitle("AI Workflows")
        }
    }
    
    var workflowDescription: String {
        switch selectedWorkflow {
        case "Fine-tuning":
            return "Fine-tune pre-trained models on your custom dataset. This workflow adapts existing models to your specific use case."
        case "Training":
            return "Train a new model from scratch using your dataset. This provides maximum control over the model architecture and training process."
        case "Core ML Conversion":
            return "Convert your trained PyTorch models to Core ML format for seamless integration with iOS and macOS applications."
        default:
            return "Select a workflow to get started."
        }
    }
    
    func runWorkflow() {
        isRunningWorkflow = true
        workflowLog = "Starting \(selectedWorkflow) workflow...\n"
        
        // Simulate workflow execution
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            workflowLog += "Loading configuration...\n"
            workflowLog += "Validating dependencies...\n"
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                workflowLog += "Executing workflow...\n"
                workflowLog += "✓ Workflow completed successfully!\n"
                workflowLog += "Output saved to: GitBot/Resources/\n"
                isRunningWorkflow = false
            }
        }
    }
}

struct AIWorkflowView_Previews: PreviewProvider {
    static var previews: some View {
        AIWorkflowView()
    }
}
