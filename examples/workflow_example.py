"""Example: Workflow automation."""

import asyncio
from gitbot.config.settings import Settings
from gitbot.ai.workflow_manager import WorkflowManager


async def main():
    """Workflow automation example."""
    
    settings = Settings()
    workflow_manager = WorkflowManager(settings)
    
    print("=== Workflow Automation Example ===\n")
    
    # Create a workflow for issue triage
    workflow_steps = [
        {
            "name": "analyze_issue",
            "type": "analyze",
            "content": "User login is broken after recent update",
            "analysis_type": "technical analysis"
        },
        {
            "name": "assign_task",
            "type": "assign",
            "task": "Fix login issue",
            "assignees": ["backend-team", "security-team", "frontend-team"]
        },
        {
            "name": "route_to_team",
            "type": "route",
            "request": "Critical login bug",
            "routes": ["backend", "frontend", "devops"]
        }
    ]
    
    # Create the workflow
    workflow = await workflow_manager.create_workflow("issue_triage", workflow_steps)
    print(f"Created workflow: {workflow['name']}\n")
    
    # Execute the workflow
    print("Executing workflow...")
    result = await workflow_manager.execute_workflow("issue_triage")
    print(f"Workflow result: {result}\n")
    
    # Link related queries
    print("Linking related queries...")
    queries = [
        "What is the status of the authentication feature?",
        "When will the security audit be completed?",
        "Are there any blockers for the release?"
    ]
    linked_result = await workflow_manager.link_queries(queries)
    print(f"Linked queries result: {linked_result}\n")
    
    print("=== Workflow example completed ===")


if __name__ == "__main__":
    asyncio.run(main())
