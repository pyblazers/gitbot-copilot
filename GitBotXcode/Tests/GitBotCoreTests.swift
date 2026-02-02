import XCTest
@testable import GitBotCore

final class GitBotCoreTests: XCTestCase {
    var gitBot: GitBot!
    
    override func setUp() {
        super.setUp()
        gitBot = GitBot()
    }
    
    override func tearDown() {
        gitBot = nil
        super.tearDown()
    }
    
    func testGitBotInitialization() {
        XCTAssertNotNil(gitBot)
        XCTAssertFalse(gitBot.isTraining)
        XCTAssertNil(gitBot.lastError)
    }
    
    func testProcessCommand() async {
        let result = await gitBot.processCommand("test command")
        XCTAssertTrue(result.contains("test command"))
    }
    
    func testTrainingDataPoint() {
        let dataPoint = TrainingDataPoint(
            input: "Fix bug in authentication",
            expectedOutput: "high",
            metadata: ["category": "bug"]
        )
        
        XCTAssertEqual(dataPoint.input, "Fix bug in authentication")
        XCTAssertEqual(dataPoint.expectedOutput, "high")
        XCTAssertEqual(dataPoint.metadata["category"], "bug")
    }
    
    func testWorkflow() async {
        var executed = false
        let workflow = Workflow(
            name: "Test Workflow",
            description: "A test workflow"
        ) {
            executed = true
        }
        
        XCTAssertEqual(workflow.name, "Test Workflow")
        
        try? await workflow.execute()
        XCTAssertTrue(executed)
    }
    
    func testGitBotConfiguration() {
        let config = GitBotConfiguration(
            openAIAPIKey: "test-key",
            enableOnDeviceTraining: true,
            modelCachePath: "/tmp/models"
        )
        
        XCTAssertEqual(config.openAIAPIKey, "test-key")
        XCTAssertTrue(config.enableOnDeviceTraining)
        XCTAssertEqual(config.modelCachePath, "/tmp/models")
    }
    
    func testFineTuning() async throws {
        let trainingData = [
            TrainingDataPoint(input: "Bug in login", expectedOutput: "high"),
            TrainingDataPoint(input: "Update documentation", expectedOutput: "low")
        ]
        
        XCTAssertFalse(gitBot.isTraining)
        
        // Start fine-tuning (non-blocking test)
        let expectation = self.expectation(description: "Fine-tuning completes")
        
        Task {
            try await gitBot.startFineTuning(with: trainingData)
            expectation.fulfill()
        }
        
        // Brief delay to check training state
        try await Task.sleep(nanoseconds: 100_000_000)
        // Note: isTraining might be true or false depending on timing
        
        await fulfillment(of: [expectation], timeout: 5.0)
        XCTAssertFalse(gitBot.isTraining)
    }
}
