"""High-level fetch helpers - convenience wrappers around RedditClient."""

import os
import time
from .client import RedditClient

# Default subreddits for tech/career research
TECH_SUBREDDITS = [
    "cscareerquestions",
    "ExperiencedDevs",
    "layoffs",
    "antiwork",
    "recruitinghell",
    "programming",
    "technology",
    "sysadmin",
    "devops",
    "MachineLearning",
]


def _make_client(client_id: str = None, client_secret: str = None) -> RedditClient:
    """Create client from args or environment variables."""
    cid = client_id or os.environ.get("REDDIT_CLIENT_ID", "")
    csec = client_secret or os.environ.get("REDDIT_CLIENT_SECRET", "")
    if not cid or not csec:
        raise ValueError(
            "Reddit credentials required. Set REDDIT_CLIENT_ID and "
            "REDDIT_CLIENT_SECRET environment variables, or pass them directly."
        )
    return RedditClient(cid, csec)


def fetch_subreddit(
    subreddit: str,
    mode: str = "hot",
    limit: int = 25,
    timeframe: str = "week",
    client_id: str = None,
    client_secret: str = None,
) -> list:
    """Fetch posts from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
        mode: "hot", "top", or "new"
        limit: Number of posts (max 100)
        timeframe: For top mode - "hour"/"day"/"week"/"month"/"year"/"all"
        client_id: Reddit app client ID (or set REDDIT_CLIENT_ID env var)
        client_secret: Reddit app secret (or set REDDIT_CLIENT_SECRET env var)

    Returns:
        List of post dicts with title, url, score, comments, created_utc, etc.

    Example:
        posts = fetch_subreddit("cscareerquestions", mode="hot", limit=25)
        for post in posts:
            print(f"[{post['score']}] {post['title']}")
    """
    client = _make_client(client_id, client_secret)

    if mode == "top":
        return client.fetch_top(subreddit, limit=limit, timeframe=timeframe)
    elif mode == "new":
        return client.fetch_new(subreddit, limit=limit)
    else:
        return client.fetch_hot(subreddit, limit=limit)


def search_reddit(
    query: str,
    subreddits: list = None,
    limit: int = 10,
    sort: str = "relevance",
    timeframe: str = "month",
    client_id: str = None,
    client_secret: str = None,
    rate_limit_delay: float = 0.7,
) -> list:
    """Search Reddit for posts matching a query.

    Args:
        query: Search query string
        subreddits: List of subreddits to search (None = all of Reddit)
        limit: Posts per subreddit
        sort: "relevance", "hot", "top", "new", "comments"
        timeframe: "hour"/"day"/"week"/"month"/"year"/"all"
        client_id: Reddit app client ID
        client_secret: Reddit app secret
        rate_limit_delay: Seconds between requests (default 0.7 = ~85 req/min)

    Returns:
        List of post dicts

    Example:
        posts = search_reddit("tech layoffs 2026", subreddits=["technology", "layoffs"])
    """
    client = _make_client(client_id, client_secret)
    all_posts = []

    if subreddits:
        for sub in subreddits:
            results = client.search(query, subreddit=sub, limit=limit,
                                    sort=sort, timeframe=timeframe)
            all_posts.extend(results)
            if len(subreddits) > 1:
                time.sleep(rate_limit_delay)
    else:
        all_posts = client.search(query, limit=limit, sort=sort, timeframe=timeframe)

    return all_posts


def scan_tech_subreddits(
    client_id: str = None,
    client_secret: str = None,
    subreddits: list = None,
    limit: int = 25,
) -> list:
    """Scan default tech subreddits for hot posts.

    Fetches hot posts from each subreddit with rate limiting.
    Returns combined list of post dicts.
    """
    client = _make_client(client_id, client_secret)
    targets = subreddits or TECH_SUBREDDITS
    all_posts = []

    for sub in targets:
        posts = client.fetch_hot(sub, limit=limit)
        all_posts.extend(posts)
        time.sleep(0.7)  # Stay well under 100 req/min

    return all_posts
