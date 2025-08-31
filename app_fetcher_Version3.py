import feedparser

def fetch_rss(rss_url):
    feed = feedparser.parse(rss_url)
    apps = []
    for entry in feed.entries:
        apps.append({
            "title": entry.title,
            "desc": entry.summary,
            "link": entry.link,
            "src": "rss"
        })
    return apps