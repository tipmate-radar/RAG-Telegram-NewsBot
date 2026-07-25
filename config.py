# ===============================
# config.py — Project Configuration
# ===============================
import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env into os.environ

# -------------------------------
# 🔹 TELEGRAM BOT SETTINGS
# -------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID_HERE")

# -------------------------------
# 🔹 RSS FEEDS TO TRACK
# -------------------------------
RSS_FEEDS = [
    # Испания (HoReCa, туризм, персонал)
    "https://www.hosteleriadeespana.es/feed",
    "https://www.segittur.es/feed",
    "https://www.ine.es/ine/rss/rss_turismo.xml",
    "https://www.gremirestauracio.cat/feed",
    "https://www.gremihotelsbcn.com/feed",

    # Европа (туризм, статистика)
    "https://www.unwto.org/rss",
    "https://ec.europa.eu/eurostat/rss",

    # Конкуренты — прямые блоги (могут быть пустыми, но не мешают)
    "https://wearetipjar.com/blogs.rss",
    "https://www.tipsi.com/blog.rss",
    "https://www.globaltips.com/rss",

    # Конкуренты — через Google News (более надёжный источник)
    "https://news.google.com/rss/search?q=%22TiPJAR%22+tipping&hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss/search?q=Tipsi+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=GlobalTips+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=eDrixx+trinkgeld&hl=de&gl=DE&ceid=DE:de",
    "https://news.google.com/rss/search?q=Sipay+Sipos+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=TipPlus+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=%22global.tips%22+OR+GlobalTips&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=TipsYou+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=%22Tap+Tiiip%22+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=Tippie+Trinkgeld&hl=de&gl=DE&ceid=DE:de",
    "https://news.google.com/rss/search?q=TackPay+mancia&hl=it&gl=IT&ceid=IT:it",
    "https://tackpayapp.medium.com/feed",

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
