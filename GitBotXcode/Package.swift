// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "GitBotXcode",
    platforms: [
        .macOS(.v13),
        .iOS(.v16)
    ],
    products: [
        .library(
            name: "GitBotCore",
            targets: ["GitBotCore"]),
        .library(
            name: "CoreMLModels",
            targets: ["CoreMLModels"]),
        .library(
            name: "OpenAIIntegration",
            targets: ["OpenAIIntegration"]),
        .library(
            name: "PythonBridge",
            targets: ["PythonBridge"])
    ],
    dependencies: [
        .package(url: "https://github.com/pvieito/PythonKit.git", branch: "master")
    ],
    targets: [
        .target(
            name: "GitBotCore",
            dependencies: []),
        .target(
            name: "CoreMLModels",
            dependencies: ["GitBotCore"]),
        .target(
            name: "OpenAIIntegration",
            dependencies: ["GitBotCore"]),
        .target(
            name: "PythonBridge",
            dependencies: ["GitBotCore", "PythonKit"]),
        .testTarget(
            name: "GitBotTests",
            dependencies: ["GitBotCore", "CoreMLModels", "OpenAIIntegration", "PythonBridge"])
    ]
)
