#!/usr/bin/env python3
"""Example: fetch hot posts from tech subreddits.

Usage:
    export REDDIT_CLIENT_ID=your_client_id
    export REDDIT_CLIENT_SECRET=your_client_secret
    python3 examples/fetch_tech_posts.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reddit_research import fetch_subreddit, search_reddit

SUBREDDITS = ["cscareerquestions", "layoffs", "technology", "programming"]
SEARCH_QUERIES = ["tech layoffs", "return to office", "AI replacing jobs"]


def main():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
        sys.exit(1)

    print("=== Hot posts from tech subreddits ===\n")
    for sub in SUBREDDITS:
        print(f"r/{sub}:")
        posts = fetch_subreddit(sub, mode="hot", limit=5,
                                client_id=client_id, client_secret=client_secret)
        for p in posts:
            print(f"  [{p['score']:>5}] {p['title'][:80]}")
        print()

    print("=== Search results ===\n")
    for query in SEARCH_QUERIES:
        print(f'Search: "{query}"')
        results = search_reddit(query, subreddits=["technology", "layoffs"], limit=3,
                                client_id=client_id, client_secret=client_secret)
        for p in results:
            print(f"  [{p['score']:>5}] r/{p['subreddit']}: {p['title'][:70]}")
        print()


if __name__ == "__main__":
    main()
