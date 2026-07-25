# ==========================================
# summarizer.py — Summarize article text using FLAN-T5, then translate to Russian
# ==========================================

from transformers import pipeline
from deep_translator import GoogleTranslator

# Load once globally (so it doesn't reload for every article)
summarizer = pipeline("summarization", model="google/flan-t5-small")


def translate_to_russian(text: str) -> str:
    """Translate any text to Russian. Falls back to original on failure."""
    if not text.strip():
        return text
    try:
        return GoogleTranslator(source="auto", target="ru").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def summarize_text(text: str, max_words: int = 60) -> str:
    """
    Generate a concise summary of the input text, translated to Russian.
    """
    if not text.strip():
        return "Нет содержания для суммаризации."

    max_input_length = 1000
    text = text[:max_input_length]

    try:
        result = summarizer(
            text,
            max_length=max_words,
            min_length=25,
            do_sample=False
        )
        summary_en = result[0]["summary_text"].strip()
    except Exception as e:
        print(f"Summarization error: {e}")
        summary_en = text[:200] + "..."

    return translate_to_russian(summary_en)
