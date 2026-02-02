import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif
import GitBotCore

/// OpenAI API client for fine-tuning and completions
public class OpenAIClient {
    private let apiKey: String
    private let baseURL = "https://api.openai.com/v1"
    private let session: URLSession
    
    public init(apiKey: String) {
        self.apiKey = apiKey
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 60
        self.session = URLSession(configuration: config)
    }
    
    /// Create a fine-tuning job
    public func createFineTuningJob(
        trainingFileId: String,
        model: String = "gpt-3.5-turbo",
        hyperparameters: FineTuningHyperparameters? = nil
    ) async throws -> FineTuningJob {
        let url = URL(string: "\(baseURL)/fine_tuning/jobs")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "training_file": trainingFileId,
            "model": model,
            "hyperparameters": hyperparameters?.toDictionary() ?? [:]
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OpenAIError.requestFailed
        }
        
        return try JSONDecoder().decode(FineTuningJob.self, from: data)
    }
    
    /// Upload training data file
    public func uploadFile(data: Data, purpose: String = "fine-tune") async throws -> FileUploadResponse {
        let url = URL(string: "\(baseURL)/files")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"purpose\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(purpose)\r\n".data(using: .utf8)!)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"training.jsonl\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/json\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (responseData, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OpenAIError.uploadFailed
        }
        
        return try JSONDecoder().decode(FileUploadResponse.self, from: responseData)
    }
    
    /// Get status of a fine-tuning job
    public func getFineTuningJob(id: String) async throws -> FineTuningJob {
        let url = URL(string: "\(baseURL)/fine_tuning/jobs/\(id)")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OpenAIError.requestFailed
        }
        
        return try JSONDecoder().decode(FineTuningJob.self, from: data)
    }
    
    /// Send completion request
    public func createCompletion(prompt: String, model: String = "gpt-3.5-turbo") async throws -> String {
        let url = URL(string: "\(baseURL)/chat/completions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "model": model,
            "messages": [
                ["role": "user", "content": prompt]
            ]
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OpenAIError.requestFailed
        }
        
        let completion = try JSONDecoder().decode(ChatCompletion.self, from: data)
        return completion.choices.first?.message.content ?? ""
    }
    
    /// Cancel a fine-tuning job
    public func cancelFineTuningJob(id: String) async throws {
        let url = URL(string: "\(baseURL)/fine_tuning/jobs/\(id)/cancel")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        
        let (_, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OpenAIError.requestFailed
        }
    }
}

/// Fine-tuning hyperparameters
public struct FineTuningHyperparameters: Codable {
    public var nEpochs: Int?
    public var batchSize: Int?
    public var learningRateMultiplier: Double?
    
    public init(nEpochs: Int? = nil, batchSize: Int? = nil, learningRateMultiplier: Double? = nil) {
        self.nEpochs = nEpochs
        self.batchSize = batchSize
        self.learningRateMultiplier = learningRateMultiplier
    }
    
    func toDictionary() -> [String: Any] {
        var dict: [String: Any] = [:]
        if let nEpochs = nEpochs { dict["n_epochs"] = nEpochs }
        if let batchSize = batchSize { dict["batch_size"] = batchSize }
        if let learningRateMultiplier = learningRateMultiplier {
            dict["learning_rate_multiplier"] = learningRateMultiplier
        }
        return dict
    }
}

/// Fine-tuning job response
public struct FineTuningJob: Codable {
    public let id: String
    public let object: String
    public let model: String
    public let createdAt: Int
    public let finishedAt: Int?
    public let fineTunedModel: String?
    public let status: String
    public let hyperparameters: Hyperparameters?
    
    enum CodingKeys: String, CodingKey {
        case id, object, model, status, hyperparameters
        case createdAt = "created_at"
        case finishedAt = "finished_at"
        case fineTunedModel = "fine_tuned_model"
    }
    
    public struct Hyperparameters: Codable {
        public let nEpochs: Int
        
        enum CodingKeys: String, CodingKey {
            case nEpochs = "n_epochs"
        }
    }
}

/// File upload response
public struct FileUploadResponse: Codable {
    public let id: String
    public let object: String
    public let bytes: Int
    public let createdAt: Int
    public let filename: String
    public let purpose: String
    
    enum CodingKeys: String, CodingKey {
        case id, object, bytes, filename, purpose
        case createdAt = "created_at"
    }
}

/// Chat completion response
public struct ChatCompletion: Codable {
    public let id: String
    public let object: String
    public let created: Int
    public let model: String
    public let choices: [Choice]
    
    public struct Choice: Codable {
        public let index: Int
        public let message: Message
        public let finishReason: String?
        
        enum CodingKeys: String, CodingKey {
            case index, message
            case finishReason = "finish_reason"
        }
    }
    
    public struct Message: Codable {
        public let role: String
        public let content: String
    }
}

/// OpenAI errors
public enum OpenAIError: Error {
    case requestFailed
    case uploadFailed
    case invalidResponse
    case authenticationFailed
}

/// Training data formatter for OpenAI
public class TrainingDataFormatter {
    public static func formatForOpenAI(data: [TrainingDataPoint]) -> String {
        var jsonl = ""
        
        for dataPoint in data {
            let entry: [String: Any] = [
                "messages": [
                    ["role": "user", "content": dataPoint.input],
                    ["role": "assistant", "content": dataPoint.expectedOutput]
                ]
            ]
            
            if let jsonData = try? JSONSerialization.data(withJSONObject: entry),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                jsonl += jsonString + "\n"
            }
        }
        
        return jsonl
    }
}
