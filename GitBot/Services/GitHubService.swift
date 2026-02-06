//
//  GitHubService.swift
//  GitBot
//
//  GitHub API integration service
//

import Foundation

class GitHubService: ObservableObject {
    static let shared = GitHubService()
    
    // GitHub API base URL
    private let baseURL = "https://api.github.com"
    
    // Authentication token (placeholder - should be securely stored)
    @Published var authToken: String = ""
    @Published var isAuthenticated: Bool = false
    
    private init() {
        // Initialize with stored token if available
        loadAuthToken()
    }
    
    // MARK: - Authentication
    
    func authenticate(token: String) {
        self.authToken = token
        self.isAuthenticated = !token.isEmpty
        saveAuthToken(token)
    }
    
    func logout() {
        self.authToken = ""
        self.isAuthenticated = false
        clearAuthToken()
    }
    
    private func loadAuthToken() {
        // TODO: Load from Keychain
        // For now, using a placeholder
        if let token = UserDefaults.standard.string(forKey: "github_token") {
            self.authToken = token
            self.isAuthenticated = !token.isEmpty
        }
    }
    
    private func saveAuthToken(_ token: String) {
        // TODO: Save to Keychain for security
        UserDefaults.standard.set(token, forKey: "github_token")
    }
    
    private func clearAuthToken() {
        // TODO: Remove from Keychain
        UserDefaults.standard.removeObject(forKey: "github_token")
    }
    
    // MARK: - Repository Operations
    
    func fetchRepositories(username: String? = nil) async throws -> [Repository] {
        let endpoint = username != nil ? "/users/\(username!)/repos" : "/user/repos"
        return try await fetchData(endpoint: endpoint)
    }
    
    func searchRepositories(query: String) async throws -> [Repository] {
        let endpoint = "/search/repositories?q=\(query)"
        let response: SearchResponse<Repository> = try await fetchData(endpoint: endpoint)
        return response.items
    }
    
    func fetchRepository(owner: String, name: String) async throws -> Repository {
        let endpoint = "/repos/\(owner)/\(name)"
        return try await fetchData(endpoint: endpoint)
    }
    
    // MARK: - Issue Operations
    
    func fetchIssues(owner: String, repo: String, state: String = "open") async throws -> [Issue] {
        let endpoint = "/repos/\(owner)/\(repo)/issues?state=\(state)"
        return try await fetchData(endpoint: endpoint)
    }
    
    func createIssue(owner: String, repo: String, title: String, body: String) async throws -> Issue {
        let endpoint = "/repos/\(owner)/\(repo)/issues"
        let payload: [String: Any] = [
            "title": title,
            "body": body
        ]
        return try await postData(endpoint: endpoint, body: payload)
    }
    
    func updateIssue(owner: String, repo: String, issueNumber: Int, title: String?, body: String?, state: String?) async throws -> Issue {
        let endpoint = "/repos/\(owner)/\(repo)/issues/\(issueNumber)"
        var payload: [String: Any] = [:]
        if let title = title { payload["title"] = title }
        if let body = body { payload["body"] = body }
        if let state = state { payload["state"] = state }
        return try await patchData(endpoint: endpoint, body: payload)
    }
    
    // MARK: - Pull Request Operations
    
    func fetchPullRequests(owner: String, repo: String, state: String = "open") async throws -> [PullRequest] {
        let endpoint = "/repos/\(owner)/\(repo)/pulls?state=\(state)"
        return try await fetchData(endpoint: endpoint)
    }
    
    func searchCode(query: String) async throws -> [SearchResult] {
        let endpoint = "/search/code?q=\(query)"
        let response: SearchResponse<SearchResult> = try await fetchData(endpoint: endpoint)
        return response.items
    }
    
    // MARK: - Generic Network Methods
    
    private func fetchData<T: Decodable>(endpoint: String) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        addAuthHeaders(to: &request)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(statusCode: httpResponse.statusCode)
        }
        
        do {
            let decoder = JSONDecoder()
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingError(error)
        }
    }
    
    private func postData<T: Decodable>(endpoint: String, body: [String: Any]) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        addAuthHeaders(to: &request)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(statusCode: httpResponse.statusCode)
        }
        
        do {
            let decoder = JSONDecoder()
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingError(error)
        }
    }
    
    private func patchData<T: Decodable>(endpoint: String, body: [String: Any]) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        addAuthHeaders(to: &request)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(statusCode: httpResponse.statusCode)
        }
        
        do {
            let decoder = JSONDecoder()
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingError(error)
        }
    }
    
    private func addAuthHeaders(to request: inout URLRequest) {
        request.setValue("application/vnd.github.v3+json", forHTTPHeaderField: "Accept")
        if !authToken.isEmpty {
            request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        }
    }
}

// MARK: - Supporting Types

struct SearchResponse<T: Decodable>: Decodable {
    let items: [T]
    let totalCount: Int
    
    enum CodingKeys: String, CodingKey {
        case items
        case totalCount = "total_count"
    }
}

struct SearchResult: Identifiable, Decodable {
    let name: String
    let path: String
    let repository: Repository
    let htmlUrl: String
    
    var id: String { path }
    
    enum CodingKeys: String, CodingKey {
        case name, path, repository
        case htmlUrl = "html_url"
    }
}

// MARK: - Network Errors

enum NetworkError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int)
    case decodingError(Error)
    case unauthorized
    case rateLimitExceeded
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let statusCode):
            return "HTTP error with status code: \(statusCode)"
        case .decodingError(let error):
            return "Failed to decode response: \(error.localizedDescription)"
        case .unauthorized:
            return "Unauthorized - please check your authentication token"
        case .rateLimitExceeded:
            return "GitHub API rate limit exceeded"
        }
    }
}
