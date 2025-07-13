import os
import openai
import requests
from typing import List


def fetch_latest_news(stock_id: str, api_key: str) -> str:
    """Fetch latest news for a given stock using NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": stock_id,
        "sortBy": "publishedAt",
        "apiKey": api_key,
        "pageSize": 5,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    articles = data.get("articles", [])
    news_items = [f"{a['title']}: {a.get('description', '')}" for a in articles]
    return "\n".join(news_items)


def request_openai(prompt: str) -> str:
    """Send a prompt to the OpenAI API and return the response."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message["content"].strip()


def analyze_stock(stock_id: str, news_api_key: str) -> str:
    news = fetch_latest_news(stock_id, news_api_key)
    prompt = (
        f"Given the following news about stock {stock_id}:\n{news}\n\n"
        "Predict today's maximum and minimum price for this stock and suggest"
        " whether to buy, sell, or take no action today."
    )
    return request_openai(prompt)


def main(stock_ids: List[str]):
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        raise ValueError("NEWS_API_KEY environment variable is not set")

    for stock_id in stock_ids:
        try:
            analysis = analyze_stock(stock_id, news_api_key)
            print(f"Analysis for {stock_id}:\n{analysis}\n")
        except Exception as exc:
            print(f"Error analyzing {stock_id}: {exc}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze stocks with OpenAI")
    parser.add_argument("stocks", nargs="+", help="Stock tickers to analyze")
    args = parser.parse_args()
    main(args.stocks)
