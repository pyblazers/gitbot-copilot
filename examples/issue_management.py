"""Example: Managing issues with GitBot."""

from gitbot.bot import GitBot
from gitbot.config import Config

# Initialize GitBot
config = Config()
bot = GitBot(config)

# Create a new issue
print("=== Creating New Issue ===")
new_issue = bot.issues.create_issue(
    title="Example Issue Created by GitBot",
    body="This is an example issue created by GitBot to demonstrate issue management features.",
    labels=["documentation", "example"],
    assignees=[]  # Add GitHub usernames here if needed
)
print(f"Created issue #{new_issue['number']}: {new_issue['title']}")
print(f"URL: {new_issue['url']}")

issue_number = new_issue['number']

# Add more labels to the issue
print(f"\n=== Adding Labels to Issue #{issue_number} ===")
updated_issue = bot.issues.add_labels(issue_number, ["enhancement"])
print(f"Labels: {', '.join(updated_issue['labels'])}")

# Assign users to the issue (replace with actual usernames)
# print(f"\n=== Assigning Issue #{issue_number} ===")
# assigned_issue = bot.issues.assign_issue(issue_number, ["username1", "username2"])
# print(f"Assignees: {', '.join(assigned_issue['assignees'])}")

# List all issues with specific label
print("\n=== Issues with 'documentation' Label ===")
doc_issues = bot.issues.list_issues(state='all', labels=["documentation"])
for issue in doc_issues[:10]:  # Show first 10
    print(f"#{issue['number']}: {issue['title']} ({issue['state']})")

# Close the issue
print(f"\n=== Closing Issue #{issue_number} ===")
closed_issue = bot.issues.close_issue(issue_number)
print(f"Issue #{closed_issue['number']} state: {closed_issue['state']}")
