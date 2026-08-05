# ===============================
# config.py — Project Configuration
# ===============================
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# 🔹 TELEGRAM BOT SETTINGS
# -------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID_HERE")

# -------------------------------
# 🔹 RSS FEEDS TO TRACK
# -------------------------------
RSS_FEEDS = [
    # Испания — отрасль и туризм
    "https://www.hosteltur.com/feed",
    "https://www.hosteltur.com/feed/hoteles-y-alojamientos",
    "https://www.hosteltur.com/feed/economia",
    "https://www.segittur.es/feed",

    # Испания — ресторанный сегмент (адреса непроверенные, лог покажет)
    "https://restauracionnews.com/feed",
    "https://www.inforestauracion.com/feed",

    # Международный отраслевой
    "https://www.revfine.com/feed",

    # Конкуренты — прямые источники
    "https://tackpayapp.medium.com/feed",
    "https://www.wearetipjar.com/feed",

    # Конкуренты — Google News
    "https://news.google.com/rss/search?q=%22TiPJAR%22+tipping&hl=en-GB&gl=GB&ceid=GB:en",
    "https://news.google.com/rss/search?q=TackPay+mancia&hl=it&gl=IT&ceid=IT:it",
    "https://news.google.com/rss/search?q=TackPay+propinas+España&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=TackPay+funding+OR+raises&hl=en&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=JustTip+tipping+Ireland&hl=en-IE&gl=IE&ceid=IE:en",
    "https://news.google.com/rss/search?q=Tipsi+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=GlobalTips+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=eDrixx+trinkgeld&hl=de&gl=DE&ceid=DE:de",
    "https://news.google.com/rss/search?q=Sipay+Sipos+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=TipPlus+propinas&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=%22global.tips%22+OR+GlobalTips&hl=es&gl=ES&ceid=ES:es",
    "https://news.google.com/rss/search?q=TipsYou+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=%22Tap+Tiiip%22+pourboire&hl=fr&gl=FR&ceid=FR:fr",
    "https://news.google.com/rss/search?q=Tippie+Trinkgeld&hl=de&gl=DE&ceid=DE:de",
]

# -------------------------------
# 🔹 SYSTEM SETTINGS
# -------------------------------
MAX_ARTICLES_PER_RUN = 25

CHROMA_DB_PATH = "./data/chroma"
CACHE_FILE = "./data/cache.json"
