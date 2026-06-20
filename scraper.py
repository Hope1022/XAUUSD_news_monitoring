import requests
import os
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

# reddit = praw.Reddit(
#     client_id=os.getenv("REDDIT_CLIENT_ID"),
#     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
#     user_agent="GoldMonitor/1.0"
# )

def get_newsapi_gold_news():
    try:
       articles = newsapi.get_everything(
            q="gold OR XAUUSD OR XAU",
            language="en",
            sort_by="publishedAt", #give the latest
            page_size=10 #10 articles
        )
        
        results = []
        for article in articles["articles"]: #loop through each article
           
            content = article.get("content") or article.get("description", "")
            if content:
                #this structure will be a common structure for all news
                results.append({
                    "title": article["title"],
                    "content": content,
                    "url": article["url"],
                    "source": "NewsAPI",
                    "published": article["publishedAt"]
                })
        return results
    except Exception as e:
        print(f"NewsAPI failed: {e}")
        return []


def get_guardian_gold_news():
    try:
        
        url = "https://content.guardianapis.com/search"
        params = {
            "q": "gold OR XAUUSD OR inflation",
            "api-key": os.getenv("GUARDIAN_API_KEY"),
            "show-fields": "bodyText",
            "order-by": "newest",
            "page-size": 10
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        results = []
        for item in data["response"]["results"]:
            results.append({
                "title": item["webTitle"],
                "content": item.get("fields", {}).get("bodyText", "")[:500],
                "url": item["webUrl"],
                "source": "The Guardian",
                "published": item["webPublicationDate"]
            })
        return results
    except Exception as e:
        print(f"Guardian failed: {e}")
        return []


def get_nyt_gold_news():
    try:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        params = {
            "q": "gold price OR XAUUSD OR Federal Reserve",
            "api-key": os.getenv("NYT_API_KEY"),
            "sort": "newest",
            "fl": "headline,abstract,web_url,pub_date"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        results = []
        for item in data["response"]["docs"]:
            results.append({
                "title": item["headline"]["main"],
                "content": item.get("abstract", ""),
                "url": item["web_url"],
                "source": "New York Times",
                "published": item["pub_date"]
            })
        return results
    except Exception as e:
        print(f"NYT failed: {e}")
        return []


# def get_reddit_gold_news():
#     try:
#         results = []
#         subreddits = ["Gold", "Forex", "economics"]

#         for sub in subreddits:
#             for post in reddit.subreddit(sub).new(limit=5):
#                 if any(word in post.title.lower()
#                        for word in ["gold", "xauusd", "xau", "inflation"]):
#                     results.append({
#                         "title": post.title,
#                         "content": post.selftext[:500] or post.title,
#                         "url": f"https://reddit.com{post.permalink}",
#                         "source": f"Reddit r/{sub}",
#                         "published": "live"
#                     })
#         return results
    # except Exception as e:
    #     print(f"Reddit failed: {e}")
    #     return []


def get_current_gold_price():
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": "XAU",
            "to_currency": "USD",
            "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        rate = data["Realtime Currency Exchange Rate"]
        price = rate["5. Exchange Rate"]
        return f"${float(price):,.2f} USD"
    except Exception as e:
        print(f"Gold price failed: {e}")
        return "unavailable"

def collect_all_news(use_newsapi=True):
    all_news = []

    if use_newsapi: # this is like checking if our 100 request for the api ended
        
        all_news.extend(get_newsapi_gold_news())

    all_news.extend(get_guardian_gold_news())
    all_news.extend(get_nyt_gold_news())
    # all_news.extend(get_reddit_gold_news())

    print(f"Collected {len(all_news)} articles from all sources")
    return all_news

