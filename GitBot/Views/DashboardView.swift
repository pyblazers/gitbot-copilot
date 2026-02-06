//
//  DashboardView.swift
//  GitBot
//
//  Main dashboard view showing statistics and recent activity
//

import SwiftUI

struct DashboardView: View {
    @StateObject private var githubService = GitHubService.shared
    @State private var statistics = Statistics()
    @State private var recentActivities: [Activity] = []
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // Welcome Header
                VStack(alignment: .leading, spacing: 8) {
                    Text("Welcome to GitBot")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    Text("Your AI-powered GitHub companion")
                        .font(.title3)
                        .foregroundColor(.secondary)
                }
                .padding(.top, 20)
                
                // Statistics Cards
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 16) {
                    StatCard(
                        title: "Repositories",
                        value: "\(statistics.totalRepositories)",
                        icon: "folder",
                        color: .blue
                    )
                    StatCard(
                        title: "Open Issues",
                        value: "\(statistics.openIssues)",
                        icon: "exclamationmark.circle",
                        color: .red
                    )
                    StatCard(
                        title: "Pull Requests",
                        value: "\(statistics.openPullRequests)",
                        icon: "arrow.triangle.pull",
                        color: .purple
                    )
                    StatCard(
                        title: "Fine-Tunings",
                        value: "\(statistics.completedFineTunings)",
                        icon: "cpu",
                        color: .green
                    )
                }
                
                // Quick Actions
                VStack(alignment: .leading, spacing: 12) {
                    Text("Quick Actions")
                        .font(.title2)
                        .fontWeight(.semibold)
                    
                    HStack(spacing: 12) {
                        QuickActionButton(
                            title: "Search Repos",
                            icon: "magnifyingglass",
                            color: .blue
                        ) {
                            // Action
                        }
                        QuickActionButton(
                            title: "Create Issue",
                            icon: "plus.circle",
                            color: .orange
                        ) {
                            // Action
                        }
                        QuickActionButton(
                            title: "Start Fine-Tuning",
                            icon: "cpu",
                            color: .green
                        ) {
                            // Action
                        }
                    }
                }
                
                // Recent Activity Feed
                VStack(alignment: .leading, spacing: 12) {
                    Text("Recent Activity")
                        .font(.title2)
                        .fontWeight(.semibold)
                    
                    if recentActivities.isEmpty {
                        VStack(spacing: 12) {
                            Image(systemName: "clock")
                                .font(.system(size: 40))
                                .foregroundColor(.secondary)
                            Text("No recent activity")
                                .foregroundColor(.secondary)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 40)
                    } else {
                        ForEach(recentActivities) { activity in
                            ActivityRow(activity: activity)
                        }
                    }
                }
            }
            .padding(.horizontal, 32)
            .padding(.bottom, 32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .onAppear {
            loadDashboardData()
        }
    }
    
    private func loadDashboardData() {
        // Load placeholder statistics
        statistics = Statistics(
            totalRepositories: 12,
            openIssues: 8,
            openPullRequests: 3,
            completedFineTunings: 2
        )
        
        // Load placeholder recent activities
        recentActivities = [
            Activity(
                type: .repositoryCreated,
                title: "New Repository",
                description: "Created gitbot-copilot repository",
                timestamp: Date().addingTimeInterval(-3600)
            ),
            Activity(
                type: .fineTuningStarted,
                title: "Fine-Tuning Started",
                description: "Started fine-tuning GPT model for code review",
                timestamp: Date().addingTimeInterval(-7200)
            ),
            Activity(
                type: .pullRequestMerged,
                title: "Pull Request Merged",
                description: "Merged PR #42: Add new dashboard features",
                timestamp: Date().addingTimeInterval(-10800)
            )
        ]
    }
}

// MARK: - Stat Card Component
struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                Spacer()
            }
            Text(value)
                .font(.system(size: 32, weight: .bold))
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(nsColor: .controlBackgroundColor))
        .cornerRadius(12)
    }
}

// MARK: - Quick Action Button
struct QuickActionButton: View {
    let title: String
    let icon: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: icon)
                Text(title)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(color.opacity(0.1))
            .foregroundColor(color)
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Activity Row
struct ActivityRow: View {
    let activity: Activity
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: activity.type.icon)
                .font(.title3)
                .foregroundColor(colorForType(activity.type.color))
                .frame(width: 40, height: 40)
                .background(colorForType(activity.type.color).opacity(0.1))
                .cornerRadius(8)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(activity.title)
                    .font(.headline)
                Text(activity.description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text(formatTimestamp(activity.timestamp))
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(nsColor: .controlBackgroundColor))
        .cornerRadius(8)
    }
    
    private func colorForType(_ type: String) -> Color {
        switch type {
        case "blue": return .blue
        case "red": return .red
        case "purple": return .purple
        case "green": return .green
        case "orange": return .orange
        default: return .gray
        }
    }
    
    private func formatTimestamp(_ date: Date) -> String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: date, relativeTo: Date())
    }
}

#Preview {
    DashboardView()
}
