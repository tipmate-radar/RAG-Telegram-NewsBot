# ==========================================
# main.py — Orchestrates RSS → Summary → Telegram
# ==========================================

from utils.rss_reader import fetch_new_articles
from utils.summarizer import summarize_text, translate_to_russian
from utils.telegram_bot import send_telegram_message
from utils.rag_store import add_summary_to_store


def classify_rubric(article) -> str:
    text = (article.get("title", "") + " " + article.get("link", "")).lower()
    if any(k in text for k in [
        "tipjar", "tipsi", "globaltips", "global.tips", "edrixx", "sunday",
        "sipay", "sipos", "tipplus", "tipead", "tiepad",
        "tipsyou", "tap tiiip", "taptiiip", "tippie", "tackpay", "justtip"
    ]):
        return "🏁 Конкуренты"
    if any(k in text for k in ["staff", "turnover", "retention", "employee", "hiring", "personal", "rotación"]):
        return "👥 Персонал"
    if any(k in text for k in ["tax", "propina", "trinkgeld", "mancia", "pourboire", "irpf", "fiscal"]):
        return "💰 Налоги/чаевые"
    return "📰 Рынок"


def main():
    print("Starting RAG Telegram Scheduler...\n")

    # Step 1: Fetch new articles
    articles = fetch_new_articles()

    if not articles:
        print("No new articles found. Exiting.")
        return

    print(f"Found {len(articles)} new articles to process.\n")

    # Step 2: Process each article
    for idx, article in enumerate(articles, 1):
        print(f"[{idx}] Summarizing: {article['title'][:80]}...")
        summary = summarize_text(article["summary"])
        title_ru = translate_to_russian(article["title"])
        rubric = classify_rubric(article)

        # Step 3: Format Telegram message
        message = (
            f"{rubric}\n"
            f"<b>{title_ru}</b>\n\n"
            f"{summary}\n\n"
            f"🔗 {article['link']}"
        )

        # Step 4: Send to Telegram
        send_telegram_message(message)

        # Step 5: Store summary in RAG store
        add_summary_to_store(article["title"], summary, article["link"])

    print("\nAll new articles summarized and sent to Telegram!")


if __name__ == "__main__":
    main()
