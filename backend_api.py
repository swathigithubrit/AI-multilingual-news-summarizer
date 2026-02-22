# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import os

# from utils import (
#     scrape_articles,
#     summarize_text,
#     get_sentiment,
#     analyze_sentiment_distribution,
#     summarize_all_articles,
#     text_to_speech,
#     supported_languages
# )

# app = FastAPI(title="News SummarEase API")

# # CORS configuration to allow access from frontend/Postman
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (for development)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Root endpoint for quick health check
# @app.get("/")
# def read_root():
#     return {"message": "✅ News SummarEase API is running!"}

# # Request models
# class CompanyRequest(BaseModel):
#     company: str

# class TTSRequest(BaseModel):
#     text: str
#     lang: str  # "en", "hi", "te", etc.

# # Endpoint: Scrape news articles
# @app.post("/scrape")
# def scrape_news(request: CompanyRequest):
#     try:
#         articles = scrape_articles(request.company)
#         return {"articles": articles}
#     except Exception as e:
#         return {"error": str(e)}

# # Endpoint: Summarize news articles
# @app.post("/summarize")
# def summarize_news(request: CompanyRequest):
#     try:
#         articles = scrape_articles(request.company)
#         summaries = [summarize_text(article['summary']) for article in articles]
#         return {"summaries": summaries}
#     except Exception as e:
#         return {"error": str(e)}

# # Endpoint: Perform sentiment analysis
# @app.post("/sentiment")
# def analyze_sentiments(request: CompanyRequest):
#     try:
#         articles = scrape_articles(request.company)
#         for article in articles:
#             article["sentiment"] = get_sentiment(article["summary"])
#         distribution = analyze_sentiment_distribution(articles)
#         return {
#             "sentiment_distribution": distribution,
#             "articles": articles
#         }
#     except Exception as e:
#         return {"error": str(e)}

# # Endpoint: Full pipeline – summarize + sentiment + combined summary
# @app.post("/full-report")
# def full_analysis(request: CompanyRequest):
#     try:
#         articles = scrape_articles(request.company)
#         for article in articles:
#             article["generated_summary"] = summarize_text(article["summary"])
#             article["sentiment"] = get_sentiment(article["generated_summary"])
#         combined_summary = summarize_all_articles(articles)
#         distribution = analyze_sentiment_distribution(articles)
#         return {
#             "combined_summary": combined_summary,
#             "sentiment_distribution": distribution,
#             "articles": articles
#         }
#     except Exception as e:
#         return {"error": str(e)}

# # Endpoint: Text to speech (TTS)
# @app.post("/tts")
# def generate_audio(request: TTSRequest):
#     try:
#         os.makedirs("static/audio", exist_ok=True)
#         filename = f"{request.lang}_summary.mp3"
#         path = f"static/audio/{filename}"
#         output_path = text_to_speech(request.text, request.lang, path)
#         return {"audio_file": output_path}
#     except Exception as e:
#         return {"error": str(e)}
