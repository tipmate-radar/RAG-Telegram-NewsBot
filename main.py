# ==========================================
# main.py — Orchestrates RSS → Summary → Telegram
# ==========================================

from utils.rss_reader import fetch_new_articles
from utils.summarizer import summarize_text, translate_to_russian
from utils.telegram_bot import send_telegram_message
from utils.rag_store import add_summary_to_store

COMPETITOR_KEYWORDS = ["tipjar", "tipsi", "globaltips", "global.tips", "edrixx", "sunday", "sipay", "sipos", "tipplus", "tipead", "tiepad", "tipsyou", "tap tiiip", "taptiiip", "tippie", "tackpay", "justtip"]

STAFF_KEYWORDS = ["staff", "turnover", "retention", "employee", "hiring", "personal", "rotación"]

TAX_KEYWORDS = ["tax", "propina", "trinkgeld", "mancia", "pourboire", "irpf", "fiscal"]


def classify_rubric(article) -> str:
    text = (article.get("title", "") + " " + article.get("link", "")).lower()
    if any(k in text for k in COMPETITOR_KEYWORDS):
        return "🏁 Конкуренты"
    if any(k in text for k in STAFF_KEYWORDS):
        return "👥 Персонал"
    if any(k in text for k in TAX_KEYWORDS):
        return "💰 Налоги/чаевые"
    return "📰 Рынок"


def main():
    print("Starting RAG Telegram Scheduler...\n")

    articles = fetch_new_articles()

    if not articles:
        print("No new articles found. Exiting.")
        return

    print(f"Found {len(articles)} new articles to process.\n")

    for idx, article in enumerate(articles, 1):
        print(f"[{idx}] Summarizing: {article['title'][:80]}...")
        summary = summarize_text(article["summary"])
        title_ru = translate_to_russian(article["title"])
        rubric = classify_rubric(article)

        message = (
            f"{rubric}\n"
            f"<b>{title_ru}</b>\n\n"
            f"{summary}\n\n"
            f"🔗 {article['link']}"
        )

        send_telegram_message(message)
        add_summary_to_store(article["title"], summary, article["link"])

    print("\nAll new articles summarized and sent to Telegram!")


if __name__ == "__main__":
    main()
