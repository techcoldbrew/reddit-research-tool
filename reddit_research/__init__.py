"""reddit-research-tool - lightweight Reddit API client using stdlib only."""

from .client import RedditClient
from .fetch import fetch_subreddit, search_reddit

__all__ = ["RedditClient", "fetch_subreddit", "search_reddit"]
__version__ = "1.0.0"
