//
//  ContentView.swift
//  GitBot
//
//  Main content view with navigation sidebar
//

import SwiftUI

struct ContentView: View {
    @State private var selectedSection: NavigationSection = .dashboard
    
    enum NavigationSection {
        case dashboard
        case repositories
        case issues
        case pullRequests
        case fineTuning
    }
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(selection: $selectedSection) {
                Section("Main") {
                    NavigationLink(value: NavigationSection.dashboard) {
                        Label("Dashboard", systemImage: "square.grid.2x2")
                    }
                    NavigationLink(value: NavigationSection.repositories) {
                        Label("Repositories", systemImage: "folder")
                    }
                }
                
                Section("GitHub") {
                    NavigationLink(value: NavigationSection.issues) {
                        Label("Issues", systemImage: "exclamationmark.circle")
                    }
                    NavigationLink(value: NavigationSection.pullRequests) {
                        Label("Pull Requests", systemImage: "arrow.triangle.pull")
                    }
                }
                
                Section("AI") {
                    NavigationLink(value: NavigationSection.fineTuning) {
                        Label("Fine-Tuning", systemImage: "cpu")
                    }
                }
            }
            .navigationSplitViewColumnWidth(min: 200, ideal: 250)
            .listStyle(.sidebar)
        } detail: {
            // Main content area
            switch selectedSection {
            case .dashboard:
                DashboardView()
            case .repositories:
                RepositoryView()
            case .issues:
                PlaceholderView(title: "Issues", icon: "exclamationmark.circle")
            case .pullRequests:
                PlaceholderView(title: "Pull Requests", icon: "arrow.triangle.pull")
            case .fineTuning:
                FineTuningView()
            }
        }
        .frame(minWidth: 800, minHeight: 600)
    }
}

// Placeholder view for sections not yet implemented
struct PlaceholderView: View {
    let title: String
    let icon: String
    
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: icon)
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            Text(title)
                .font(.largeTitle)
                .fontWeight(.bold)
            Text("Coming soon...")
                .font(.title3)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

#Preview {
    ContentView()
}
