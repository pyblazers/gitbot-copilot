import XCTest
@testable import CoreMLModels

final class CoreMLIntegrationTests: XCTestCase {
    
    func testIssuePriorityEnum() {
        XCTAssertEqual(IssuePriority.critical.rawValue, "critical")
        XCTAssertEqual(IssuePriority.high.rawValue, "high")
        XCTAssertEqual(IssuePriority.medium.rawValue, "medium")
        XCTAssertEqual(IssuePriority.low.rawValue, "low")
    }
    
    func testCoreMLError() {
        let error = CoreMLError.modelNotLoaded
        XCTAssertNotNil(error)
    }
    
    #if canImport(CoreML) && canImport(NaturalLanguage)
    func testNLPTaskHandlerInitialization() {
        // Test that NLPTaskHandler can be initialized with a URL
        let tempURL = URL(fileURLWithPath: "/tmp/test.mlmodel")
        
        // This will fail in test but verifies the API
        XCTAssertThrowsError(try NLPTaskHandler(modelURL: tempURL))
    }
    
    func testCoreMLModelWrapperInitialization() {
        let tempURL = URL(fileURLWithPath: "/tmp/test.mlmodel")
        
        // This will fail in test but verifies the API
        XCTAssertThrowsError(try CoreMLModelWrapper(modelURL: tempURL))
    }
    #endif
}
