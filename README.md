# reddit-research-tool

Lightweight Reddit API client for content research. Uses Python stdlib only — no pip dependencies.

## Features

- OAuth2 client credentials flow (read-only, no user login required)
- Fetch hot / top / new posts from any subreddit
- Search Reddit by keyword, scoped to specific subreddits
- Rate-limit aware (stays under 100 req/min)
- Zero external dependencies (urllib, json, base64 only)

## Setup

```bash
git clone git@github.com:techcoldbrew/reddit-research-tool.git
cd reddit-research-tool

# Set credentials (get from reddit.com/prefs/apps)
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
```

## Usage

```python
from reddit_research import fetch_subreddit, search_reddit

# Fetch hot posts
posts = fetch_subreddit("cscareerquestions", mode="hot", limit=25)
for post in posts:
    print(f"[{post['score']}] {post['title']}")

# Search across subreddits
results = search_reddit(
    "tech layoffs 2026",
    subreddits=["technology", "layoffs", "cscareerquestions"],
    limit=10,
    timeframe="month",
)
```

## Post dict fields

| Field          | Description                        |
|----------------|------------------------------------|
| `title`        | Post title                         |
| `url`          | Reddit permalink                   |
| `external_url` | Linked URL (if not a text post)    |
| `subreddit`    | Subreddit name                     |
| `score`        | Upvotes                            |
| `comments`     | Comment count                      |
| `upvote_ratio` | Ratio of upvotes (0.0 - 1.0)       |
| `created_utc`  | Unix timestamp                     |
| `author`       | Post author username               |
| `flair`        | Post flair text                    |
| `selftext`     | Post body text (first 500 chars)   |

## Run the example

```bash
python3 examples/fetch_tech_posts.py
```

## Rate limits

Reddit free tier: 100 requests/minute. This client defaults to 0.7s delay between
subreddit scans (~85 req/min), staying safely under the limit.

## License

MIT
