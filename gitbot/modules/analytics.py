"""
Repository Analytics Module
"""

from datetime import datetime, timedelta


class RepositoryAnalytics:
    """
    Provides repository analytics and statistics
    """

    def __init__(self, github_client, repository=None):
        """
        Initialize RepositoryAnalytics

        Args:
            github_client: GitHub client instance
            repository: Repository object
        """
        self.github_client = github_client
        self.repo = repository

    def set_repository(self, repository):
        """
        Set or change the repository

        Args:
            repository: Repository object
        """
        self.repo = repository

    def get_basic_stats(self):
        """
        Get basic repository statistics

        Returns:
            dict: Repository statistics
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        return {
            "name": self.repo.name,
            "full_name": self.repo.full_name,
            "description": self.repo.description,
            "stars": self.repo.stargazers_count,
            "forks": self.repo.forks_count,
            "watchers": self.repo.watchers_count,
            "open_issues": self.repo.open_issues_count,
            "size": self.repo.size,
            "language": self.repo.language,
            "default_branch": self.repo.default_branch,
            "created_at": self.repo.created_at.isoformat(),
            "updated_at": self.repo.updated_at.isoformat(),
            "pushed_at": self.repo.pushed_at.isoformat(),
            "url": self.repo.html_url,
        }

    def get_commit_stats(self, since_days=30):
        """
        Get commit statistics

        Args:
            since_days (int): Number of days to look back

        Returns:
            dict: Commit statistics
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        since = datetime.now() - timedelta(days=since_days)
        commits = list(self.repo.get_commits(since=since))
        
        # Count commits by author
        authors = {}
        for commit in commits:
            if commit.author:
                author = commit.author.login
                authors[author] = authors.get(author, 0) + 1

        return {
            "total_commits": len(commits),
            "since_days": since_days,
            "commits_by_author": authors,
            "most_active_author": max(authors.items(), key=lambda x: x[1])[0] if authors else None,
        }

    def get_contributor_stats(self):
        """
        Get contributor statistics

        Returns:
            list: List of contributors with their statistics
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        contributors = []
        for contributor in self.repo.get_contributors():
            contributors.append({
                "login": contributor.login,
                "contributions": contributor.contributions,
                "avatar_url": contributor.avatar_url,
                "profile_url": contributor.html_url,
            })
        
        return contributors

    def get_recent_activity(self, limit=10):
        """
        Get recent repository activity

        Args:
            limit (int): Number of recent events to retrieve

        Returns:
            dict: Recent activity information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        activity = {
            "recent_commits": [],
            "recent_issues": [],
            "recent_pull_requests": [],
        }

        # Recent commits
        for commit in self.repo.get_commits()[:limit]:
            activity["recent_commits"].append({
                "sha": commit.sha[:7],
                "message": commit.commit.message.split('\n')[0],
                "author": commit.author.login if commit.author else "Unknown",
                "date": commit.commit.author.date.isoformat(),
                "url": commit.html_url,
            })

        # Recent issues
        for issue in self.repo.get_issues(state="all", sort="updated")[:limit]:
            if not issue.pull_request:
                activity["recent_issues"].append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "user": issue.user.login,
                    "updated_at": issue.updated_at.isoformat(),
                    "url": issue.html_url,
                })

        # Recent pull requests
        for pr in self.repo.get_pulls(state="all", sort="updated")[:limit]:
            activity["recent_pull_requests"].append({
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "user": pr.user.login,
                "updated_at": pr.updated_at.isoformat(),
                "url": pr.html_url,
            })

        return activity

    def get_language_stats(self):
        """
        Get programming language statistics

        Returns:
            dict: Language usage statistics
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        languages = self.repo.get_languages()
        total_bytes = sum(languages.values())

        language_stats = {}
        for lang, bytes_count in languages.items():
            percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
            language_stats[lang] = {
                "bytes": bytes_count,
                "percentage": round(percentage, 2),
            }

        return language_stats

    def get_release_stats(self):
        """
        Get release statistics

        Returns:
            dict: Release information
        """
        if not self.repo:
            raise ValueError("Repository not set. Use set_repository() first.")

        releases = []
        for release in self.repo.get_releases():
            releases.append({
                "tag_name": release.tag_name,
                "name": release.title,
                "draft": release.draft,
                "prerelease": release.prerelease,
                "created_at": release.created_at.isoformat(),
                "published_at": release.published_at.isoformat() if release.published_at else None,
                "url": release.html_url,
            })

        return {
            "total_releases": len(releases),
            "releases": releases[:10],  # Return last 10 releases
        }
