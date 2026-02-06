//
//  RepositoryView.swift
//  GitBot
//
//  Repository browser view
//

import SwiftUI

struct RepositoryView: View {
    @StateObject private var githubService = GitHubService.shared
    @State private var repositories: [Repository] = []
    @State private var searchText = ""
    @State private var isLoading = false
    @State private var selectedRepository: Repository?
    
    var filteredRepositories: [Repository] {
        if searchText.isEmpty {
            return repositories
        }
        return repositories.filter { repo in
            repo.name.localizedCaseInsensitiveContains(searchText) ||
            (repo.description?.localizedCaseInsensitiveContains(searchText) ?? false)
        }
    }
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Repositories")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                Spacer()
                Button(action: loadRepositories) {
                    Label("Refresh", systemImage: "arrow.clockwise")
                }
                .disabled(isLoading)
            }
            .padding()
            
            // Search Bar
            HStack {
                Image(systemName: "magnifyingglass")
                    .foregroundColor(.secondary)
                TextField("Search repositories...", text: $searchText)
                    .textFieldStyle(.plain)
                if !searchText.isEmpty {
                    Button(action: { searchText = "" }) {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundColor(.secondary)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(8)
            .background(Color(nsColor: .controlBackgroundColor))
            .cornerRadius(8)
            .padding(.horizontal)
            
            Divider()
                .padding(.top)
            
            // Repository List
            if isLoading {
                ProgressView("Loading repositories...")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if filteredRepositories.isEmpty {
                VStack(spacing: 16) {
                    Image(systemName: "folder")
                        .font(.system(size: 60))
                        .foregroundColor(.secondary)
                    Text(repositories.isEmpty ? "No repositories found" : "No matching repositories")
                        .font(.title3)
                        .foregroundColor(.secondary)
                    if repositories.isEmpty {
                        Button("Load Repositories") {
                            loadRepositories()
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                ScrollView {
                    LazyVStack(spacing: 12) {
                        ForEach(filteredRepositories) { repo in
                            RepositoryCard(repository: repo)
                                .onTapGesture {
                                    selectedRepository = repo
                                }
                        }
                    }
                    .padding()
                }
            }
        }
        .onAppear {
            if repositories.isEmpty {
                loadRepositories()
            }
        }
    }
    
    private func loadRepositories() {
        isLoading = true
        
        // Simulate loading with placeholder data
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            repositories = [
                Repository(
                    id: 1,
                    name: "gitbot-copilot",
                    fullName: "pyblazers/gitbot-copilot",
                    description: "AI-powered GitHub assistant with SwiftUI interface",
                    stargazersCount: 42,
                    forksCount: 8,
                    language: "Swift",
                    htmlUrl: "https://github.com/pyblazers/gitbot-copilot",
                    updatedAt: "2024-01-15T10:30:00Z",
                    isPrivate: false
                ),
                Repository(
                    id: 2,
                    name: "ml-models",
                    fullName: "pyblazers/ml-models",
                    description: "Collection of fine-tuned ML models for code analysis",
                    stargazersCount: 156,
                    forksCount: 23,
                    language: "Python",
                    htmlUrl: "https://github.com/pyblazers/ml-models",
                    updatedAt: "2024-01-14T15:20:00Z",
                    isPrivate: false
                ),
                Repository(
                    id: 3,
                    name: "swiftui-components",
                    fullName: "pyblazers/swiftui-components",
                    description: "Reusable SwiftUI components library",
                    stargazersCount: 89,
                    forksCount: 12,
                    language: "Swift",
                    htmlUrl: "https://github.com/pyblazers/swiftui-components",
                    updatedAt: "2024-01-13T09:45:00Z",
                    isPrivate: false
                )
            ]
            isLoading = false
        }
    }
}

// MARK: - Repository Card Component
struct RepositoryCard: View {
    let repository: Repository
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header with name and privacy badge
            HStack {
                Text(repository.name)
                    .font(.headline)
                    .fontWeight(.semibold)
                
                if repository.isPrivate {
                    Label("Private", systemImage: "lock.fill")
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.orange.opacity(0.2))
                        .foregroundColor(.orange)
                        .cornerRadius(4)
                }
                
                Spacer()
            }
            
            // Description
            if let description = repository.description {
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            // Metadata
            HStack(spacing: 16) {
                if let language = repository.language {
                    HStack(spacing: 4) {
                        Circle()
                            .fill(languageColor(for: language))
                            .frame(width: 12, height: 12)
                        Text(language)
                            .font(.caption)
                    }
                }
                
                HStack(spacing: 4) {
                    Image(systemName: "star")
                        .font(.caption)
                    Text("\(repository.stargazersCount)")
                        .font(.caption)
                }
                
                HStack(spacing: 4) {
                    Image(systemName: "tuningfork")
                        .font(.caption)
                    Text("\(repository.forksCount)")
                        .font(.caption)
                }
                
                Spacer()
                
                Text("Updated \(formatDate(repository.updatedAt))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(nsColor: .controlBackgroundColor))
        .cornerRadius(8)
    }
    
    private func languageColor(for language: String) -> Color {
        switch language.lowercased() {
        case "swift": return .orange
        case "python": return .blue
        case "javascript": return .yellow
        case "typescript": return .blue
        case "java": return .red
        case "go": return .cyan
        default: return .gray
        }
    }
    
    private func formatDate(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: dateString) else {
            return "recently"
        }
        
        let relativeFormatter = RelativeDateTimeFormatter()
        relativeFormatter.unitsStyle = .abbreviated
        return relativeFormatter.localizedString(for: date, relativeTo: Date())
    }
}

#Preview {
    RepositoryView()
}
