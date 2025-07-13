# Stock Analyzer

Given several stock ids, use OpenAI to analyze their latest news, predict maximum and minimum values, and suggest whether to buy, sell or take no action today.

## Requirements

- Python 3.8+
- `requests`
- `openai`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Set the following environment variables before running:

- `NEWS_API_KEY` – API key for [NewsAPI](https://newsapi.org/)
- `OPENAI_API_KEY` – your OpenAI API key

## Usage

Run the script with one or more stock tickers:

```bash
python analyze_stocks.py AAPL MSFT TSLA
```

The script will fetch recent news for each stock, ask OpenAI to predict today's maximum and minimum price and output a suggestion to buy, sell or take no action.
