import SwiftUI

struct DashboardView: View {
    @State private var repositoryStatus = "Connected"
    @State private var lastSync = Date()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Repository Status Card
                    GroupBox(label: Label("Repository Status", systemImage: "folder.badge.gearshape")) {
                        VStack(alignment: .leading, spacing: 10) {
                            HStack {
                                Text("Status:")
                                    .fontWeight(.medium)
                                Spacer()
                                Text(repositoryStatus)
                                    .foregroundColor(.green)
                            }
                            
                            HStack {
                                Text("Last Sync:")
                                    .fontWeight(.medium)
                                Spacer()
                                Text(lastSync, style: .relative)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding()
                    }
                    .padding(.horizontal)
                    
                    // AI Models Card
                    GroupBox(label: Label("AI Models", systemImage: "brain")) {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Fine-tuned models ready for use")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                            
                            HStack {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                                Text("Core ML Model Available")
                            }
                        }
                        .padding()
                    }
                    .padding(.horizontal)
                    
                    // Quick Actions
                    GroupBox(label: Label("Quick Actions", systemImage: "bolt.fill")) {
                        VStack(spacing: 12) {
                            Button(action: {
                                // Action: Refresh data
                            }) {
                                HStack {
                                    Image(systemName: "arrow.clockwise")
                                    Text("Refresh Data")
                                    Spacer()
                                }
                            }
                            .buttonStyle(.bordered)
                            
                            Button(action: {
                                // Action: Run diagnostics
                            }) {
                                HStack {
                                    Image(systemName: "waveform.path.ecg")
                                    Text("Run Diagnostics")
                                    Spacer()
                                }
                            }
                            .buttonStyle(.bordered)
                        }
                        .padding()
                    }
                    .padding(.horizontal)
                    
                    Spacer()
                }
                .padding(.top)
            }
            .navigationTitle("GitBot Dashboard")
        }
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}
