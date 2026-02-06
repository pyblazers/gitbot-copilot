//
//  GitBotApp.swift
//  GitBot
//
//  Main application entry point for GitBot
//

import SwiftUI

@main
struct GitBotApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowStyle(.hiddenTitleBar)
        .commands {
            CommandGroup(replacing: .newItem) { }
        }
    }
}
