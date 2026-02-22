import os
from flask import Blueprint, render_template, request
from tavily_scraper import scrape_articles
from utils import (
    generate_summary,
    analyze_sentiment,
    extract_topics,
    supported_languages,
    clean_text_for_tts,
    translate_text,
    text_to_speech
)


bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        company = request.form["company"]
        language = request.form["language"]
        lang_code = supported_languages.get(language, "en")

        articles = scrape_articles(company)
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        summaries = []
        kpi_mentions = {}

        skip_phrases = [
            "sign up", "click here", "allow notifications", "subscribe",
            "stay updated", "photo by", "image of", "may be an image",
            "see full image", "tap to view"
        ]

        for i, article in enumerate(articles):
            content = article.get("content", "").strip()

            if not content or len(content.split()) < 30 or any(phrase in content.lower() for phrase in skip_phrases):
                print(f"[INFO] Skipping article {i}: low-quality or image content.")
                continue

            # Generate summary and extract NLP outputs
            generated_summary = generate_summary(content)
            sentiment = analyze_sentiment(generated_summary)
            topics = extract_topics(generated_summary)
            sentiment_counts[sentiment] += 1

            

            # 🎧 Generate summary audio
            summary_audio_path = f"static/audio/{company}_summary_{i}_{lang_code}.mp3"
            cleaned_summary = clean_text_for_tts(generated_summary)
            translated_summary = translate_text(cleaned_summary, lang_code)
            if translated_summary.strip():
                text_to_speech(translated_summary, lang_code, summary_audio_path)
            else:
                print(f"[Warning] Empty translation for article {i}, skipping TTS.")

            summaries.append({
                "title": article["title"],
                "link": article["link"],
                "published": article.get("published", "Not Provided"),
                "original_content": content,
                "generated_summary": generated_summary,
                "sentiment": sentiment,
                "topics": topics,
                "audio_path": summary_audio_path
            })

        # 🧠 Generate final sentiment summary
        final_summary_input = " ".join([s["generated_summary"] for s in summaries])
        final_summary = generate_summary(final_summary_input) if final_summary_input.strip() else "No summary available."

        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        sentiment_text = (
            f"Final Sentiment Analysis Report for {company}. "
            f"Out of {sum(sentiment_counts.values())} articles, "
            f"{sentiment_counts['Positive']} are positive, "
            f"{sentiment_counts['Negative']} are negative, "
            f"and {sentiment_counts['Neutral']} are neutral. "
            f"Hence, the overall sentiment is {dominant_sentiment.lower()}."
        )

        # 🎧 Generate all audio outputs
        os.makedirs("static/audio", exist_ok=True)

        # Sentiment summary audio
        sentiment_audio_path = f"static/audio/{company}_sentiment_{lang_code}.mp3"
        cleaned_sentiment = clean_text_for_tts(sentiment_text)
        translated_sentiment = translate_text(cleaned_sentiment, lang_code)
        if translated_sentiment.strip():
            text_to_speech(translated_sentiment, lang_code, sentiment_audio_path)

        # Final summary audio
        final_summary_audio_path = f"static/audio/{company}_summary_{lang_code}.mp3"
        cleaned_final_summary = clean_text_for_tts(final_summary)
        translated_final_summary = translate_text(cleaned_final_summary, lang_code)
        if translated_final_summary.strip():
            text_to_speech(translated_final_summary, lang_code, final_summary_audio_path)

        # Full report audio
        full_report_text = f"{sentiment_text} Summary: {final_summary}"
        full_report_audio_path = f"static/audio/{company}_report_{lang_code}.mp3"
        cleaned_full_report = clean_text_for_tts(full_report_text)
        translated_full_report = translate_text(cleaned_full_report, lang_code)
        if translated_full_report.strip():
            text_to_speech(translated_full_report, lang_code, full_report_audio_path)

        return render_template(
            "index.html",
            company=company,
            sentiment_counts=sentiment_counts,
            summaries=summaries,
            final_summary=sentiment_text,
            overall_generated_summary=final_summary,
            audio_path=full_report_audio_path,
            final_summary_audio_path=final_summary_audio_path,
            sentiment_audio_path=sentiment_audio_path,
            languages=supported_languages,
            kpi_mentions=kpi_mentions
        )

    return render_template("index.html", languages=supported_languages)
