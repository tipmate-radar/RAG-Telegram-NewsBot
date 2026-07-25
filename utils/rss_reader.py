import feedparser
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from config import RSS_FEEDS

CACHE_FILE = "data/cache.json"

# Отрасль гостеприимства в широком смысле — там, где потенциально есть персонал и чаевые
RELEVANCE_KEYWORDS = [
    "hotel", "hoteles", "hostel", "restaurant", "restaurante", "café", "cafe",
    "bar", "spa", "salon", "salón", "hospitality", "horeca", "tourism", "turismo",
    "turístico", "staff", "employee", "personal", "camarero", "waiter", "barista",
    "housekeeping", "tip", "tips", "propina", "propinas", "trinkgeld", "mancia",
    "pourboire", "gratuity",
]

# Домены конкурентов — релевантны всегда, даже без ключевых слов выше
COMPETITOR_DOMAINS = [
    "tipjar", "tipsi", "globaltips", "edrixx", "sunday", "wearetipjar",
]

MAX_ARTICLES_PER_RUN = 10  # общий лимит на один запуск


def clean_html(raw_html: str) -> str:
    """Remove HTML tags and entities from RSS summary."""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text()
    return re.sub(r'\s+', ' ', text).strip()


def is_relevant(title: str, summary: str, link: str) -> bool:
    text = f"{title} {summary} {link}".lower()
    if any(domain in text for domain in COMPETITOR_DOMAINS):
        return True
    return any(keyword in text for keyword in RELEVANCE_KEYWORDS)


def fetch_new_articles():
    # Load cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {"processed_links": []}

    new_articles = []
    for feed_url in RSS_FEEDS:
        print(f"Fetching feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # limit to 5 per feed
            link = entry.link
            if link in cache["processed_links"]:
                continue

            title = entry.title
            summary = clean_html(entry.summary)

            if not is_relevant(title, summary, link):
                cache["processed_links"].append(link)  # не показывать снова
                continue

            article = {
                "source": feed.feed.title if "title" in feed.feed else "Unknown Source",
                "title": title,
                "summary": summary,
                "link": link,
                "published": getattr(entry, "published", str(datetime.now())),
            }
            new_articles.append(article)
            cache["processed_links"].append(link)

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    return new_articles[:MAX_ARTICLES_PER_RUN]
