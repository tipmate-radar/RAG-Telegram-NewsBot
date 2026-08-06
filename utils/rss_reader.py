import feedparser
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from config import RSS_FEEDS, MAX_ARTICLES_PER_RUN

CACHE_FILE = "data/cache.json"

ENTRIES_PER_FEED = 25

# Высокий приоритет — прямо влияет на бизнес
PRIORITY_KEYWORDS = ["propina", "propinas", "tip", "tips", "tipping", "trinkgeld", "mancia", "pourboire", "gratuity", "tronc", "bizum", "pago digital", "pagos digitales", "cashless", "sin efectivo", "contactless", "qr", "wallet", "monedero", "rotación", "turnover", "retention", "fuga de talento", "falta de personal", "escasez de personal", "camarero", "camareros", "housekeeping", "salario", "convenio", "irpf", "fiscalidad", "hacienda"]

COMPETITOR_DOMAINS = ["tipjar", "tipsi", "globaltips", "global.tips", "edrixx", "sunday", "wearetipjar", "sipay", "sipos", "tipplus", "tipead", "tiepad", "tipsyou", "taptiiip", "tippie", "tackpay", "justtip", "strikepay", "tiphaus", "kickfin"]

# Низкий приоритет — отраслевой фон
CONTEXT_KEYWORDS = ["hotel", "hoteles", "hostelería", "restaurante", "restauración", "hospitality", "horeca", "turismo", "turístico", "spa", "bar", "cafetería"]

QUOTAS = {"competitors": 10, "staff": 6, "tips_tax": 6, "market": 8}


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return re.sub(r'\s+', ' ', soup.get_text()).strip()


def classify(title, summary, link):
    text = f"{title} {summary} {link}".lower()

    if any(d in text for d in COMPETITOR_DOMAINS):
        return "competitors", 3

    if any(k in text for k in ["propina", "tipping", "trinkgeld", "mancia", "pourboire", "tronc", "gratuity", "irpf", "fiscalidad", "hacienda", "bizum"]):
        return "tips_tax", 3

    if any(k in text for k in ["rotación", "turnover", "retention", "camarero", "housekeeping", "salario", "convenio", "falta de personal", "escasez de personal", "fuga de talento"]):
        return "staff", 2

    if any(k in text for k in PRIORITY_KEYWORDS):
        return "market", 2

    if any(k in text for k in CONTEXT_KEYWORDS):
        return "market", 1

    return None, 0


def fetch_new_articles():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {"processed_links": []}

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
            rubric, priority = classify(title, summary, link)

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
                "priority": priority,
            })
            kept += 1

        print(f"Feed: {feed_url} | relevant new: {kept}")

    candidates.sort(key=lambda a: -a["priority"])

    selected = []
    used = {k: 0 for k in QUOTAS}
    for a in candidates:
        if len(selected) >= MAX_ARTICLES_PER_RUN:
            break
        if used[a["rubric"]] < QUOTAS[a["rubric"]]:
            selected.append(a)
            used[a["rubric"]] += 1

    for a in selected:
        cache["processed_links"].append(a["link"])

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"\nCandidates: {len(candidates)} | selected: {len(selected)} | by rubric: {used}")
    return selected
