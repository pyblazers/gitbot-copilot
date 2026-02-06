//
//  GitHubModel.swift
//  GitBot
//
//  Data models for GitHub entities
//

import Foundation

// MARK: - Repository Model
struct Repository: Identifiable, Codable {
    let id: Int
    let name: String
    let fullName: String
    let description: String?
    let stargazersCount: Int
    let forksCount: Int
    let language: String?
    let htmlUrl: String
    let updatedAt: String
    let isPrivate: Bool
    
    enum CodingKeys: String, CodingKey {
        case id, name, description, language
        case fullName = "full_name"
        case stargazersCount = "stargazers_count"
        case forksCount = "forks_count"
        case htmlUrl = "html_url"
        case updatedAt = "updated_at"
        case isPrivate = "private"
    }
}

// MARK: - Issue Model
struct Issue: Identifiable, Codable {
    let id: Int
    let number: Int
    let title: String
    let state: String
    let createdAt: String
    let updatedAt: String
    let body: String?
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case id, number, title, state, body, user
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Pull Request Model
struct PullRequest: Identifiable, Codable {
    let id: Int
    let number: Int
    let title: String
    let state: String
    let createdAt: String
    let updatedAt: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case id, number, title, state, user
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - User Model
struct User: Identifiable, Codable {
    let id: Int
    let login: String
    let avatarUrl: String
    
    enum CodingKeys: String, CodingKey {
        case id, login
        case avatarUrl = "avatar_url"
    }
}

// MARK: - Activity Model (for dashboard)
struct Activity: Identifiable {
    let id = UUID()
    let type: ActivityType
    let title: String
    let description: String
    let timestamp: Date
    
    enum ActivityType {
        case repositoryCreated
        case issueOpened
        case pullRequestMerged
        case commitPushed
        case fineTuningStarted
        case fineTuningCompleted
        
        var icon: String {
            switch self {
            case .repositoryCreated: return "folder.badge.plus"
            case .issueOpened: return "exclamationmark.circle"
            case .pullRequestMerged: return "arrow.triangle.merge"
            case .commitPushed: return "arrow.up.circle"
            case .fineTuningStarted: return "cpu"
            case .fineTuningCompleted: return "checkmark.circle"
            }
        }
        
        var color: String {
            switch self {
            case .repositoryCreated: return "blue"
            case .issueOpened: return "red"
            case .pullRequestMerged: return "purple"
            case .commitPushed: return "green"
            case .fineTuningStarted: return "orange"
            case .fineTuningCompleted: return "green"
            }
        }
    }
}

// MARK: - Statistics Model (for dashboard)
struct Statistics {
    var totalRepositories: Int = 0
    var openIssues: Int = 0
    var openPullRequests: Int = 0
    var completedFineTunings: Int = 0
}
