AI-Powered Multilingual News Summarizer & Sentiment Insight Tool
Overview
This project is an AI-driven web application that fetches real-time company-related news articles, generates intelligent summaries, performs sentiment analysis, extracts business insights, and converts results into multilingual audio reports.
The system integrates modern NLP techniques and API-based data retrieval to provide actionable news intelligence for businesses and analysts.

Features
Fetches real-time news using Tavily API
Abstractive summarization using Hugging Face BART model
Sentiment analysis using VADER (NLTK)
Multilingual support (translation-based output)
Text-to-Speech generation using gTTS
Individual article summaries + overall summary
Final sentiment aggregation report
Robust error handling & safe summarization retries
Clean and responsive web UI



System Architecture

User Input (Company Name)
⬇
Tavily API → Fetch News Articles
⬇
Text Cleaning & Preprocessing
⬇
BART Model → Generate Summaries
⬇
VADER → Sentiment Analysis
⬇
Aggregate Sentiment Report
⬇
Translation (Optional Language Selection)
⬇
gTTS → Audio Report Generation
⬇
Display Results in Web Interface


Tech Stack
Backend
Python
Flask
Tavily API
Hugging Face Transformers (facebook/bart-large-cnn)
NLTK (VADER Sentiment Analyzer)
gTTS

Frontend
HTML
CSS
Bootstrap

Other Tools
dotenv for environment variables
REST API integration
Audio file handling


📂 Project Structure
news_summarease/
│
├── app.py
├── backend_api.py
├── tavily_scraper.py
├── utils.py
├── routes.py
├── kpi_extractor.py
├── templates/
├── static/audio/
├── requirements.txt
└── README.md



How It Works:---

User enters a company name.
The Tavily API retrieves related news articles.
Articles are cleaned and passed to BART for abstractive summarization.
VADER analyzes each article’s sentiment.
Sentiments are aggregated to determine overall company sentiment.
The summary is translated (if selected).
gTTS generates an audio version of the final report.
Results are displayed in a structured UI.


Key Highlights

End-to-end AI pipeline implementation
Real-time data integration
Practical NLP application
Multilingual and speech-enabled output
Modular and scalable backend design

Sample Output

Final Sentiment Summary
Overall Summary
Individual Article Summaries
Audio Playback for Reports
