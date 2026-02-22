import os
from tavily import TavilyClient
from dotenv import load_dotenv

# Load API key
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found. Please set it in the .env file.")

client = TavilyClient(api_key=TAVILY_API_KEY)

def scrape_articles(company_name, max_articles=20):
    try:
        # 🔍 Use exact phrase match with quotes
        query = f'"{company_name}" company news'

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_articles,
            include_answer=False,
            include_raw_content=True
        )

        articles = []
        for entry in response.get("results", []):
            content = entry.get("content", "")
            title = entry.get("title", "")

            # ❌ Skip articles that don't mention company name in title or content
            if company_name.lower() not in title.lower() and company_name.lower() not in content.lower():
                continue

            articles.append({
                "title": title or "No Title",
                "link": entry.get("url", "#"),
                "content": content,
                "published": entry.get("date_published", "Not Provided")
            })

        print(f"[INFO] Fetched {len(articles)} articles for '{company_name}'")
        return articles

    except Exception as e:
        print(f"[ERROR] Failed to fetch articles from Tavily: {e}")
        return []
