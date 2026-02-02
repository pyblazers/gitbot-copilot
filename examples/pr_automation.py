"""Example: Automated PR merging with validation."""

from typing import Tuple
from gitbot.bot import GitBot
from gitbot.config import Config

# Initialize GitBot
config = Config()
bot = GitBot(config)


def can_merge_pr(pr_number: int) -> Tuple[bool, str]:
    """
    Check if a PR can be safely merged.
    
    Returns:
        Tuple of (can_merge: bool, reason: str)
    """
    # Get PR details
    pr = bot.pull_requests.get_pull_request(pr_number)
    
    # Check if PR is open
    if pr['state'] != 'open':
        return False, f"PR is {pr['state']}"
    
    # Check if already merged
    if pr['merged']:
        return False, "PR is already merged"
    
    # Check if mergeable
    if pr['mergeable'] is False:
        return False, "PR has merge conflicts"
    
    # Check mergeable state
    if pr['mergeable_state'] not in ['clean', 'unstable']:
        return False, f"PR mergeable state is {pr['mergeable_state']}"
    
    # Get reviews
    reviews = bot.pull_requests.get_pending_reviews(pr_number)
    
    # Check for approvals
    approved = any(review['state'] == 'APPROVED' for review in reviews)
    if not approved:
        return False, "PR has no approvals"
    
    # Check for requested changes
    changes_requested = any(review['state'] == 'CHANGES_REQUESTED' for review in reviews)
    if changes_requested:
        return False, "PR has requested changes"
    
    return True, "All checks passed"


# Example: List and merge eligible PRs
print("=== Checking Pull Requests for Auto-Merge ===\n")

prs = bot.pull_requests.list_pull_requests(state='open')

for pr in prs:
    pr_number = pr['number']
    print(f"Checking PR #{pr_number}: {pr['title']}")
    
    can_merge, reason = can_merge_pr(pr_number)
    
    if can_merge:
        print(f"  ✓ Can merge: {reason}")
        
        # Uncomment to actually merge
        # try:
        #     result = bot.pull_requests.merge_pull_request(
        #         pr_number=pr_number,
        #         merge_method='squash'
        #     )
        #     print(f"  ✓ Merged successfully: {result['sha']}")
        # except Exception as e:
        #     print(f"  ✗ Merge failed: {e}")
    else:
        print(f"  ✗ Cannot merge: {reason}")
    
    print()
