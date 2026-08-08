import feedparser
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from config import RSS_FEEDS, MAX_ARTICLES_PER_RUN

CACHE_FILE = "data/cache.json"
ENTRIES_PER_FEED = 25

COMPETITOR_DOMAINS = ["tipjar", "tipsi", "globaltips", "global.tips", "edrixx", "sunday", "wearetipjar", "sipay", "sipos", "tipplus", "tipead", "tiepad", "tipsyou", "taptiiip", "tippie", "tackpay", "justtip", "strikepay", "tiphaus", "kickfin"]

TIPS_TAX = ["propina", "propinas", "tipping", "trinkgeld", "mancia", "pourboire", "gratuity", "tronc", "irpf", "fiscalidad", "hacienda", "bizum", "pago digital", "pagos digitales", "cashless", "sin efectivo", "medios de pago"]

STAFF = ["rotación de personal", "turnover", "retención de talento", "fuga de talento", "falta de personal", "escasez de personal", "camarero", "camareros", "housekeeping", "convenio colectivo", "salarios hostelería", "contratación hostelería"]

QUOTAS = {"competitors": 10, "tips_tax": 8, "staff": 7}


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return re.sub(r'\s+', ' ', soup.get_text()).strip()


def classify(title, summary, link):
    text = f"{title} {summary} {link}".lower()
    if any(d in text for d in COMPETITOR_DOMAINS):
        return "competitors"
    if any(k in text for k in TIPS_TAX):
        return "tips_tax"
    if any(k in text for k in STAFF):
        return "staff"
    return None


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {"processed_links": []}


def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def fetch_new_articles():
    cache = load_cache()
    candidates = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        kept = 0

        for entry in feed.entries[:ENTRIES_PER_FEED]:
            link = getattr(entry, "link", None)
            if not link or link in cache["processed_links"]:
                continue

            title = getattr(entry, "title", "")
            summary = clean_html(getattr(entry, "summary", ""))
            rubric = classify(title, summary, link)

            if not rubric:
                cache["processed_links"].append(link)
                continue

            candidates.append({
                "source": feed.feed.title if "title" in feed.feed else "Unknown",
                "title": title,
                "summary": summary,
                "link": link,
                "published": getattr(entry, "published", str(datetime.now())),
                "rubric": rubric,
            })
            kept += 1

        print(f"Feed: {feed_url} | relevant new: {kept}")

    selected = []
    used = {k: 0 for k in QUOTAS}
    for a in candidates:
        if len(selected) >= MAX_ARTICLES_PER_RUN:
            break
        if used[a["rubric"]] < QUOTAS[a["rubric"]]:
            selected.append(a)
            used[a["rubric"]] += 1

    save_cache(cache)
    print(f"\nCandidates: {len(candidates)} | selected: {len(selected)} | by rubric: {used}")
    return selected


def mark_as_sent(link):
    cache = load_cache()
    if link not in cache["processed_links"]:
        cache["processed_links"].append(link)
        save_cache(cache)
