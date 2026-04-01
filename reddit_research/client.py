"""Reddit OAuth2 client - stdlib only (no pip dependencies)."""

import base64
import json
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OAUTH_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"
USER_AGENT = "reddit-research-tool/1.0 (research use)"
TIMEOUT = 15


class RedditClient:
    """Thin Reddit API client using client credentials OAuth2 flow.

    Usage:
        client = RedditClient(client_id="...", client_secret="...")
        posts = client.fetch_hot("cscareerquestions", limit=25)
    """

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._token_expiry = 0

    def _get_token(self) -> str:
        """Get or refresh OAuth2 access token."""
        if self._token and time.time() < self._token_expiry - 60:
            return self._token

        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        data = urlencode({"grant_type": "client_credentials"}).encode()
        req = Request(OAUTH_URL, data=data, headers={
            "User-Agent": USER_AGENT,
            "Authorization": f"Basic {credentials}",
        })

        with urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode())

        self._token = result["access_token"]
        self._token_expiry = time.time() + result.get("expires_in", 3600)
        return self._token

    def _get(self, path: str, params: dict = None) -> dict:
        """Authenticated GET request to Reddit API."""
        url = f"{API_BASE}{path}"
        if params:
            url += "?" + urlencode(params)

        req = Request(url, headers={
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self._get_token()}",
        })

        try:
            with urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode())
        except (URLError, json.JSONDecodeError):
            return {}

    def _parse_posts(self, data: dict, subreddit: str = "") -> list:
        """Extract post dicts from Reddit listing response."""
        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("stickied"):
                continue
            posts.append({
                "title": post.get("title", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "external_url": post.get("url", ""),
                "subreddit": post.get("subreddit", subreddit),
                "score": post.get("score", 0),
                "comments": post.get("num_comments", 0),
                "upvote_ratio": post.get("upvote_ratio", 0.0),
                "created_utc": int(post.get("created_utc", 0)),
                "author": post.get("author", ""),
                "flair": post.get("link_flair_text", ""),
                "selftext": post.get("selftext", "")[:500],
            })
        return posts

    def fetch_hot(self, subreddit: str, limit: int = 25) -> list:
        """Fetch hot posts from a subreddit."""
        data = self._get(f"/r/{subreddit}/hot", {"limit": limit})
        return self._parse_posts(data, subreddit)

    def fetch_top(self, subreddit: str, limit: int = 25, timeframe: str = "week") -> list:
        """Fetch top posts from a subreddit. timeframe: hour/day/week/month/year/all"""
        data = self._get(f"/r/{subreddit}/top", {"limit": limit, "t": timeframe})
        return self._parse_posts(data, subreddit)

    def fetch_new(self, subreddit: str, limit: int = 25) -> list:
        """Fetch newest posts from a subreddit."""
        data = self._get(f"/r/{subreddit}/new", {"limit": limit})
        return self._parse_posts(data, subreddit)

    def search(self, query: str, subreddit: str = None, limit: int = 25,
               sort: str = "relevance", timeframe: str = "month") -> list:
        """Search Reddit posts. If subreddit given, scoped to that sub."""
        path = f"/r/{subreddit}/search" if subreddit else "/search"
        data = self._get(path, {
            "q": query,
            "limit": limit,
            "sort": sort,
            "t": timeframe,
            "restrict_sr": "true" if subreddit else "false",
            "type": "link",
        })
        return self._parse_posts(data, subreddit or "")
