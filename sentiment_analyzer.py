from newsapi import NewsApiClient
from textblob import TextBlob

# !!! Замени това с твоя реален NewsAPI ключ !!!
NEWS_API_KEY = "1d4f3fff3f074e4b8009ed96d45439d7"

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def update_sentiment(symbol):
    symbol_map = {
        "tBTCUSD": "Bitcoin",
        "tETHUSD": "Ethereum",
        "tLTCUSD": "Litecoin",
        "tXRPUSD": "Ripple"
    }

    query = symbol_map.get(symbol, "crypto")

    try:
        # Взимаме последните 5 новини
        articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=5)
        sentiments = []

        for article in articles["articles"]:
            title = article.get("title", "")
            description = article.get("description", "")
            content = f"{title}. {description}"

            polarity = TextBlob(content).sentiment.polarity  # от -1 до 1
            sentiments.append(polarity)

        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            return avg_sentiment  # стойност между -1.0 (негативно) и 1.0 (позитивно)
        else:
            return 0.0

    except Exception as e:
        print(f"[❌] Грешка при sentiment анализа: {e}")
        return 0.0

