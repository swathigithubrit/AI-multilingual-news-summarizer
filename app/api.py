from tavily_scraper import scrape_articles
from utils import generate_summary, analyze_sentiment
import nltk

nltk.download('vader_lexicon')

def get_news_data(company_name):
    try:
        articles = scrape_articles(company_name)

        all_text = " ".join([article.get("content", "") for article in articles])
        overall_generated_summary = generate_summary(all_text)

        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for article in articles:
            content = article.get("content", "")
            sentiment = analyze_sentiment(content)
            article["sentiment"] = sentiment
            article["generated_summary"] = generate_summary(content)
            sentiment_counts[sentiment] += 1

        final_summary = f"Overall news coverage shows a generally {max(sentiment_counts, key=sentiment_counts.get).lower()} sentiment towards the company."

        return {
            "articles": articles,
            "overall_generated_summary": overall_generated_summary,
            "sentiment_counts": sentiment_counts,
            "final_summary": final_summary
        }

    except Exception as e:
        print(f"[ERROR] Failed to process news data: {e}")
        return {
            "articles": [],
            "overall_generated_summary": "",
            "sentiment_counts": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "final_summary": "Failed to analyze news data."
        }
