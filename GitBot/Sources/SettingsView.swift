import SwiftUI

struct SettingsView: View {
    @State private var pythonPath = "/usr/bin/python3"
    @State private var autoRunWorkflows = false
    @State private var showNotifications = true
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Python Configuration")) {
                    HStack {
                        Text("Python Path")
                        Spacer()
                        Text(pythonPath)
                            .foregroundColor(.secondary)
                            .lineLimit(1)
                            .truncationMode(.middle)
                    }
                    
                    Button("Detect Python") {
                        detectPythonPath()
                    }
                }
                
                Section(header: Text("Workflow Settings")) {
                    Toggle("Auto-run workflows on build", isOn: $autoRunWorkflows)
                    Toggle("Show notifications", isOn: $showNotifications)
                }
                
                Section(header: Text("AI Models")) {
                    NavigationLink(destination: Text("Model Manager")) {
                        HStack {
                            Image(systemName: "cube.box")
                            Text("Manage Models")
                        }
                    }
                    
                    NavigationLink(destination: Text("Training Data")) {
                        HStack {
                            Image(systemName: "doc.text")
                            Text("Training Data")
                        }
                    }
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                    
                    Button("View Documentation") {
                        // Open documentation
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
    
    func detectPythonPath() {
        // Simulate detecting Python installation
        let paths = [
            "/usr/bin/python3",
            "/usr/local/bin/python3",
            "/opt/homebrew/bin/python3"
        ]
        pythonPath = paths.first ?? "/usr/bin/python3"
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
}
