import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationSplitView {
            List {
                NavigationLink("Dashboard", destination: DashboardView())
                NavigationLink("Repositories", destination: RepositoriesView())
                NavigationLink("Fine-Tuning", destination: FineTuningView())
            }
            .navigationTitle("GitBot")
        } detail: {
            DashboardView()
        }
    }
}

struct DashboardView: View {
    var body: some View {
        VStack {
            Text("GitBot Dashboard")
                .font(.largeTitle)
                .padding()
            Text("Welcome to GitBot - Your AI-Powered GitHub Assistant")
                .foregroundColor(.secondary)
        }
    }
}

struct RepositoriesView: View {
    var body: some View {
        VStack {
            Text("Repositories")
                .font(.largeTitle)
            Text("GitHub repository management coming soon...")
                .foregroundColor(.secondary)
        }
    }
}

struct FineTuningView: View {
    var body: some View {
        VStack {
            Text("AI Fine-Tuning")
                .font(.largeTitle)
            Text("Model fine-tuning interface coming soon...")
                .foregroundColor(.secondary)
        }
    }
}

#Preview {
    ContentView()
}
