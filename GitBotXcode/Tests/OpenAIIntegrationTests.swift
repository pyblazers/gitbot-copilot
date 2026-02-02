import XCTest
@testable import OpenAIIntegration
@testable import GitBotCore

final class OpenAIIntegrationTests: XCTestCase {
    
    func testOpenAIClientInitialization() {
        let client = OpenAIClient(apiKey: "test-key")
        XCTAssertNotNil(client)
    }
    
    func testFineTuningHyperparameters() {
        let hyperparams = FineTuningHyperparameters(
            nEpochs: 3,
            batchSize: 8,
            learningRateMultiplier: 0.1
        )
        
        XCTAssertEqual(hyperparams.nEpochs, 3)
        XCTAssertEqual(hyperparams.batchSize, 8)
        XCTAssertEqual(hyperparams.learningRateMultiplier, 0.1)
        
        let dict = hyperparams.toDictionary()
        XCTAssertEqual(dict["n_epochs"] as? Int, 3)
        XCTAssertEqual(dict["batch_size"] as? Int, 8)
        XCTAssertEqual(dict["learning_rate_multiplier"] as? Double, 0.1)
    }
    
    func testTrainingDataFormatter() {
        let trainingData = [
            TrainingDataPoint(
                input: "How do I fix this bug?",
                expectedOutput: "You can fix it by...",
                metadata: [:]
            )
        ]
        
        let formatted = TrainingDataFormatter.formatForOpenAI(data: trainingData)
        XCTAssertTrue(formatted.contains("How do I fix this bug?"))
        XCTAssertTrue(formatted.contains("You can fix it by..."))
        XCTAssertTrue(formatted.contains("user"))
        XCTAssertTrue(formatted.contains("assistant"))
    }
    
    func testOpenAIError() {
        let error = OpenAIError.requestFailed
        XCTAssertNotNil(error)
    }
}
