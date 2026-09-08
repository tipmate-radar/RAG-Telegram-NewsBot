from utils.rss_reader import fetch_new_articles, mark_as_sent
from utils.summarizer import summarize_text, translate_to_russian
from utils.telegram_bot import send_telegram_message
from utils.rag_store import add_summary_to_store

RUBRIC_LABELS = {"competitors": "🏁 Конкуренты", "tips_tax": "💰 Чаевые и платежи", "staff": "👥 Персонал"}


def main():
    print("Starting RAG Telegram Scheduler...\n")

    articles = fetch_new_articles()

    if not articles:
        print("No new articles found. Exiting.")
        return

    print(f"Found {len(articles)} new articles to process.\n")

    sent = 0
    for idx, article in enumerate(articles, 1):
        print(f"[{idx}] Summarizing: {article['title'][:80]}...")

        summary = summarize_text(article["summary"])

        if not summary:
            print(f"[{idx}] Skipped — empty or error summary.")
            mark_as_sent(article["link"])
            continue

        title_ru = translate_to_russian(article["title"])
        rubric = RUBRIC_LABELS.get(article["rubric"], "📰 Рынок")

        message = (
            f"{rubric}\n"
            f"<b>{title_ru}</b>\n\n"
            f"{summary}\n\n"
            f"🔗 {article['link']}"
        )

        send_telegram_message(message)
        mark_as_sent(article["link"])
        add_summary_to_store(article["title"], summary, article["link"])
        sent += 1

    print(f"\nDone. Sent: {sent} articles.")


if __name__ == "__main__":
    main()
