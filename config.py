# ===============================
# config.py — Project Configuration
# ===============================

import os
from dotenv import load_dotenv
load_dotenv()  # load variables from .env into os.environ

# -------------------------------
# 🔹 TELEGRAM BOT SETTINGS
# -------------------------------
# Create your Telegram bot using @BotFather and get the token
# Then get your chat ID using @userinfobot or via the bot API

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID_HERE")

# -------------------------------
# 🔹 RSS FEEDS TO TRACK
# -------------------------------
# Add as many RSS feeds as you like — you can mix news, blogs, etc.

RSS_FEEDS = [
    # Оригинальные источники (оставляем)
    "https://rss.mytimes.com/services/xml/rss/myt/Technology.xml",
    "https://news.google.com/rss?hl=en-IN&gl=IN&cid=IN:en",
    "https://www.theverge.com/rss/index.xml",
    
    # Испания (HoReCa, туризм, персонал)
    "https://www.hosteleriadeespana.es/feed",
    "https://www.segittur.es/feed",
    "https://www.ine.es/ine/rss/rss_turismo.xml",
    "https://www.gremirestauracio.cat/feed",
    "https://www.gremihotelsbcn.com/feed",
    
    # Европа (туризм, статистика)
    "https://www.unwto.org/rss",
    "https://ec.europa.eu/eurostat/rss",
    "https://sifted.eu/articles.rss",  # технологии Европы
    
    # Конкуренты
    "https://wearetipjar.com/blogs.rss",
    "https://www.tipsi.com/blog.rss",
    "https://www.globaltips.com/rss",
    
    # HR / персонал
    "https://www.hosteltur.com/rss/talento",
    "https://www.revfine.com/feed"
]

# -------------------------------
# 🔹 SYSTEM SETTINGS
# -------------------------------
# Number of new articles to summarize each run
MAX_ARTICLES_PER_RUN = 10

# Path to vector DB and cache files
CHROMA_DB_PATH = "./data/chroma"
CACHE_FILE = "./data/cache.json"
