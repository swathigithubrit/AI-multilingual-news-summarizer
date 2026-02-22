import os
import re
import time
from bs4 import BeautifulSoup
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gtts import gTTS
from deep_translator import GoogleTranslator

# ============================================================
# Summarizer pipeline
# ============================================================
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ============================================================
# Supported languages for UI and TTS
# ============================================================
supported_languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu"
}

# ============================================================
# Translate text to target language
# ============================================================
def translate_text(text, target_language):
    try:
        return GoogleTranslator(source="auto", target=target_language).translate(text)
    except Exception as e:
        print(f"[Warning] Translation failed: {e}")
        return text

# ============================================================
# Clean up input text before TTS
# ============================================================
def clean_text_for_tts(text):
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"\*|_|`|>|#+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ============================================================
# Convert text to speech and save as MP3
# ============================================================
def text_to_speech(text, lang, filename):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except Exception as e:
        print(f"[Warning] TTS generation failed for {filename}: {e}")

# ============================================================
# Robust summarization with safe handling
# ============================================================
def generate_summary(text, retries=2):
    text = text.strip()
    if not text:
        print("[INFO] Skipping summarization: empty text.")
        return "No content available to summarize."

    try:
        word_count = len(text.split())

        # Skip very short text (not meaningful)
        if word_count < 30:
            print("[INFO] Skipping summarization: text too short.")
            return "Insufficient content to summarize."

        # Limit text length to avoid model overflow
        if len(text) > 2000:
            text = text[:2000]

        max_len = min(130, max(30, int(word_count * 0.4)))

        for attempt in range(retries):
            try:
                result = summarizer(
                    text,
                    max_length=max_len,
                    min_length=30,
                    do_sample=False
                )
                return result[0]["summary_text"]
            except Exception as inner_e:
                print(f"[Warning] Summarization attempt {attempt + 1} failed: {inner_e}")
                time.sleep(1)

        print("[Warning] All summarization attempts failed.")
        return "Summary generation failed."

    except Exception as e:
        print(f"[Warning] Summary failed: {e}")
        return "Summary generation failed."

# ============================================================
# Sentiment analysis using NLTK Vader
# ============================================================
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    compound = score["compound"]
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# ============================================================
# Keyword/topic extraction
# ============================================================
def extract_topics(text):
    words = re.findall(r"\b\w+\b", text.lower())
    stop_words = {
        "the", "is", "at", "which", "on", "and", "a", "an", "in", "to", "of", "for", "with",
        "by", "about", "this", "from", "that", "as", "it", "are", "be", "has", "was",
        "but", "not", "have", "or", "their", "they", "will", "its", "more", "can"
    }
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    return sorted(list(set(keywords)))


# ============================================================
# Audio generation helper
# ============================================================
def generate_audio(text, lang_code, filepath):
    try:
        cleaned = clean_text_for_tts(text)
        translated = translate_text(cleaned, lang_code)
        if translated.strip():
            text_to_speech(translated, lang_code, filepath)
            return True
        else:
            print(f"[Warning] Empty translated text for audio at {filepath}")
    except Exception as e:
        print(f"[ERROR] Audio generation failed at {filepath}: {e}")
    return False
