# ==========================================
# summarizer.py — Summarize article text using FLAN-T5, then translate to Russian
# ==========================================

from transformers import pipeline
from deep_translator import GoogleTranslator

ERROR_MARKERS = ["error 500", "server error", "that's an error", "please try again", "403 forbidden", "404 not found", "access denied", "gateway timeout"]

summarizer = pipeline("summarization", model="google/flan-t5-small")


def is_error_text(text: str) -> bool:
    t = text.lower()
    return any(marker in t for marker in ERROR_MARKERS)


def translate_to_russian(text: str) -> str:
    if not text.strip():
        return text
    try:
        return GoogleTranslator(source="auto", target="ru").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def summarize_text(text: str, max_words: int = 60) -> str:
    if not text.strip() or is_error_text(text):
        return None

    text = text[:1000]

    try:
        result = summarizer(text, max_length=max_words, min_length=25, do_sample=False)
        summary_en = result[0]["summary_text"].strip()
    except Exception as e:
        print(f"Summarization error: {e}")
        if len(text) > 100:
            summary_en = text[:200] + "..."
        else:
            return None

    if is_error_text(summary_en):
        return None

    return translate_to_russian(summary_en)
