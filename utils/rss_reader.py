import feedparser
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from config import RSS_FEEDS, MAX_ARTICLES_PER_RUN

CACHE_FILE = "data/cache.json"

ENTRIES_PER_FEED = 15

RELEVANCE_KEYWORDS = ["hotel", "hoteles", "hostel", "restaurant", "restaurante", "café", "cafe", "bar", "spa", "salon", "salón", "hospitality", "horeca", "tourism", "turismo", "turístico", "staff", "employee", "personal", "camarero", "waiter", "barista", "housekeeping", "tip", "tips", "propina", "propinas", "trinkgeld", "mancia", "pourboire", "gratuity"]

COMPETITOR_DOMAINS = ["tipjar", "tipsi", "globaltips", "global.tips", "edrixx", "sunday", "wearetipjar", "sipay", "sipos", "tipplus", "tipead", "tiepad", "tipsyou", "taptiiip", "tippie", "tackpay", "justtip"]


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text()
    return re.sub(r'\s+', ' ', text).strip()


def is_relevant(title: str, summary: str, link: str) -> bool:
    text = f"{title} {summary} {link}".lower()
    if any(domain in text for domain in COMPETITOR_DOMAINS):
        return True
    return any(keyword in text for keyword in RELEVANCE_KEYWORDS)


def fetch_new_articles():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {"processed_links": []}

    candidates = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        total = len(feed.entries)
        kept = 0

        for entry in feed.entries[:ENTRIES_PER_FEED]:
            link = getattr(entry, "link", None)
            if not link or link in cache["processed_links"]:
                continue

            title = getattr(entry, "title", "")
            raw_summary = getattr(entry, "summary", "")
            summary = clean_html(raw_summary)

            if not is_relevant(title, summary, link):
                cache["processed_links"].append(link)
                continue

            candidates.append({
                "source": feed.feed.title if "title" in feed.feed else "Unknown Source",
                "title": title,
                "summary": summary,
                "link": link,
                "published": getattr(entry, "published", str(datetime.now())),
            })
            kept += 1

        print(f"Feed: {feed_url} | entries: {total} | relevant new: {kept}")

    selected = candidates[:MAX_ARTICLES_PER_RUN]

    for article in selected:
        cache["processed_links"].append(article["link"])

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"\nCandidates found: {len(candidates)} | selected this run: {len(selected)}")
    return selected
